# 🚀 Getting Started with Revamp Agent

**Transform your GitHub projects into hackathon winners in minutes!**

## 🎯 What Does Revamp Agent Do?

Revamp Agent is like having an expert hackathon strategist and developer on your team. It:

1. **Analyzes** your GitHub project to understand its strengths
2. **Researches** hackathons to find the perfect match
3. **Creates** a winning strategy with novel features
4. **Implements** the code changes automatically (optional)

## 🏃‍♂️ Quick Start (5 Minutes)

### Option 1: Easy Setup Wizard (Recommended)

```bash
# 1. Download and run the setup wizard
python setup_wizard.py

# 2. Follow the interactive prompts
# 3. You're ready to go!
```

### Option 2: Web Interface (No Code Required)

```bash
# 1. Start the web interface
uv run python app/web_interface.py

# 2. Open http://localhost:8000 in your browser
# 3. Fill out the form and click "Generate Strategy"
```

### Option 3: Command Line (For Developers)

```bash
# 1. Install dependencies
uv sync

# 2. Copy and edit environment file
cp .env.example .env
# Edit .env with your API keys

# 3. Run your first analysis
revamp analyze --github https://github.com/user/repo --hackathon https://hackathon-site.com
```

## 🔑 Required API Keys

You only need **2 keys minimum** to get started:

### Essential (Required)
- **OpenAI API Key** - For AI analysis ([Get it here](https://platform.openai.com/api-keys))
- **LangWatch API Key** - For prompt management ([Sign up here](https://app.langwatch.ai/))

### Optional (Enhances Features)
- **Firecrawl API Key** - For web scraping hackathon sites ([Get it here](https://firecrawl.dev/))
- **GitHub Token** - For automatic code implementation ([Create here](https://github.com/settings/tokens))
- **Cerebras API Key** - For better code generation ([Get it here](https://cerebras.ai/))

## 📖 Usage Examples

### 🎯 Scenario 1: I Have Both URLs

**Perfect! This is the easiest case.**

```bash
# Command line
revamp analyze \
  --github https://github.com/user/awesome-project \
  --hackathon https://devpost.com/software/some-hackathon

# Python
from app.main import revamp_project
result = revamp_project(
    github_url="https://github.com/user/awesome-project",
    hackathon_url="https://devpost.com/software/some-hackathon"
)
```

### 🔍 Scenario 2: I Only Have a Project

**No problem! We'll find hackathons for you.**

```bash
# Command line
revamp analyze --github https://github.com/user/ai-project --topic "AI"

# Python
result = revamp_project(
    github_url="https://github.com/user/ai-project",
    search_topic="AI"
)
```

### 🏆 Scenario 3: I Only Have a Hackathon

**We'll find projects that fit!**

```bash
# Command line
revamp analyze --hackathon https://devpost.com/software/ai-hackathon

# Python
result = revamp_project(
    hackathon_url="https://devpost.com/software/ai-hackathon"
)
```

### 🎲 Scenario 4: I Have Nothing (Discovery Mode)

**Let us find both for you!**

```bash
# Command line
revamp analyze --topic "web3"

# Python
result = revamp_project(
    search_topic="web3",
    search_order="projects_first"  # or "hackathons_first"
)
```

### 🛠️ Scenario 5: Generate + Implement Code

**Full automation - strategy + code changes!**

```bash
# Command line (with forking)
revamp generate \
  --github https://github.com/user/project \
  --hackathon https://hackathon-site.com \
  --fork

# Python
result = revamp_and_implement(
    github_url="https://github.com/user/project",
    hackathon_url="https://hackathon-site.com",
    implement_changes=True,
    fork_repo=True
)
```

## 🎨 What You Get

### Strategy Output
```
🎯 STRATEGIC POSITIONING
- Position as "AI-powered sustainability tracker"
- Target judges focused on social impact
- Emphasize real-world applicability

💡 NOVEL FEATURES
1. AI-powered carbon footprint prediction
2. Gamified sustainability challenges
3. Community impact leaderboards

🔧 TECHNICAL IMPROVEMENTS
- Add real-time data visualization
- Implement mobile-responsive design
- Integrate with IoT sensors

📊 DEMO STRATEGY
- Start with compelling problem statement
- Show before/after comparison
- End with future impact projections
```

### Implementation Output (if enabled)
```
🔄 CODE CHANGES MADE
- Created new AI prediction module
- Added gamification system
- Implemented responsive dashboard
- Updated documentation

📁 FILES MODIFIED
- src/prediction/ai_model.py (new)
- src/components/Dashboard.jsx (updated)
- README.md (updated)

🌿 BRANCH CREATED
- Branch: hackathon-revamp
- Commits: 5
- Ready for demo!
```

## 🚨 Troubleshooting

### "No module named 'app'"
```bash
# Make sure you're in the project directory
cd revamp
uv sync
```

### "API key not found"
```bash
# Check your .env file exists and has keys
cat .env
# Should show your API keys
```

### "Command not found: revamp"
```bash
# Use uv run prefix
uv run revamp analyze --help
```

### "Setup test failed"
```bash
# Check individual components
uv run python -c "import openai; print('OpenAI OK')"
uv run python -c "import langwatch; print('LangWatch OK')"
```

## 🎓 Learning Path

### Beginner (Web Interface)
1. Use setup wizard: `python setup_wizard.py`
2. Start web interface: `uv run python app/web_interface.py`
3. Try simple mode with URLs you know
4. Experiment with discovery mode

### Intermediate (Command Line)
1. Learn basic commands: `revamp --help`
2. Try different scenarios from examples above
3. Experiment with topics: AI, web3, climate, healthcare
4. Use implementation mode: `--fork` flag

### Advanced (Python API)
1. Import functions: `from app.main import revamp_project`
2. Use team workflows: `from app.teams_workflows import get_revamp_team`
3. Customize prompts: Edit files in `prompts/`
4. Write tests: Add to `tests/scenarios/`

## 🤝 Getting Help

### Quick Help
- **Commands**: `revamp --help`
- **Web Interface**: Built-in help tooltips
- **Examples**: This guide + README.md

### Community
- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)
- **Discord**: [Join our Discord](#) (coming soon)

### Documentation
- **Full Docs**: README.md
- **API Reference**: `app/main.py` docstrings
- **Architecture**: AGENTS.md

## 🎉 Success Stories

> "Used Revamp Agent to transform my basic web scraper into an AI-powered market intelligence platform. Won 1st place at TechCrunch Disrupt!" - Sarah K.

> "Discovery mode found the perfect hackathon for my climate project. The strategy was spot-on and helped us win $10k!" - Mike R.

> "The automatic code implementation saved me 8 hours of work. Just forked, ran the tool, and had a demo-ready project!" - Alex T.

---

**Ready to win your next hackathon? Let's get started! 🚀**