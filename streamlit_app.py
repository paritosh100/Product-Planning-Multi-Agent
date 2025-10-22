import json
from io import BytesIO
import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from services.parsers import parse_team, parse_bullets
from services.planner import run_planner

# ensure .env is loaded in the Streamlit process
load_dotenv()

st.set_page_config(page_title="Product Project Planner", layout="wide")
st.title("Inputs")

c1, c2 = st.columns(2)
with c1:
    project_type = st.text_input("Project Type", value="", placeholder="e.g., Website, Data product, Mobile app")
    industry = st.text_input("Industry", value="", placeholder="e.g., Healthcare, Retail, Technology")
    objectives = st.text_area(
        "Project Objectives",
        value="",
        height=100,
        placeholder="One or two sentences on goals and constraints",
    )
with c2:
    team_text = st.text_area(
        "Team Members (one per line with role)",
        value="",
        height=160,
        placeholder="- Jane Doe (Software Engineer) [wh=25]\n- John Smith (Project Manager) [wh=10]",
    )
    req_text = st.text_area(
        "Project Requirements (bullet list)",
        value="",
        height=160,
        placeholder="- Responsive design\n- Export CSV\n- Role-based access\n- Dark mode",
    )

st.markdown("---")
horizon_weeks = st.number_input("Planning horizon (weeks)", min_value=1, max_value=52, value=2)
estimate_hours = st.checkbox("Estimate hours (uses CrewAI if available)", value=False)

if st.button("Run plan", type="primary"):
    payload = {
        "project_type": project_type.strip(),
        "industry": industry.strip(),
        "objectives": objectives.strip(),
        "requirements": parse_bullets(req_text),
        "team": parse_team(team_text),
        "estimate_hours": bool(estimate_hours),
        "horizon_weeks": int(horizon_weeks),
    }

    # runtime status
    st.caption(f"🔐 API key loaded: {'yes' if bool(os.getenv('OPENAI_API_KEY')) else 'no'}")
    st.caption(f"🧩 YAML present: agents.yaml/tasks.yaml will be auto-loaded if found")

    with st.spinner("Planning..."):
        result = run_planner(payload)

    meta = result.get("meta", {})
    mode = "🧠 CrewAI Active" if meta.get("crewai_used") else "⚙️ Fallback Mode"
    colA, colB = st.columns(2)
    colA.success(mode)
    if meta.get("error"):
        colB.error(f"CrewAI error: {meta['error']}")

    st.subheader("Tasks")
    st.dataframe(result.get("tasks", []), width="stretch")

    st.subheader("Milestones")
    st.dataframe(result.get("milestones", []), width="stretch")

    st.subheader("Team / Resources")
    res = result.get("resources", [])
    if res:
        st.dataframe(res, width="stretch")
    else:
        st.write("No team provided.")

    # st.subheader("Raw JSON")
    # st.json(result)

    buf = BytesIO(json.dumps(result, indent=2).encode("utf-8"))
    st.download_button("Download plan JSON", data=buf, file_name="project_plan.json", mime="application/json")

    tasks = result.get("tasks", [])
    if tasks:
        tasks_csv = BytesIO(pd.DataFrame(tasks).to_csv(index=False).encode("utf-8"))
        st.download_button("Download tasks CSV", data=tasks_csv, file_name="tasks.csv", mime="text/csv")
