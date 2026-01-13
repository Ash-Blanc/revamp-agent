# 🎯 Complete Usage Guide: Revamp Agent

## 📋 Table of Contents
1. [Quick Reference](#quick-reference)
2. [Installation Methods](#installation-methods)
3. [Usage Methods](#usage-methods)
4. [API Reference](#api-reference)
5. [Advanced Features](#advanced-features)
6. [Troubleshooting](#troubleshooting)

## 🚀 Quick Reference

### Fastest Ways to Get Started

| Method | Best For | Command |
|--------|----------|---------|
| **Setup Wizard** | First-time users | `python setup_wizard.py` |
| **Web Interface** | Non-technical users | `revamp web` |
| **Interactive CLI** | Guided experience | `revamp interactive` |
| **Direct CLI** | Power users | `revamp analyze --github URL --hackathon URL` |

## 🛠️ Installation Methods

### Method 1: Automated Setup (Recommended)
```bash
# Download and run setup wizard
curl -O https://raw.githubusercontent.com/your-repo/revamp/main/setup_wizard.py
python setup_wizard.py
```

### Method 2: Manual Setup
```bash
# Clone repository
git clone https://github.com/your-repo/revamp.git
cd revamp

# Install uv (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Setup environment
cp .env.example .env
# Edit .env with your API keys
```

### Method 3: Docker (One-Click)
```bash
# Clone and start with Docker
git clone https://github.com/your-repo/revamp.git
cd revamp
cp .env.example .env  # Edit with your keys
docker-compose up -d
```

### Method 4: Cloud Deployment
- **Railway**: `railway up`
- **Render**: Connect GitHub repo
- **Heroku**: `git push heroku main`

## 🎮 Usage Methods

### 1. Web Interface (Easiest)

**Start the interface:**
```bash
revamp web
# Opens http://localhost:8000
```

**Features:**
- ✅ No coding required
- ✅ Mobile-friendly
- ✅ Real-time progress tracking
- ✅ Three modes: Simple, Advanced, Discovery

### 2. Interactive CLI (Guided)

**Start interactive mode:**
```bash
revamp interactive
```

**What it does:**
- Asks questions step-by-step
- Guides you through all options
- Explains each choice
- Perfect for learning

### 3. Direct CLI Commands

#### Basic Analysis
```bash
# With both URLs
revamp analyze --github https://github.com/user/repo --hackathon https://hackathon-site.com

# With context
revamp analyze --github https://github.com/user/repo --context "AI healthcare hackathon"

# Discovery mode
revamp analyze --topic "AI" --search-order projects_first
```

#### Full Implementation
```bash
# Generate strategy + implement code
revamp generate --github https://github.com/user/repo --hackathon https://hackathon-site.com --fork

# With custom branch
revamp generate --github https://github.com/user/repo --hackathon https://hackathon-site.com --fork --branch "my-hackathon-branch"
```

#### Discovery Examples
```bash
# Find AI projects and hackathons
revamp analyze --topic "AI"

# Find hackathons first, then projects
revamp analyze --topic "web3" --search-order hackathons_first

# Specific technology focus
revamp analyze --topic "React TypeScript"
```

### 4. Python API (Most Flexible)

#### Basic Usage
```python
from app.main import revamp_project, revamp_and_implement

# Strategy only
strategy = revamp_project(
    github_url="https://github.com/user/repo",
    hackathon_url="https://hackathon-site.com"
)
print(strategy)

# Strategy + Implementation
result = revamp_and_implement(
    github_url="https://github.com/user/repo",
    hackathon_url="https://hackathon-site.com",
    implement_changes=True,
    fork_repo=True
)
print(result["strategy"])
print(result["implementation"])
```

#### Advanced Usage
```python
# Using team workflows
from app.teams_workflows import get_revamp_workflow

workflow = get_revamp_workflow()
result = workflow.run_workflow(
    github_url="https://github.com/user/repo",
    hackathon_url="https://hackathon-site.com"
)

# Using session management
from app.session_manager import get_session_manager

session_manager = get_session_manager()
session_id = session_manager.create_session(user_id="user123")
# Use session_id for tracking conversations
```

#### Discovery API
```python
from app.tools import HackathonDiscoveryTools

tools = HackathonDiscoveryTools()

# Find hackathons
hackathons = tools.find_ongoing_hackathons("AI hackathon", max_results=5)

# Find projects
projects = tools.find_relevant_github_projects("AI", language="python")

# Smart matching
matching_hackathons = tools.find_hackathons_for_project(
    project_topic="machine learning",
    project_tech_stack="Python, TensorFlow"
)
```

## 📚 API Reference

### Core Functions

#### `revamp_project()`
**Purpose:** Generate revamp strategy only

**Parameters:**
- `github_url` (str, optional): GitHub repository URL
- `hackathon_url` (str, optional): Hackathon website URL  
- `hackathon_context` (str, optional): Additional hackathon description
- `search_order` (str): "projects_first" or "hackathons_first"
- `search_topic` (str, optional): Topic for discovery

**Returns:** String with comprehensive revamp strategy

#### `revamp_and_implement()`
**Purpose:** Generate strategy + implement code changes

**Parameters:** Same as `revamp_project()` plus:
- `implement_changes` (bool): Enable code implementation
- `fork_repo` (bool): Fork repository before changes
- `branch_name` (str): Branch name for changes

**Returns:** Dictionary with:
- `strategy`: The revamp strategy
- `implementation`: Implementation summary
- `repo_name`: Repository used

### Discovery Tools

#### `find_ongoing_hackathons(query, max_results=5)`
**Purpose:** Search for active hackathons

**Returns:** List of dictionaries with:
- `name`: Hackathon name
- `url`: Website URL
- `description`: Brief description
- `deadline`: Deadline if available

#### `find_relevant_github_projects(topic, language=None, max_results=5)`
**Purpose:** Search for GitHub projects by topic

**Returns:** List of dictionaries with:
- `name`: Project name
- `url`: GitHub URL
- `description`: Project description
- `stars`: Star count (if available)

## 🔧 Advanced Features

### 1. Multi-Model Support
The coding agent uses multiple AI models with fallback:
1. **Cerebras** (primary) - Fast and efficient
2. **Mistral** (fallback 1) - Reliable alternative  
3. **OpenRouter** (fallback 2) - Access to multiple models
4. **OpenAI** (final fallback) - Always available

### 2. Memory & Sessions
```python
# Persistent memory across conversations
from app.memory_storage import get_memory_manager
memory = get_memory_manager()
memory.store_user_memory("user123", "preferences", {"topic": "AI"})

# Session tracking for multi-turn conversations
from app.session_manager import get_session_manager
session = get_session_manager()
session_id = session.create_session(user_id="user123")
```

### 3. Team Workflows
```python
# Use specialized agent teams
from app.teams_workflows import get_revamp_team

team = get_revamp_team()
# Team includes: ProjectAnalyzer, HackathonResearcher, StrategyDeveloper
```

### 4. Custom Prompts
```bash
# Manage prompts with LangWatch
langwatch prompt create my_custom_prompt
langwatch prompt sync
```

### 5. Web Scraping
Automatic extraction from hackathon websites:
- Themes and focus areas
- Judging criteria
- Deadlines and requirements
- Prize information
- Sponsor details

## 🎯 Use Case Examples

### Scenario 1: Complete Beginner
```bash
# 1. Run setup wizard
python setup_wizard.py

# 2. Start web interface
revamp web

# 3. Use Simple Mode with URLs you know
```

### Scenario 2: Developer with Project
```bash
# 1. Quick analysis
revamp analyze --github https://github.com/myuser/myproject --topic "AI"

# 2. If you like the strategy, implement it
revamp generate --github https://github.com/myuser/myproject --hackathon <found-hackathon-url> --fork
```

### Scenario 3: Hackathon Participant
```bash
# 1. Find projects for your hackathon
revamp analyze --hackathon https://devpost.com/software/your-hackathon

# 2. Implement on chosen project
revamp generate --github <chosen-project> --hackathon <your-hackathon> --fork
```

### Scenario 4: Team Lead
```python
# Use Python API for custom workflows
from app.main import revamp_and_implement

# Batch process multiple projects
projects = ["user/proj1", "user/proj2", "user/proj3"]
hackathon = "https://hackathon-site.com"

for project in projects:
    result = revamp_and_implement(
        github_url=f"https://github.com/{project}",
        hackathon_url=hackathon,
        implement_changes=True,
        fork_repo=True
    )
    print(f"Project {project}: {result['strategy'][:100]}...")
```

### Scenario 5: Research & Discovery
```bash
# Explore what's possible in different domains
revamp analyze --topic "climate tech"
revamp analyze --topic "fintech"  
revamp analyze --topic "healthcare AI"
revamp analyze --topic "web3 gaming"
```

## 🚨 Troubleshooting

### Common Issues

#### "Command not found: revamp"
```bash
# Use uv run prefix
uv run revamp --help

# Or activate virtual environment
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
revamp --help
```

#### "API key not found"
```bash
# Check .env file exists and has correct keys
cat .env
# Should show: OPENAI_API_KEY=sk-...

# Test API key
uv run python -c "import openai; print('OpenAI key works')"
```

#### "No module named 'app'"
```bash
# Make sure you're in project directory
pwd  # Should show /path/to/revamp
ls   # Should show app/ folder

# Reinstall dependencies
uv sync
```

#### Web interface won't start
```bash
# Check port availability
lsof -i :8000  # Linux/Mac
netstat -an | findstr :8000  # Windows

# Try different port
uv run python app/web_interface.py --port 8080
```

#### Discovery tools return empty results
```bash
# Check internet connection
curl -I https://www.google.com

# Try with different topics
revamp analyze --topic "python"  # More general
revamp analyze --topic "machine learning"  # More specific
```

### Getting Help

1. **Built-in Help**
   ```bash
   revamp --help
   revamp analyze --help
   revamp generate --help
   ```

2. **Examples**
   ```bash
   revamp examples
   ```

3. **Setup Issues**
   ```bash
   revamp setup  # Re-run setup wizard
   ```

4. **Community**
   - GitHub Issues: Report bugs
   - GitHub Discussions: Ask questions
   - Discord: Real-time help (coming soon)

## 🎉 Success Tips

### For Best Results:
1. **Use specific topics** in discovery mode ("React TypeScript" vs "web development")
2. **Provide context** when possible (hackathon themes, requirements)
3. **Fork repositories** before implementing changes (`--fork` flag)
4. **Start small** - try analysis before implementation
5. **Read the strategy** before implementing to understand changes

### Popular Topics That Work Well:
- **AI/ML**: "artificial intelligence", "machine learning", "computer vision"
- **Web3**: "blockchain", "DeFi", "smart contracts", "NFT"
- **Climate**: "sustainability", "carbon tracking", "renewable energy"
- **Health**: "healthcare", "medical AI", "telemedicine"
- **Fintech**: "payments", "banking", "financial services"
- **IoT**: "internet of things", "sensors", "smart home"

---

**Ready to transform your next project into a hackathon winner? Pick your preferred method and get started! 🚀**