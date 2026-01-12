# Hackathon Project Revamp Agent - Context

## Project Overview
This project implements an AI agent designed to transform open-source GitHub projects into hackathon-winning solutions. It analyzes codebases, researches hackathon criteria, scrapes hackathon websites, and generates comprehensive revamp strategies, including optional code implementation.

## Tech Stack
- **Language**: Python 3.13+
- **Framework**: [Agno](https://docs.agno.com/) (AI agent framework)
- **Package Manager**: `uv`
- **LLMs**: OpenAI GPT-4o (Strategy), Cerebras/Mistral/OpenRouter (Coding)
- **Tools**:
  - **Firecrawl**: Web scraping for hackathon details.
  - **MorphTools**: AI-powered code editing.
  - **LangWatch**: Prompt management and observability.
  - **Scenario**: End-to-end agent testing.

## Project Structure
```
revamp/
├── app/                    # Application source code
│   ├── main.py             # Entry point
│   ├── cli.py              # CLI interface
│   ├── coding_agent.py     # Implementation logic
│   └── ...
├── prompts/                # Managed prompts (YAML format)
│   └── *.yaml
├── tests/
│   ├── scenarios/          # End-to-end scenario tests
│   └── evaluations/        # Jupyter notebooks for eval
├── AGENTS.md               # Development guidelines (CRITICAL)
├── pyproject.toml          # Dependencies and config
└── README.md               # Project documentation
```

## Key Commands

### Running the Agent
```bash
# Run the main script
uv run python app/main.py

# Run as module
uv run python -m app.main
```

### Testing
```bash
# Run all tests
uv run pytest

# Run scenario tests (end-to-end)
uv run pytest tests/scenarios/
```

### Dependency Management
**Always use `uv`.**
```bash
# Install dependencies
uv sync

# Add a dependency
uv add <package_name>

# Add a dev dependency
uv add --dev <package_name>
```

### Prompt Management
Prompts are managed via LangWatch CLI and stored in `prompts/`. **Do not hardcode prompts.**
```bash
# Create a new prompt
uv run langwatch prompt create <prompt_name>

# Sync prompts after editing YAML files
uv run langwatch prompt sync

# List prompts
uv run langwatch prompt list
```

## Development Guidelines (from AGENTS.md)
1.  **Scenario Testing**: Every new feature MUST be tested with Scenario tests (`tests/scenarios/`).
2.  **Prompt Management**: Use `langwatch` CLI. Fetch prompts in code via `langwatch.prompts.get()`.
3.  **Agno Framework**: Follow Agno best practices (reuse agents, use structured output).
4.  **Environment**: Ensure `.env` is configured with necessary API keys (OpenAI, LangWatch, Firecrawl, GitHub, etc.).

## Configuration
See `.env.example` for required environment variables. Key variables include:
- `OPENAI_API_KEY`
- `LANGWATCH_API_KEY`
- `FIRECRAWL_API_KEY`
- `GITHUB_ACCESS_TOKEN`
