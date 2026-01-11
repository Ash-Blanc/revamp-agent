# Hackathon Project Revamp Agent

An AI agent that transforms open-source GitHub projects into hackathon-winning solutions through strategic analysis, research, and innovation.

## Overview

This agent specializes in:
- **Analyzing GitHub Projects**: Deep examination of repository structure, codebase, features, and technical stack
- **Scraping Hackathon Websites**: Using Firecrawl to extract themes, judging criteria, requirements, and deadlines from hackathon websites
- **Researching Hackathon Context**: Understanding hackathon themes, judging criteria, and current trends
- **Developing Winning Strategies**: Creating innovative revamp plans with novelty and strategic positioning
- **Providing Actionable Plans**: Comprehensive strategies with features, improvements, and presentation recommendations
- **Implementing Code Changes**: Using a coding agent to actually make code changes, fork repositories, and create branches

## Features

- 🤖 AI-powered project analysis and strategy development
- 🕷️ Web scraping of hackathon websites using Firecrawl
- 🔍 Automatic discovery of ongoing hackathons and relevant GitHub projects
- 🎯 Smart matching between projects and hackathons
- 🔄 Flexible search order (projects-first or hackathons-first)
- 💡 Novel feature proposals aligned with hackathon goals
- 📊 Comprehensive revamp plans with actionable steps
- 🎯 Strategic differentiation tactics
- 💻 **Coding Agent**: Automatically implement revamp strategies with code changes
- 🧬 **MorphTools Integration**: AI-powered code editing with Morph's Fast Apply API
- 🍴 **Repository Forking**: Fork repositories before making changes
- 🌿 **Branch Management**: Create branches and make commits via GitHub API

## Tech Stack

