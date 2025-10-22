from datetime import datetime, date, timezone, timedelta
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# deterministic fallback
def _fallback_plan(payload: Dict[str, Any]) -> Dict[str, Any]:
    team = payload.get("team", [])
    horizon_weeks = payload.get("horizon_weeks", 2)
    
    def pick(role_kw, default="Owner"):
        for m in team:
            if role_kw in (m.get("role","").lower()):
                return m["name"]
        return team[0]["name"] if team else default

    tasks = [
        {"title": "Scope & plan",      "owner": pick("project")},
        {"title": "Design prototype",  "owner": pick("design")},
        {"title": "Build MVP",         "owner": pick("engineer")},
        {"title": "QA & release",      "owner": pick("qa")},
    ]
    
    # Calculate milestone dates based on planning horizon
    today = date.today()
    mvp_date = today + timedelta(weeks=horizon_weeks // 2 if horizon_weeks > 1 else 1)
    beta_date = today + timedelta(weeks=horizon_weeks)
    
    milestones = [
        {"name": "MVP",  "due": mvp_date.isoformat(), "tasks": [t["title"] for t in tasks[:2]]},
        {"name": "Beta", "due": beta_date.isoformat(), "tasks": [t["title"] for t in tasks[2:]]},
    ]
    resources = [{"name": m.get("name"), "role": m.get("role"), "weekly_hours": int(m.get("weekly_hours") or 20)} for m in team]
    return {
        "tasks": tasks,
        "milestones": milestones,
        "resources": resources,
        "token_cost": {"input": 0, "output": 0, "usd_estimate": 0.0},
        "meta": {"run_at": datetime.now(timezone.utc).isoformat() + "Z", "crewai_used": False},
    }

def run_planner(payload: Dict[str, Any]) -> Dict[str, Any]:
    estimate = bool(payload.get("estimate_hours"))
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    if estimate and api_key:
        try:
            # fast smoke test
            from openai import OpenAI
            OpenAI().chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "ping"}],
                max_tokens=4,
            )
            # real CrewAI path
            from .crew_runner import run_crew
            plan = run_crew(payload)
            return {
                **plan,
                "token_cost": {"input": 0, "output": 0, "usd_estimate": 0.0},
                "meta": {"run_at": datetime.now(timezone.utc).isoformat() + "Z", "crewai_used": True},
            }
        except Exception as e:
            fb = _fallback_plan(payload)
            fb["meta"]["error"] = f"{type(e).__name__}: {e}"
            fb["meta"]["crewai_used"] = False
            return fb
    
    fb = _fallback_plan(payload)
    fb["meta"]["crewai_used"] = False
    return fb
