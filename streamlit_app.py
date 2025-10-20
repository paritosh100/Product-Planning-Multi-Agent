
import os
import yaml
import json
import streamlit as st
from typing import List
from pydantic import BaseModel, Field
from crewai import Agent, Task, Crew

# ---------- Models matching the notebook ----------
class TaskEstimate(BaseModel):
    task_name: str = Field(..., description="Name of the task")
    estimated_time_hours: float = Field(..., description="Estimated time to complete the task in hours")
    required_resources: List[str] = Field(..., description="List of resources required to complete the task")

class Milestone(BaseModel):
    milestone_name: str = Field(..., description="Name of the milestone")
    tasks: List[str] = Field(..., description="List of task IDs associated with this milestone")

class ProjectPlan(BaseModel):
    tasks: List[TaskEstimate] = Field(..., description="List of tasks with their estimates")
    milestones: List[Milestone] = Field(..., description="List of project milestones")

# ---------- Helpers ----------
@st.cache_data(show_spinner=False)
def load_yaml(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_configs(agents_path: str, tasks_path: str):
    agents_config = load_yaml(agents_path)
    tasks_config = load_yaml(tasks_path)
    return agents_config, tasks_config

def build_crew(agents_config, tasks_config):
    # Agents
    project_planning_agent = Agent(config=agents_config['project_planning_agent'])
    estimation_agent       = Agent(config=agents_config['estimation_agent'])
    resource_alloc_agent   = Agent(config=agents_config['resource_allocation_agent'])

    # Tasks
    task_breakdown = Task(
        config=tasks_config['task_breakdown'],
        agent=project_planning_agent
    )
    time_resource_estimation = Task(
        config=tasks_config['time_resource_estimation'],
        agent=estimation_agent
    )
    resource_allocation = Task(
        config=tasks_config['resource_allocation'],
        agent=resource_alloc_agent,
        output_pydantic=ProjectPlan
    )

    crew = Crew(
        agents=[project_planning_agent, estimation_agent, resource_alloc_agent],
        tasks=[task_breakdown, time_resource_estimation, resource_allocation],
        verbose=True
    )
    return crew

def estimate_cost(usage_metrics):
    # Notebook logic: $0.150 per 1,000,000 tokens for both prompt + completion
    total_tokens = (usage_metrics.prompt_tokens or 0) + (usage_metrics.completion_tokens or 0)
    return 0.150 * (total_tokens / 1_000_000.0)

# ---------- UI ----------
st.set_page_config(page_title="L1 Project Planner", layout="wide")

st.title("L1: Automated Project Planning, Estimation, and Allocation")

with st.sidebar:
    st.header("Configs")
    agents_path = st.text_input("agents.yaml path", value="config/agents.yaml")
    tasks_path  = st.text_input("tasks.yaml path",  value="config/tasks.yaml")
    st.caption("Paths are relative to the working directory.")

st.subheader("Inputs")
col1, col2 = st.columns(2)

with col1:
    project_type = st.text_input("Project Type", value="Website")
    industry = st.text_input("Industry", value="Technology")
    project_objectives = st.text_area("Project Objectives", value="Create a website for a small business", height=100)

with col2:
    team_members = st.text_area("Team Members (one per line with role)", value="- John Doe (Project Manager)\n- Jane Doe (Software Engineer)\n- Bob Smith (Designer)\n- Alice Johnson (QA Engineer)\n- Tom Brown (QA Engineer)", height=120)
    project_requirements = st.text_area("Project Requirements (bullet list)", value="- Responsive design\n- Modern UI\n- Intuitive navigation\n- About Us page\n- Services page\n- Contact form with map\n- Blog section\n- Fast loading + SEO\n- Social links\n- Basic analytics", height=160)

run = st.button("Run plan")

if run:
    try:
        agents_config, tasks_config = load_configs(agents_path, tasks_path)
        crew = build_crew(agents_config, tasks_config)

        inputs = {
            "project_type": project_type,
            "project_objectives": project_objectives,
            "industry": industry,
            "team_members": team_members,
            "project_requirements": project_requirements
        }

        with st.spinner("Running Crew..."):
            result = crew.kickoff(inputs=inputs)

        # Structured result
        plan_dict = result.pydantic.dict() if hasattr(result, "pydantic") else {}

        st.success("Plan generated")
        st.download_button("Download raw JSON", data=json.dumps(plan_dict, indent=2), file_name="plan.json", mime="application/json")

        # Tasks
        tasks = plan_dict.get("tasks", [])
        if tasks:
            st.markdown("### Tasks")
            st.dataframe(tasks, use_container_width=True)

        # Milestones
        milestones = plan_dict.get("milestones", [])
        if milestones:
            st.markdown("### Milestones")
            st.dataframe(milestones, use_container_width=True)

        # Usage and Cost
        try:
            usage = crew.usage_metrics.dict()  # crewai UsageMetrics -> dict
            st.markdown("### Usage metrics")
            st.json(usage)

            # Token cost estimate
            # Some versions may not have attributes; guard with dict keys.
            prompt_tokens = usage.get("prompt_tokens", 0) or 0
            completion_tokens = usage.get("completion_tokens", 0) or 0
            total_tokens = prompt_tokens + completion_tokens
            est_cost = 0.150 * (total_tokens / 1_000_000.0)
            st.metric("Estimated token cost (USD)", f"${est_cost:.4f}", help="Rate: $0.150 per 1M tokens")
        except Exception as e:
            st.info("Usage metrics not available from CrewAI version in use.")

    except FileNotFoundError as e:
        st.error(f"Config file not found: {e}")
    except KeyError as e:
        st.error(f"Missing expected key in YAML or result: {e}")
    except Exception as e:
        st.exception(e)
else:
    st.info("Set YAML paths and inputs. Click 'Run plan'.")
