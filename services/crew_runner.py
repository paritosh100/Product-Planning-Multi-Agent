import os, json, re
from typing import Dict, Any, List
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from pydantic import BaseModel, Field, ValidationError

load_dotenv()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

# -------- Embedded YAML (now Python dicts) --------
AGENTS_CFG = {
    "project_planning_agent": {
        "role": "Project Planner",
        "goal": "Design a JSON-only task plan for {project_type} in {industry}",
        "backstory": "PM who outputs structured JSON, never prose."
    },
    "estimation_agent": {
        "role": "Effort Estimator",
        "goal": "Estimate hours per task in strict JSON",
        "backstory": "Analyst who quantifies workload; JSON only."
    },
    "resource_allocation_agent": {
        "role": "Allocator",
        "goal": "Create milestones and resource allocation in strict JSON",
        "backstory": "Scheduler; returns final JSON only."
    },
}

TASKS_CFG = {
    "task_breakdown": {
        "description": (
            "Using objectives and requirements, produce a task list.\n"
            "Return ONLY valid JSON (no prose, no markdown):\n"
            '{{"tasks":[{{"title":"...", "owner":"..."}}]}}\n'
            "Owners must be team member names when possible.\n"
            "Context:\n"
            "project_type={project_type}\nindustry={industry}\n"
            "objectives={project_objectives}\nrequirements:\n{project_requirements}\nteam:\n{team_members}"
        ),
        "expected_output": 'Valid JSON with "tasks" list.'
    },
    "time_resource_estimation": {
        "description": (
            "Add numeric 'hours' to each task based on complexity and team capacity "
            "over {{horizon_weeks}} weeks. Return ONLY valid JSON:\n"
            '{{"tasks":[{{"title":"...", "owner":"...", "hours": 12.5}}]}}'
        ),
        "expected_output": 'Valid JSON with "tasks" list including numeric "hours".'
    },
    "resource_allocation": {
        "description": (
            "Produce the final plan. Allocate work by weekly capacity over {{horizon_weeks}} weeks. "
            "TODAY is {today_date}. Plan ends on {end_date}. "
            "ALL milestone dates MUST be between {today_date} and {end_date} (YYYY-MM-DD format). "
            "Return ONLY valid JSON EXACTLY in this shape:\n"
            '{{"tasks":[{{"title":"...","owner":"...","hours":0}}],'
            '"milestones":[{{"name":"MVP","due":"YYYY-MM-DD","tasks":["..."]}}],'
            '"resources":[{{"name":"...","role":"...","weekly_hours":20,"allocated_hours":0,"utilization_pct":0}}]}}\n"'
            "No extra keys. No text."
        ),
        "expected_output": "Valid JSON matching the schema above. No extra keys. No text."
    },
}

# -------- Schemas --------
class PlannedTask(BaseModel):
    title: str
    owner: str
    hours: float = Field(..., ge=0)

class PlannedMilestone(BaseModel):
    name: str
    due: str
    tasks: List[str]

class ResourceAlloc(BaseModel):
    name: str
    role: str
    weekly_hours: int | None = None
    allocated_hours: float | None = None
    utilization_pct: float | None = None

class PlanOutput(BaseModel):
    tasks: List[PlannedTask]
    milestones: List[PlannedMilestone]
    resources: List[ResourceAlloc]

# -------- Helpers --------
def _ctx_from_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    from datetime import date, timedelta
    
    team = payload.get("team", [])
    team_members = "\n".join(
        f"- {m.get('name')} ({m.get('role')}) [wh={m.get('weekly_hours') or 'NA'}]" for m in team
    )
    reqs = payload.get("requirements") or []
    horizon_weeks = payload.get("horizon_weeks", 2)
    
    # Calculate date range for planning
    today = date.today()
    end_date = today + timedelta(weeks=horizon_weeks)
    
    return {
        "project_type": payload.get("project_type", ""),
        "industry": payload.get("industry", ""),
        "project_objectives": payload.get("objectives", ""),
        "project_requirements": "\n".join(f"- {r}" for r in reqs),
        "team_members": team_members,
        "horizon_weeks": horizon_weeks,
        "today_date": today.isoformat(),
        "end_date": end_date.isoformat(),
    }

def _render(text: str, ctx: dict) -> str:
    return text.format(**ctx)

def _extract_json(raw) -> dict:
    if isinstance(raw, dict):
        return raw
    s = str(raw)
    m = re.search(r"```json\s*([\s\S]*?)```", s, re.IGNORECASE)
    if m:
        return json.loads(m.group(1))
    m = re.search(r"\{[\s\S]*\}", s)
    if m:
        return json.loads(m.group(0))
    m = re.search(r"\[[\s\S]*\]", s)
    if m:
        return json.loads(m.group(0))
    return {}

# -------- Main --------
def run_crew(payload: Dict[str, Any]) -> Dict[str, Any]:
    ctx = _ctx_from_payload(payload)
    print("Model:", OPENAI_MODEL)

    # Agents
    def make_agent(node: dict) -> Agent:
        return Agent(
            role=_render(node["role"], ctx),
            goal=_render(node["goal"], ctx),
            backstory=_render(node["backstory"], ctx),
            allow_delegation=False,
            verbose=False,
            model=OPENAI_MODEL,
        )

    planner   = make_agent(AGENTS_CFG["project_planning_agent"])
    estimator = make_agent(AGENTS_CFG["estimation_agent"])
    allocator = make_agent(AGENTS_CFG["resource_allocation_agent"])

    # Tasks
    def make_task(node: dict, agent: Agent, extra_ctx: dict | None = None) -> Task:
        dctx = ctx | (extra_ctx or {})
        return Task(
            description=_render(node["description"], dctx),
            expected_output=_render(node["expected_output"], dctx),
            agent=agent,
            input=dctx,
        )

    t1 = make_task(TASKS_CFG["task_breakdown"], planner)
    t2 = make_task(TASKS_CFG["time_resource_estimation"], estimator, {"depends_on": "task_breakdown"})
    t3 = make_task(TASKS_CFG["resource_allocation"], allocator, {"depends_on": "time_resource_estimation"})

    crew = Crew(agents=[planner, estimator, allocator], tasks=[t1, t2, t3], process=Process.sequential, verbose=False)
    result = crew.kickoff()

    raw = result.raw if not isinstance(result.raw, list) else result.raw[-1]
    print("=== Raw CrewAI output (truncated) ===")
    print(str(raw)[:1200])

    data = _extract_json(raw)
    if any(k.startswith('"') or k.endswith('"') for k in data.keys()):
        cleaned = {}
        for k, v in data.items():
            cleaned[k.strip('"').strip("'")] = v
        data = cleaned
    data.setdefault("tasks", [])
    data.setdefault("milestones", [])
    data.setdefault("resources", [])

    try:
        plan = PlanOutput.model_validate(data)
    except ValidationError as e:
        print("Schema validation error:", e)
        plan = PlanOutput(tasks=[], milestones=[], resources=[])

    return plan.model_dump()