- **Framework**: [Agno](https://docs.agno.com/) - Production-ready AI agent framework
- **Language**: Python 3.13+
- **LLM Models**:
  - **Strategy Agent**: OpenAI GPT-4o
  - **Coding Agent**: Cerebras (primary), Mistral/OpenRouter (fallbacks)
- **Web Scraping**: Firecrawl for extracting hackathon website information
- **Search**: DuckDuckGo for research
- **Code Editing**: MorphTools for AI-powered, precise code editing
- **Monitoring**: LangWatch for prompt management and observability
- **Testing**: Scenario for end-to-end agent testing
- **Package Manager**: uv

## Prerequisites

- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- OpenAI API key
- LangWatch API key
- Firecrawl API key (for web scraping hackathon websites)
- GitHub Access Token (for coding agent and repository operations)
- Morph API key (for AI-powered code editing - optional but recommended)
- **Coding Agent Model Providers** (at least one required):
  - **Cerebras API key** (primary, recommended)
  - **Mistral API key** (fallback 1)
  - **OpenRouter API key** (fallback 2)
  - If none are provided, falls back to OpenAI

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd revamp
   ```

2. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys:
   # - OPENAI_API_KEY (or set via environment)
   # - LANGWATCH_API_KEY
   # - FIRECRAWL_API_KEY (for web scraping hackathon websites)
   # - GITHUB_ACCESS_TOKEN (for coding agent and repository operations)
   # - MORPH_API_KEY (for AI-powered code editing - optional but recommended)
   # - CEREBRAS_API_KEY (primary coding model - recommended)
   # - MISTRAL_API_KEY (fallback coding model)
   # - OPENROUTER_API_KEY (fallback coding model)
   ```

4. **Install dependencies**:
   ```bash
   uv sync
   ```

5. **Install Scenario** (for testing):
   ```bash
   # Note: Scenario may require additional system dependencies
   # If installation fails, you may need to install build tools:
   # - cmake
   # - ninja
   # - C++ compiler
   uv add scenario
   # Or try: pip install scenario
   ```

## Usage

### Basic Usage

```python
from app.main import revamp_project

# Option 1: With GitHub repo and hackathon URL (recommended)
result = revamp_project(
    github_url="https://github.com/user/repo",
    hackathon_url="https://hackathon-website.com",
    hackathon_context="Additional context if needed"
)

# Option 2: Just analyze a hackathon website
result = revamp_project(
    hackathon_url="https://hackathon-website.com"
)

# Option 3: GitHub repo with manual context
result = revamp_project(
    github_url="https://github.com/user/repo",
    hackathon_context="AI/ML hackathon focusing on innovation and social impact"
)

# Option 4: Auto-discover hackathons for a project
result = revamp_project(
    github_url="https://github.com/user/repo",
    search_topic="AI"  # Optional: guide the search
)

# Option 5: Auto-discover both projects and hackathons (projects first)
result = revamp_project(
    search_order="projects_first",  # or "hackathons_first"
    search_topic="web3"  # Optional: guide the search
)

# Option 6: Auto-discover hackathons first, then find projects
result = revamp_project(
    search_order="hackathons_first",
    search_topic="sustainability"
)

# Option 7: Strategy + Implementation (complete workflow)
from app.main import revamp_and_implement

result = revamp_and_implement(
    github_url="https://github.com/user/repo",
    hackathon_url="https://hackathon-website.com",
    implement_changes=True,  # Enable coding agent
    fork_repo=True,  # Fork before making changes
    branch_name="hackathon-revamp"
)

print(result["strategy"])  # The revamp strategy
print(result["implementation"])  # Summary of code changes made
print(result["repo_name"])  # Repository name used
```

**Notes**:
- The agent will automatically scrape hackathon websites when a `hackathon_url` is provided
- If `hackathon_url` is missing, the agent will use discovery tools to find ongoing hackathons
- If `github_url` is missing, the agent will search for relevant GitHub projects
- If both are missing, the agent will discover both based on `search_order`:
  - `"projects_first"` (default): Find projects first, then matching hackathons
  - `"hackathons_first"`: Find hackathons first, then matching projects
- Use `search_topic` to guide the discovery process (e.g., "AI", "web3", "sustainability")
- Use `revamp_and_implement()` with `implement_changes=True` to automatically implement the strategy
- Set `fork_repo=True` to fork the repository before making changes (recommended)

### Command Line

```bash
# Run the main script
uv run python app/main.py

# Or use as a module
uv run python -m app.main
```

### Development Server with Agno

Agno provides workspace management for running agents. To set up a development workspace:

```bash
# Initialize Agno (first time only)
uv run agno init

# Create a workspace
uv run agno ws create

# Start the workspace (this will start any resources defined in resources.py)
uv run agno ws up

# Or use the start command if you have a resources.py file
uv run agno start
```

Check the Agno documentation for more details on workspace setup and the URL where your agent will be accessible.

## Project Structure

```
revamp/
├── app/                    # Main application code
│   └── main.py            # Agent implementation
├── prompts/               # Versioned prompt files (YAML)
│   └── hackathon_revamp_agent.prompt.yaml
├── tests/
│   ├── evaluations/      # Jupyter notebooks for component evaluation
│   └── scenarios/        # End-to-end scenario tests
│       └── test_hackathon_revamp.py
├── prompts.json          # Prompt registry
├── pyproject.toml        # Project configuration
└── README.md            # This file
```

## Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run scenario tests specifically
uv run pytest tests/scenarios/

# Run with verbose output
uv run pytest -v
```

### Prompt Management

This project uses LangWatch Prompt CLI for managing prompts:

```bash
# Create a new prompt
uv run langwatch prompt create <prompt_name>

# Sync prompts (after editing)
uv run langwatch prompt sync

# List all prompts
uv run langwatch prompt list
```

Prompts are stored in `prompts/` as YAML files and registered in `prompts.json`.

### Adding Dependencies

Always use `uv` to manage dependencies:

```bash
# Add a new dependency
uv add <package_name>

# Add a development dependency
uv add --dev <package_name>
```

## How It Works

1. **Input**: You provide:
   - A GitHub project URL (optional)
   - A hackathon website URL (optional, will be scraped automatically)
   - Additional hackathon context (optional)
   - Search order preference (optional, default: "projects_first")
   - Search topic to guide discovery (optional)

2. **Discovery Mode** (when URLs are missing):
   - **If hackathon URL missing**: Agent uses `find_ongoing_hackathons` to discover relevant hackathons
   - **If GitHub URL missing**: Agent uses `find_relevant_github_projects` to discover projects
   - **If both missing**: Agent follows `search_order`:
     - `"projects_first"`: Finds projects → then finds matching hackathons
     - `"hackathons_first"`: Finds hackathons → then finds matching projects
   - Agent presents discovered options and selects best matches

3. **Web Scraping**: If a hackathon URL is provided (or discovered), the agent uses Firecrawl to scrape the website and extract:
   - Themes and focus areas
   - Judging criteria and evaluation metrics
   - Prizes and categories
   - Deadlines and requirements
   - Specific rules or constraints
   - Sponsor information

4. **Project Analysis**: If a GitHub URL is provided (or discovered), the agent analyzes the project structure, codebase, and features

5. **Research**: The agent researches hackathon trends and winning patterns

6. **Strategy**: The agent develops a comprehensive revamp strategy that aligns the project with hackathon goals

7. **Implementation** (optional): If `implement_changes=True`:
   - Coding agent reads the repository structure
   - Creates a new branch for changes
   - Implements the revamp strategy by making code changes:
     - Uses **MorphTools** for AI-powered, precise code editing (if available)
     - MorphTools handles complex refactoring while preserving code style
     - Falls back to direct GitHub API updates if MorphTools unavailable
   - Creates commits with clear messages
   - Optionally forks the repository first if `fork_repo=True`

8. **Output**: You receive:
   - **Strategy**: Detailed revamp plan with:
     - Discovered projects/hackathons (if discovery mode was used)
     - Project analysis (if GitHub URL provided or discovered)
     - Hackathon analysis (if hackathon URL provided or discovered)
     - Strategic positioning
     - Novel feature proposals
     - Technical improvements
     - Demo recommendations
     - Differentiation tactics
   - **Implementation** (if enabled): Summary of code changes made, branches created, commits

## Example Output

The agent provides comprehensive revamp strategies including:

- **Project Analysis**: Technical stack, architecture, current features
- **Hackathon Research**: Trends, judging criteria, winning patterns
- **Strategic Positioning**: How to position the project for maximum impact
- **Novel Features**: Creative enhancements that differentiate the project
- **Action Plan**: Step-by-step implementation guide
- **Demo Strategy**: How to present the revamped project

## Contributing

This project follows the Better Agents standard. See `AGENTS.md` for detailed development guidelines.

Key principles:
- ✅ Always use LangWatch Prompt CLI for prompts
- ✅ Write Scenario tests for new features
- ✅ Follow the Agent Testing Pyramid
- ✅ Never hardcode prompts in code
- ✅ Use uv for dependency management

## Resources

- [Agno Documentation](https://docs.agno.com/)
- [LangWatch Dashboard](https://app.langwatch.ai/)
- [Scenario Documentation](https://scenario.langwatch.ai/)
- [Agent Testing Pyramid](https://scenario.langwatch.ai/best-practices/the-agent-testing-pyramid)

## License

[Add your license here]

## Support

For issues and questions, please open an issue on GitHub.