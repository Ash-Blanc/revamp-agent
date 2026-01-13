# Revamp Agent

**An AI-powered autonomous agent for strategically enhancing open-source projects.**

Revamp Agent utilizes advanced Large Language Models (LLMs) and the Agno framework to analyze GitHub repositories, research hackathon criteria, and generate comprehensive modernization strategies. It automates the process of code analysis, strategic planning, and implementation, enabling developers to transform existing codebases into competitive, hackathon-ready solutions.

---

## 📋 Project Overview

The **Revamp Agent** is designed to bridge the gap between existing open-source software and the specific, often novel requirements of hackathons. By leveraging a multi-agent architecture, it performs deep semantic analysis of codebases and correlates findings with real-time web research on hackathon themes and judging criteria.

### Core Capabilities
*   **Automated Codebase Analysis**: Deep inspection of repository structure, dependencies, and code patterns.
*   **Strategic Market Research**: Real-time scraping and analysis of hackathon websites to identify winning trends and criteria.
*   **Autonomous Implementation**: Optional capability to generate and apply code patches, new features, and documentation updates directly to the repository.
*   **Multi-Modal Interfaces**: Accessible via Command Line Interface (CLI), Web UI, and Python API.

---

## ✨ Features

*   **Intelligent Strategy Generation**: Produces detailed reports covering strategic positioning, novel feature suggestions, and technical improvements.
*   **Multi-Agent Orchestration**: Utilizes specialized agents for research, strategy, and coding tasks, orchestrated by the Agno framework.
*   **Seamless Integration**:
    *   **GitHub**: Direct integration for reading repositories and creating pull requests.
    *   **Firecrawl**: Robust web scraping for gathering hackathon intelligence.
    *   **LangWatch**: Enterprise-grade prompt management and observability.
*   **Dual Operation Modes**:
    *   **Analysis Mode**: Generates strategic reports without modifying code.
    *   **Implementation Mode**: Applies changes directly via forking or branching.
*   **Developer-First Tooling**: Includes a comprehensive CLI, a modern Web UI, and a simplified setup wizard.

---

## 🛠️ Technology Stack

*   **Language**: Python 3.13+
*   **Agent Framework**: [Agno](https://docs.agno.com/)
*   **Package Management**: `uv`
*   **LLMs**: OpenAI GPT-4o (Strategy), Cerebras/Mistral (Coding)
*   **Infrastructure**:
    *   **Firecrawl**: Web scraping and content extraction.
    *   **LangWatch**: Prompt engineering, management, and testing.
    *   **Scenario**: End-to-end agent behavior testing.

---

## ⚙️ Installation

### Prerequisites
*   Python 3.13 or higher
*   Git
*   [uv](https://github.com/astral-sh/uv) (Recommended package manager)

### Automated Setup (Recommended)
The included setup wizard handles dependency installation, environment configuration, and verification.

```bash
python setup_wizard.py
```

### Manual Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-org/revamp.git
    cd revamp
    ```

2.  **Install dependencies using `uv`:**
    ```bash
    uv sync
    ```

3.  **Configure environment variables:**
    Copy the example configuration and update it with your API keys.
    ```bash
    cp .env.example .env
    ```
    *See the [Configuration](#-configuration) section for required keys.*

---

## 🚀 Usage

Revamp Agent offers multiple interfaces to suit different workflows.

### 1. Command Line Interface (CLI)

**Analyze a project for a specific hackathon:**
```bash
uv run revamp analyze --github https://github.com/user/repo --hackathon https://hackathon-url.com
```

**Discovery Mode (Find relevant hackathons):**
```bash
uv run revamp analyze --topic "Generative AI"
```

**Full Implementation (Fork and Apply Changes):**
```bash
uv run revamp generate --github https://github.com/user/repo --hackathon https://hackathon-url.com --fork
```

**Start Interactive Mode:**
```bash
uv run revamp interactive
```

### 2. Web Interface

Launch the local web server to interact with the agent via a graphical interface.

```bash
uv run revamp web
```
Access the interface at `http://localhost:8000`.

### 3. Python API

Integrate Revamp Agent into your own Python applications.

```python
from app.main import revamp_project

result = revamp_project(
    github_url="https://github.com/user/repo",
    hackathon_url="https://hackathon-url.com"
)
print(result.strategy)
```

---

## 🔧 Configuration

The application requires several API keys to function fully. Configure these in your `.env` file.

| Variable | Description | Required |
|----------|-------------|:--------:|
| `OPENAI_API_KEY` | Core LLM reasoning (GPT-4o). | Yes |
| `LANGWATCH_API_KEY` | Prompt management and observability. | Yes |
| `FIRECRAWL_API_KEY` | Web scraping for hackathon research. | Optional |
| `GITHUB_ACCESS_TOKEN` | Repository access for implementation mode. | Optional |
| `CEREBRAS_API_KEY` | High-speed inference for coding tasks. | Optional |

---

## 🏗️ Project Structure

```
revamp/
├── app/
│   ├── agents/            # Specialized agent implementations
│   ├── core/              # Core framework components
│   ├── teams/             # Multi-agent coordination logic
│   ├── tools/             # External tool integrations (GitHub, Firecrawl)
│   ├── workflows/         # End-to-end execution flows
│   ├── main.py            # Application entry point
│   └── cli.py             # CLI command definitions
├── prompts/               # Managed YAML prompts (synced via LangWatch)
├── tests/
│   ├── scenarios/         # End-to-end behavioral tests
│   └── evaluations/       # Component performance evaluations
├── AGENTS.md              # Development standards and guidelines
└── pyproject.toml         # Project dependencies and metadata
```

---

## 🤝 Contributing

We welcome contributions! This project adheres to the **Better Agents** standard. Please ensure you follow these guidelines:

1.  **Prompt Management**: Do not hardcode prompts. Use the `langwatch` CLI to manage prompts in the `prompts/` directory.
2.  **Testing**:
    *   **Scenario Tests**: Every new feature must include end-to-end tests in `tests/scenarios/`.
    *   **Evaluations**: Use Jupyter notebooks in `tests/evaluations/` for component metrics.
3.  **Dependencies**: Use `uv` for all dependency management (`uv add`, `uv sync`).

To run tests:
```bash
uv run pytest
```

---

## 📄 License

[License Information] - Please refer to the repository for license details.

---

## 📚 Resources

*   [Usage Guide](USAGE_GUIDE.md)
*   [Development Guidelines](AGENTS.md)
*   [Refactoring Summary](REFACTORING_SUMMARY.md)
*   [Agno Framework Documentation](https://docs.agno.com/)