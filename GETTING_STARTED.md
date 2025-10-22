# 🚀 Getting Started - Your First AI-Powered Project Plan

Welcome! This guide will help you create your first intelligent project plan in just **5 minutes**.

---

## ✅ Prerequisites Checklist

Before you begin, make sure you have:

- [ ] **Python 3.10 or higher** installed
- [ ] **Internet connection** (for AI agents)
- [ ] **OpenAI API key** (free to get, pennies to use)
- [ ] **5 minutes** of your time

---

## 📋 Step-by-Step Setup

### Step 1: Install Dependencies (2 minutes)

Open your terminal in the project folder and run:

```bash
pip install -r requirements.txt
```

**What this does**: Installs all the tools the AI agents need to work.

---

### Step 2: Get Your OpenAI API Key (2 minutes)

1. Go to: https://platform.openai.com/api-keys
2. Sign in (or create a free account)
3. Click **"Create new secret key"**
4. Copy the key (starts with `sk-`)

**Cost**: ~$0.10 per plan. Your first $5 is usually free!

---

### Step 3: Configure Your Environment (1 minute)

Create a file named `.env` in the project root folder:

```bash
# Windows
notepad .env

# Mac/Linux
nano .env
```

Add this content (replace with your actual key):

```
OPENAI_API_KEY=sk-your-actual-key-here
OPENAI_MODEL=gpt-4o-mini
```

Save and close the file.

---

### Step 4: Launch the Application

Run this command:

```bash
streamlit run streamlit_app.py
```

The app will open in your browser automatically! 🎉

---

## 🎯 Creating Your First Plan

### 1. Fill in Basic Info

```
Project Type: E-commerce Website
Industry: Retail
```

### 2. Describe Your Objectives

```
Build a modern online store for selling handmade crafts
Must handle 100+ products and process payments securely
Launch MVP in 4 weeks
```

### 3. Add Your Team

```
- Alice Johnson (Full Stack Developer) [wh=40]
- Bob Smith (UI/UX Designer) [wh=20]
- Carol Martinez (Project Manager) [wh=15]
```

**Format**: `- Name (Role) [wh=hours per week]`

### 4. List Requirements

```
- Product catalog with search
- Shopping cart functionality
- Stripe payment integration
- Customer accounts
- Admin dashboard
- Mobile responsive design
```

### 5. Set Timeline

```
Planning horizon: 4 weeks
```

### 6. ✅ CRITICAL: Activate AI Agents

**Check the box**: ✅ **"Estimate hours (uses CrewAI if available)"**

> ⚠️ **If you don't check this box, you'll get basic templates instead of AI intelligence!**

### 7. Click "Run plan"

Watch the magic happen! ✨

---

## 🎭 What to Expect

### While the AI Agents Work (~20 seconds)

You'll see "Planning..." with a spinner. Behind the scenes:

1. 🤖 Agent 1 is analyzing your requirements
2. 🤖 Agent 2 is calculating realistic hours
3. 🤖 Agent 3 is optimizing resource allocation

### When It's Done

You'll see three sections:

#### 📋 **Tasks**
Detailed breakdown with:
- Specific task titles
- Assigned team member
- Hour estimates

#### 🎯 **Milestones**
Key project phases:
- MVP milestone (halfway)
- Beta milestone (completion)
- Linked tasks for each

#### 👥 **Team / Resources**
Team utilization:
- Weekly hours available
- Allocated hours
- Utilization percentage

---

## 🎨 Understanding the Results

### Status Indicators

Look at the top of the results:

#### ✅ Success: "🧠 CrewAI Active"
**What it means**: Your AI agents worked! You got intelligent planning.

**You'll see:**
- Context-specific tasks (not generic templates)
- Realistic hour estimates
- Smart resource allocation
- Dates within your timeline

#### ⚠️ Fallback: "⚙️ Fallback Mode"
**What it means**: AI agents didn't run. You got basic templates.

**Common causes:**
1. ❌ "Estimate hours" checkbox not checked
2. ❌ Missing or invalid API key
3. ❌ App needs restart after adding .env

**How to fix**: See troubleshooting below ⬇️

---

## 🔧 Troubleshooting

### Problem: Still seeing "Fallback Mode"

**Check this list in order:**

1. **Is the checkbox checked?**
   - ✅ Look for: "Estimate hours (uses CrewAI if available)"
   - If not checked, check it and try again

2. **Is the API key loaded?**
   - Look for: "🔐 API key loaded: yes"
   - If it says "no", your .env file isn't working

3. **Did you restart the app?**
   - After creating/editing .env, you MUST restart:
   - Press `Ctrl+C` in terminal
   - Run `streamlit run streamlit_app.py` again

