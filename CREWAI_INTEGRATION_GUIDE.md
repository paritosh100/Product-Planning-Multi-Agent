# CrewAI Integration Guide

This guide will help you integrate CrewAI into your Multi-AI Agent Project Planner.

## Prerequisites

- Python 3.9 or higher
- OpenAI API account with credits

## Step-by-Step Integration

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Or if using Pipenv:

```bash
pipenv install
```

### 2. Set Up Environment Variables

1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit the `.env` file** and add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   OPENAI_MODEL=gpt-4o-mini
   ```

   **Where to get your API key:**
   - Go to: https://platform.openai.com/api-keys
   - Sign in or create an account
   - Click "Create new secret key"
   - Copy the key and paste it in your `.env` file

### 3. Verify Your Setup

The app will automatically check for:
- ✅ API key presence
- ✅ YAML configuration files (agents.yaml, tasks.yaml)

You'll see status indicators in the UI:
- 🔐 API key loaded: yes/no
- 🧩 YAML present: agents.yaml/tasks.yaml will be auto-loaded if found

### 4. Run the Application

```bash
streamlit run streamlit_app.py
```

### 5. Activate CrewAI

In the Streamlit interface:
1. Fill in the project details (type, industry, objectives, requirements, team)
2. **CHECK the "Estimate hours" checkbox** ✅ (this is crucial!)
3. Click "Run plan"

### Expected Behavior

**With CrewAI Active:**
- Status: 🧠 CrewAI Active
- Three AI agents will collaborate:
  - **Project Planner**: Creates task breakdown
  - **Effort Estimator**: Adds time estimates
  - **Resource Allocator**: Creates milestones and allocations
- More detailed and accurate project plans
- Hour estimates for each task

**Fallback Mode:**
- Status: ⚙️ Fallback Mode
- Uses deterministic template-based planning
- No hour estimates
- Basic task structure

## Troubleshooting

### CrewAI not activating?

Check these conditions:
1. ✅ "Estimate hours" checkbox is checked
2. ✅ `.env` file exists in project root
3. ✅ `OPENAI_API_KEY` is set correctly
4. ✅ Streamlit app restarted after creating `.env`
5. ✅ OpenAI API key has credits available

### Error: "KeyError: '"tasks"'"

This has been fixed in the latest code. Make sure you have the updated `services/crew_runner.py`.

### API Rate Limits

If you hit rate limits:
- Switch to `OPENAI_MODEL=gpt-3.5-turbo` (faster, cheaper)
- Add delays between requests
- Check your OpenAI account usage and limits

### Slow Performance

- Use `gpt-4o-mini` instead of `gpt-4o` for faster responses
- CrewAI runs 3 sequential agent tasks, so expect 15-30 seconds per plan

## How It Works

### Architecture

```
User Input → Streamlit UI → run_planner() → CrewAI Crew
                                              ├── Agent 1: Project Planner
                                              ├── Agent 2: Effort Estimator  
                                              └── Agent 3: Resource Allocator
                                              ↓
                              JSON Output → Parse & Validate → Display
```

### Agent Workflow

1. **Project Planning Agent**
   - Receives: project type, industry, objectives, requirements, team
   - Outputs: JSON with task list and owners

2. **Estimation Agent**
   - Receives: tasks from Agent 1
   - Adds: hour estimates based on complexity and team capacity

3. **Resource Allocation Agent**
   - Receives: tasks with estimates
   - Creates: milestones, resource allocations, utilization percentages

### Data Flow

All agents communicate via JSON to ensure structured output. The final output schema:

```json
{
  "tasks": [
    {"title": "...", "owner": "...", "hours": 12.5}
  ],
  "milestones": [
    {"name": "MVP", "due": "2025-10-30", "tasks": ["..."]}
  ],
  "resources": [
    {
      "name": "Jane Doe",
      "role": "Software Engineer", 
      "weekly_hours": 25,
      "allocated_hours": 40,
      "utilization_pct": 80
    }
  ]
}
```

## Configuration

### Customizing Agents

Edit `services/crew_runner.py` to modify agent behavior:
- Change agent roles, goals, or backstories (lines 11-27)
- Modify task descriptions (lines 29-61)
- Adjust model parameters

### Changing Models

In `.env`:
- **Fastest/Cheapest**: `OPENAI_MODEL=gpt-3.5-turbo`
- **Balanced**: `OPENAI_MODEL=gpt-4o-mini` (recommended)
- **Most Capable**: `OPENAI_MODEL=gpt-4o`

## Cost Estimates

Approximate costs per plan (varies by input size):
- gpt-3.5-turbo: $0.01 - $0.03
- gpt-4o-mini: $0.05 - $0.15
- gpt-4o: $0.30 - $1.00

## Support

For issues or questions:
1. Check the error message in the UI
2. Review console output for debugging info
3. Verify all prerequisites are met
4. Check OpenAI API status: https://status.openai.com/

## Next Steps

Once integrated, you can:
- Export plans as JSON or CSV
- Customize agent prompts for your domain
- Add more agents for specialized tasks
- Integrate with project management tools

Happy planning! 🚀

