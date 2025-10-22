import json
from io import BytesIO
import pandas as pd
import streamlit as st

from services.parsers import parse_team, parse_bullets
from services.planner import run_planner

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
estimate_hours = st.checkbox("Estimate hours", value=False)

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

    with st.spinner("Planning..."):
        result = run_planner(payload)

    st.success("Plan generated")

    st.subheader("Tasks")
    st.dataframe(result.get("tasks", []), use_container_width=True)

    st.subheader("Milestones")
    st.dataframe(result.get("milestones", []), use_container_width=True)

    st.subheader("Team / Resources")
    res = result.get("resources", [])
    if res:
        st.dataframe(res, use_container_width=True)
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