4. **Is your API key valid?**
   - Run the diagnostic: `python setup_crewai.py`
   - It will test your API connection

### Problem: "API Error" or "Rate Limit"

**Solutions:**
- Check your OpenAI account has credits
- Try a different model in .env:
  ```
  OPENAI_MODEL=gpt-3.5-turbo  # Faster and cheaper
  ```

### Problem: Very Slow Response

**This is normal!** AI agents are:
- Reading your requirements
- Analyzing complexity
- Discussing among themselves
- Optimizing the plan

**Typical times:**
- Small project (2 weeks): 15-20 seconds
- Medium project (4 weeks): 20-30 seconds
- Large project (8+ weeks): 30-45 seconds

**To speed up:**
- Use faster model: `OPENAI_MODEL=gpt-3.5-turbo`
- Reduce requirements list
- Shorter objectives description

---

## 💾 Downloading Your Plan

After getting results, you can:

### 📄 Download Full Plan (JSON)
- Click "Download plan JSON"
- Contains all tasks, milestones, and resources
- Can import into other tools

### 📊 Download Tasks (CSV)
- Click "Download tasks CSV"
- Open in Excel/Google Sheets
- Great for sharing with team

---

## 🎓 Pro Tips

### 1. Be Specific in Objectives
❌ **Generic**: "Build a website"
✅ **Specific**: "Build a booking system for yoga classes with payment processing"

### 2. List Real Requirements
The more details you provide, the smarter the AI's suggestions:
- Security needs (HIPAA, GDPR, etc.)
- Integrations (Stripe, Google Maps, etc.)
- Platforms (iOS, Android, web)
- Special features

### 3. Accurate Team Info
AI considers:
- Available hours per week
- Role types (affects task assignment)
- Team size (affects parallelization)

### 4. Realistic Timeline
- 1-2 weeks: Very small projects
- 3-4 weeks: Small projects
- 5-8 weeks: Medium projects
- 8+ weeks: Large projects

---

## 🎯 Example Projects

### Quick Website (2 weeks)
```
Type: Marketing Website
Team: 1 developer, 1 designer (both 20h/week)
Requirements: 5 pages, contact form, blog
```

### Mobile App (6 weeks)
```
Type: Mobile Application  
Team: 2 developers, 1 designer, 1 PM (total 100h/week)
Requirements: User auth, real-time chat, payments, notifications
```

### Enterprise Platform (12 weeks)
```
Type: Enterprise Software
Team: 4 developers, 2 designers, 1 PM, 1 QA (total 200h/week)
Requirements: Multi-tenant, SSO, admin portal, analytics, API
```

---

## 📚 Next Steps

After your first plan:

1. **Experiment**: Try different project types
2. **Compare**: Run same project with/without AI to see the difference
3. **Refine**: Adjust requirements and see how the plan adapts
4. **Export**: Use the plans in your actual project management
5. **Share**: Show your team the AI-generated timelines

---

## 🆘 Need Help?

### Run Diagnostics
```bash
python setup_crewai.py
```

This will check:
- ✅ All dependencies installed
- ✅ API key configured
- ✅ API connection working

### Check Documentation
- **[README.md](README.md)** - Full overview
- **[QUICK_START.md](QUICK_START.md)** - Quick reference
- **[CREWAI_INTEGRATION_GUIDE.md](CREWAI_INTEGRATION_GUIDE.md)** - Deep technical dive

### Common Questions

**Q: How much does it cost?**
A: About $0.05-$0.15 per plan with gpt-4o-mini. Very affordable!

**Q: Can I use it offline?**
A: No, AI agents need internet to think. But you can export plans and use them offline.

**Q: Is my project data safe?**
A: Yes! OpenAI doesn't train on API data. See their privacy policy.

**Q: Can I customize the agents?**
A: Yes! Edit `services/crew_runner.py` to change agent behavior.

---

## 🎉 Success Checklist

You know it's working when you see:

- ✅ "🧠 CrewAI Active" status
- ✅ "🔐 API key loaded: yes"
- ✅ 8-15 specific tasks (not 4 generic ones)
- ✅ Hour estimates on each task
- ✅ Realistic milestone dates
- ✅ Team utilization percentages

---

<div align="center">

## 🚀 Ready? Let's Create Your First Plan!

1. Run `streamlit run streamlit_app.py`
2. Fill in your project
3. Check "Estimate hours" ✅
4. Click "Run plan"
5. Watch AI agents work their magic! ✨

---

**Questions?** Check the [README](README.md) or run diagnostics: `python setup_crewai.py`

</div>

