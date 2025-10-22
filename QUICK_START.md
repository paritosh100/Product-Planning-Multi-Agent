# Quick Start Guide - CrewAI Integration ✅

## Status: READY TO USE! 🎉

All checks passed! Your CrewAI integration is fully configured and tested.

---

## How to Use

### 1. Start the Application

```bash
streamlit run streamlit_app.py
```

### 2. In the Streamlit UI

1. Fill in your project details:
   - **Project Type**: e.g., "Website", "Mobile App", "Data Platform"
   - **Industry**: e.g., "Healthcare", "Retail", "Technology"
   - **Objectives**: Your project goals and constraints
   - **Requirements**: Bullet list of features needed
   - **Team Members**: One per line with role and weekly hours
     ```
     - Jane Doe (Software Engineer) [wh=25]
     - John Smith (Project Manager) [wh=10]
     ```

2. **✅ CHECK the "Estimate hours (uses CrewAI if available)" checkbox**  
   ⚠️ **CRITICAL: CrewAI will NOT activate unless this checkbox is checked!**

3. Click **"Run plan"**

### 3. What You'll Get

When CrewAI is active (🧠 CrewAI Active), you'll receive:

- **Detailed task breakdown** with specific owners
- **Hour estimates** for each task based on complexity
- **Smart milestones** aligned with your timeline
- **Resource allocation** with utilization percentages
- **Downloadable JSON and CSV** exports

---

## Verification Checklist

✅ All dependencies installed  
✅ OPENAI_API_KEY configured in .env  
✅ OpenAI API connection tested successfully  
✅ "Estimate hours" checkbox checked in UI  

---

## What's Happening Behind the Scenes?

When you click "Run plan" with CrewAI enabled, three AI agents collaborate:

1. **Project Planner Agent** → Creates task breakdown
2. **Effort Estimator Agent** → Adds time estimates  
3. **Resource Allocator Agent** → Creates milestones and allocations

This sequential workflow ensures comprehensive, realistic project plans.

---

## Troubleshooting

### CrewAI still showing as "Fallback Mode"?

- [ ] Did you check the "Estimate hours" checkbox?
- [ ] Is the app restarted after creating .env?
- [ ] Do you see "🔐 API key loaded: yes" in the UI?

### Getting API errors?

- Check your OpenAI account has credits
- Verify API key is valid
- Try switching model: `OPENAI_MODEL=gpt-3.5-turbo` in .env

---

## Cost Information

Approximate cost per plan:
- **gpt-3.5-turbo**: $0.01 - $0.03 (fastest)
- **gpt-4o-mini**: $0.05 - $0.15 (recommended, balanced)
- **gpt-4o**: $0.30 - $1.00 (most capable)

Default model: `gpt-4o-mini`

---

## Configuration Files

- **`.env`** - Your API keys and settings
- **`requirements.txt`** - Python dependencies
- **`services/crew_runner.py`** - Agent definitions
- **`streamlit_app.py`** - Main UI

---

## Support & Documentation

- 📖 Full guide: `CREWAI_INTEGRATION_GUIDE.md`
- 🔧 Run diagnostics: `python setup_crewai.py`
- 💡 CrewAI docs: https://docs.crewai.com/

---

## Example Input

```
Project Type: E-commerce Website
Industry: Retail
Objectives: Build MVP in 4 weeks with mobile-first design
Requirements:
- Product catalog with search
- Shopping cart
- Payment integration
- User accounts
- Admin dashboard

Team:
- Alice (Full Stack Developer) [wh=40]
- Bob (UI/UX Designer) [wh=20]
- Carol (Project Manager) [wh=15]
```

**Planning horizon**: 4 weeks  
**Estimate hours**: ✅ Checked

---

## Next Steps

1. Run the app: `streamlit run streamlit_app.py`
2. Enter your project details
3. **Check "Estimate hours"**
4. Click "Run plan"
5. Download your project plan!

Happy planning! 🚀

