
# 🚀 Product Project Planner — CrewAI + Streamlit

An **AI-powered project planning assistant** that automates task breakdown, time/resource estimation, and milestone creation.  
Built with [CrewAI](https://github.com/joaomdmoura/crewai) and a clean [Streamlit](https://streamlit.io) frontend.

---

## 🧠 What it does

Product Project Planner takes a few plain‑text project inputs — like type, objectives, team members, and requirements — and generates:
- 🗂️ A **structured task list** with estimated hours and required resources.  
- 🏁 A **milestone breakdown** showing grouped deliverables.  
- 💰 **Usage metrics** with estimated token cost.  
- 📦 Downloadable JSON outputs for reuse in your own systems.

---

## ⚙️ Tech Stack

| Layer | Tools |
|-------|-------|
| **Core AI Logic** | CrewAI (Agents, Tasks, Crew orchestration) |
| **Frontend** | Streamlit |
| **Data Models** | Pydantic v2 |
| **Config** | YAML (agents.yaml, tasks.yaml) |
| **Packaging** | requirements.txt |

---

## 📁 Project Structure

```
.
├── config/
│   ├── agents.yaml
│   └── tasks.yaml
├── streamlit_app.py
├── requirements.txt
└── README.md
```

---

## 🧩 Installation

```bash
# 1. Clone repository or copy files
git clone <repo_url>
cd Product Project Planner-project-planner

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run Streamlit
streamlit run streamlit_app.py
```

---

## 🪄 Usage

1. Open the Streamlit sidebar.  
2. Set paths for your YAML config files.  
3. Fill in project details:
   - Project Type (e.g., Website, Mobile App)
   - Industry
   - Objectives
   - Team Members
   - Requirements  
4. Click **“Run Plan”** to trigger the CrewAI agents.

The app will display three tabs:  
✅ Tasks table • ✅ Milestones • ✅ Token Cost Summary  

You can also download the generated JSON for further processing.

---

## 🧰 YAML Config Expectations

### agents.yaml
```yaml
project_planning_agent:
  role: "Planner"
  goal: "Break down objectives into tasks"

estimation_agent:
  role: "Estimator"
  goal: "Estimate time and resources for each task"

resource_allocation_agent:
  role: "Allocator"
  goal: "Group tasks into milestones and finalize plan"
```

### tasks.yaml
```yaml
task_breakdown:
  description: "Break down project objectives into tasks"

time_resource_estimation:
  description: "Estimate time and resource usage per task"

resource_allocation:
  description: "Form milestones and output final ProjectPlan"
```

---

## 🧾 Output Schema

```json
{
  "tasks": [
    {"task_name": "Design UI", "estimated_time_hours": 8.5, "required_resources": ["Designer", "Figma"]}
  ],
  "milestones": [
    {"milestone_name": "Design Phase", "tasks": ["Design UI", "Review UI"]}
  ]
}
```

---

## 💡 Ideas for Extension

- 📊 Gantt chart visualization using Plotly or Altair  
- 🔄 Integration with Notion, Jira, or Trello APIs  
- ☁️ FastAPI backend + React frontend for multi‑user access  
- 🧮 Persistent DB (SQLite / Postgres) to store historical runs  
- 🧑‍💼 User authentication and plan versioning

---

## 🧑‍💻 Author

**Paritosh Gandre**  
M.S. Data Science, Kent State University  
[GitHub](https://github.com/paritosh100) • [Portfolio](https://paritosh-gandre.vercel.app) • [LinkedIn](https://linkedin.com/in/paritosh-gandre)

---

## 🏷️ License

MIT License © 2025  
Free to use, modify, and share.
