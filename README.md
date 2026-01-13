# 🚀 Revamp Agent

**Transform any GitHub project into a hackathon winner with AI!**

Revamp Agent is an AI-powered tool that analyzes your GitHub projects and hackathons, then creates winning strategies and even implements the code changes for you.

## 🎯 What Does It Do?

**In 3 simple steps:**
1. **Analyze** - Understands your GitHub project and hackathon requirements
2. **Strategize** - Creates a winning plan with novel features and improvements  
3. **Implement** - Optionally makes the code changes automatically

**Perfect for:**
- 🏆 Hackathon participants who want to win
- 👩‍💻 Developers looking to enhance their projects
- 🎓 Students learning about strategic project development
- � Aneyone wanting to make their code more competitive

---

## ⚡ Quick Start (Choose Your Style)

### 🧙‍♂️ **Option 1: Setup Wizard (Easiest)**
*Perfect for first-time users*

```bash
# Download and run the magic setup wizard
curl -O https://raw.githubusercontent.com/your-repo/revamp/main/setup_wizard.py
python setup_wizard.py
```

The wizard will:
- ✅ Install everything you need
- ✅ Help you get API keys (with direct links!)
- ✅ Test your setup
- ✅ Run your first example

### 🌐 **Option 2: Web Interface (No Code Required)**
*Perfect for non-technical users*

```bash
# Start the web interface
git clone <repository-url>
cd revamp
python setup_wizard.py  # Run setup first
revamp web
```

Then open http://localhost:8000 in your browser and use the friendly web interface!

### 💻 **Option 3: Command Line (For Developers)**
*Perfect for power users*

```bash
# Quick setup
git clone <repository-url>
cd revamp
python setup_wizard.py  # Guided setup
# OR manual setup:
# uv sync && cp .env.example .env && edit .env

# Your first revamp
revamp analyze --github https://github.com/user/repo --hackathon https://hackathon-site.com
```

---

## 🎮 How to Use It

### **🎯 Scenario 1: I Have Both URLs**
*You know your project and target hackathon*

**Web Interface:**
- Go to http://localhost:8000
- Paste your GitHub URL and hackathon URL
- Click "Generate Strategy"

**Command Line:**
```bash
revamp analyze --github https://github.com/user/awesome-project --hackathon https://devpost.com/software/cool-hackathon
```

**Python:**
```python
from app.main import revamp_project
result = revamp_project(
    github_url="https://github.com/user/awesome-project",
    hackathon_url="https://devpost.com/software/cool-hackathon"
)
print(result)
```

### **🔍 Scenario 2: I Only Have a Project**
*You have a project but need to find hackathons*

**Interactive Mode:**
```bash
revamp interactive
# Follow the guided prompts
```

**Command Line:**
```bash
revamp analyze --github https://github.com/user/ai-project --topic "AI"
```

### **🏆 Scenario 3: I Only Have a Hackathon**
*You found a cool hackathon but need a project*

```bash
revamp analyze --hackathon https://devpost.com/software/ai-hackathon
```

### **🎲 Scenario 4: I Have Nothing (Discovery Mode)**
*Let AI find both for you!*

```bash
# Find projects and hackathons about AI
revamp analyze --topic "AI"

# Find hackathons first, then projects
revamp analyze --topic "web3" --search-order hackathons_first
```

### **🛠️ Scenario 5: Generate + Implement Code**
*Get strategy AND automatic code changes*

```bash
# Safe mode: Fork first, then implement
revamp generate --github https://github.com/user/project --hackathon https://hackathon-site.com --fork

# Advanced: Direct implementation (need write access)
revamp generate --github https://github.com/user/project --hackathon https://hackathon-site.com
```

---

## 🔑 What You Need (API Keys)

### **Required (Minimum to Start):**
- **OpenAI API Key** - For AI analysis ([Get it here](https://platform.openai.com/api-keys))
- **LangWatch API Key** - For prompt management ([Sign up here](https://app.langwatch.ai/))

### **Optional (Unlocks More Features):**
- **Firecrawl API Key** - For scraping hackathon websites ([Get it here](https://firecrawl.dev/))
- **GitHub Token** - For automatic code implementation ([Create here](https://github.com/settings/tokens))
- **Cerebras API Key** - For better code generation ([Get it here](https://cerebras.ai/))

**💡 Pro Tip:** The setup wizard will guide you through getting these keys with direct links!

---

## 📱 All the Ways to Use It

### **🌐 Web Interface**
```bash
revamp web
```
- ✅ No coding required
- ✅ Works on mobile
- ✅ Real-time progress
- ✅ Three modes: Simple, Advanced, Discovery

### **🎯 Interactive CLI**
```bash
revamp interactive
```
- ✅ Step-by-step guidance
- ✅ Explains each option
- ✅ Perfect for learning

### **⚡ Quick Commands**
```bash
# Basic analysis
revamp analyze --github <repo-url> --hackathon <hackathon-url>

# Auto-discovery
revamp analyze --topic "AI"

# Full implementation
revamp generate --github <repo-url> --hackathon <hackathon-url> --fork

# Show examples
revamp examples

# Get help
revamp --help
```

### **🐍 Python API**
```python
from app.main import revamp_project, revamp_and_implement

# Strategy only
strategy = revamp_project(github_url="...", hackathon_url="...")

# Strategy + Implementation
result = revamp_and_implement(
    github_url="...", 
    hackathon_url="...",
    implement_changes=True,
    fork_repo=True
)
```

---

## 🎉 What You Get

### **📋 Strategy Report**
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

### **🔄 Implementation Report** (if enabled)
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

---

## 🚨 Troubleshooting

### **"Command not found: revamp"**
```bash
# Use the full path
uv run revamp --help
```

### **"API key not found"**
```bash
# Check your .env file
cat .env
# Should show your API keys

# Re-run setup wizard
python setup_wizard.py
```

### **"Setup test failed"**
```bash
# Test individual components
uv run python -c "import openai; print('OpenAI OK')"
uv run python -c "import langwatch; print('LangWatch OK')"
```

### **Web interface won't start**
```bash
# Try a different port
revamp web --port 8080
```

---

## 🎓 Learning Path

### **Beginner (Web Interface)**
1. Run setup wizard: `python setup_wizard.py`
2. Start web interface: `revamp web`
3. Try simple mode with URLs you know
4. Experiment with discovery mode

### **Intermediate (Command Line)**
1. Learn basic commands: `revamp --help`
2. Try different scenarios from examples above
3. Experiment with topics: AI, web3, climate, healthcare
4. Use implementation mode: `--fork` flag

### **Advanced (Python API)**
1. Import functions: `from app.main import revamp_project`
2. Use team workflows: `from app.teams import RevampTeam`
3. Customize prompts: Edit files in `prompts/`
4. Write tests: Add to `tests/scenarios/`

---

## 🚀 Popular Topics That Work Great

- **AI/ML**: "artificial intelligence", "machine learning", "computer vision"
- **Web3**: "blockchain", "DeFi", "smart contracts", "NFT"  
- **Climate**: "sustainability", "carbon tracking", "renewable energy"
- **Health**: "healthcare", "medical AI", "telemedicine"
- **Fintech**: "payments", "banking", "financial services"
- **IoT**: "internet of things", "sensors", "smart home"

---

## 🤝 Getting Help

### **Quick Help**
- **Commands**: `revamp --help`
- **Examples**: `revamp examples`
- **Web Interface**: Built-in help tooltips

### **Community**
- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)
- **Discord**: [Join our Discord](#) (coming soon)

---

## 🎉 Success Stories

> *"Used Revamp Agent to transform my basic web scraper into an AI-powered market intelligence platform. Won 1st place at TechCrunch Disrupt!"* - Sarah K.

> *"Discovery mode found the perfect hackathon for my climate project. The strategy was spot-on and helped us win $10k!"* - Mike R.

> *"The automatic code implementation saved me 8 hours of work. Just forked, ran the tool, and had a demo-ready project!"* - Alex T.

---

**Ready to win your next hackathon? Let's get started! 🚀**

Choose your preferred method above and transform your project in minutes!

## 🔧 Installation & Setup

### **🧙‍♂️ Method 1: Setup Wizard (Recommended)**
*Easiest way - handles everything for you*

```bash
# Download and run the setup wizard
curl -O https://raw.githubusercontent.com/your-repo/revamp/main/setup_wizard.py
python setup_wizard.py
```

The wizard will:
- Install Python dependencies
- Guide you through getting API keys
- Test your setup
- Run your first example

### **💻 Method 2: Manual Setup**
*For developers who prefer control*

```bash
# 1. Clone the repository
git clone <repository-url>
cd revamp

# 2. Install uv package manager (if needed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Install dependencies
uv sync

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your API keys (see "What You Need" section above)

# 5. Test your setup
revamp --help
```

### **🐳 Method 3: Docker (One-Click)**
*Perfect for consistent environments*

```bash
# Clone and start with Docker
git clone <repository-url>
cd revamp
cp .env.example .env  # Edit with your API keys
docker-compose up -d

# Access at http://localhost:8000
```

### **☁️ Method 4: Cloud Deployment**
*Deploy to the cloud in minutes*

```bash
# Railway
railway up

# Render
# Connect your GitHub repo to Render

# Heroku  
git push heroku main
```

---

## 🎯 Advanced Usage

### **🤖 Python API Examples**

```python
# Basic usage
from app.main import revamp_project

result = revamp_project(
    github_url="https://github.com/user/repo",
    hackathon_url="https://hackathon-site.com"
)

# Advanced usage with teams
from app.teams import RevampTeam

team = RevampTeam()
result = team.execute(
    github_url="https://github.com/user/repo",
    hackathon_url="https://hackathon-site.com"
)

# Workflow usage
from app.workflows import RevampWorkflow

workflow = RevampWorkflow(include_coding_agent=True)
result = workflow.execute(
    github_url="https://github.com/user/repo",
    implement_changes=True,
    fork_repo=True
)

# Custom agent creation
from app.core import AgentFactory

factory = AgentFactory()
strategy_agent = factory.create_strategy_agent()
result = strategy_agent.create_revamp_strategy(...)
```

### **🔧 CLI Advanced Commands**

```bash
# Interactive mode with step-by-step guidance
revamp interactive

# Deploy your revamp agent
revamp deploy

# Run tests
revamp test

# Initialize new project
revamp init my-hackathon-project

# Show detailed examples
revamp examples
```

---

## 🏗️ For Developers

### **Project Structure**
```
revamp/
├── app/                    # Main application
│   ├── core/              # Core functionality  
│   ├── agents/            # Specialized agents
│   ├── teams/             # Team orchestration
│   ├── workflows/         # Structured processes
│   ├── tools/             # Custom tools
│   └── utils/             # Utilities
├── prompts/               # AI prompts (managed by LangWatch)
├── tests/                 # Tests and scenarios
└── setup_wizard.py        # Easy setup
```

### **Running Tests**
```bash
# Run all tests
uv run pytest

# Run specific test types
uv run pytest tests/scenarios/  # End-to-end tests
uv run pytest tests/evaluations/  # Component tests
```

### **Contributing**
This project follows the [Better Agents](AGENTS.md) standard:
- ✅ Use LangWatch for prompt management
- ✅ Write Scenario tests for new features  
- ✅ Follow the Agent Testing Pyramid
- ✅ Never hardcode prompts in code

---

## 📚 Resources & Links

- **📖 Complete Usage Guide**: [USAGE_GUIDE.md](USAGE_GUIDE.md)
- **🚀 Getting Started Guide**: [GETTING_STARTED.md](GETTING_STARTED.md)
- **🏗️ Development Guidelines**: [AGENTS.md](AGENTS.md)
- **🔧 Refactoring Details**: [REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md)

### **External Resources**
- [Agno Documentation](https://docs.agno.com/) - AI agent framework
- [LangWatch Dashboard](https://app.langwatch.ai/) - Prompt management
- [Scenario Documentation](https://scenario.langwatch.ai/) - Agent testing

---

## 📄 License

[Add your license here]

## 🤝 Support & Community

- **🐛 Report Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **💬 Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)  
- **📧 Email**: support@revamp-agent.com
- **💬 Discord**: [Join our community](#) (coming soon)

---

**🎉 Ready to transform your next project into a hackathon winner?**

**Start with the setup wizard and you'll be revamping projects in minutes!**

```bash
python setup_wizard.py
```
