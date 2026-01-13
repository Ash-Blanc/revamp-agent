# Revamp Agent

> *"In the vast expanse of open-source code, greatness often lies dormant, waiting for a vision to awaken it."*

**The Revamp Agent is your digital charioteer—an AI-powered architect designed to navigate the chaotic battlefield of hackathons and steer existing projects toward victory.**

By harnessing the wisdom of advanced Large Language Models (LLMs) and the orchestrating power of the Agno framework, this agent does not merely analyze code; it perceives potential. It studies the landscape of competition, forges a master strategy, and can even take up the hammer to rebuild the codebase itself.

---

## 📜 The Saga (Project Overview)

The journey from a static repository to a winning hackathon submission is fraught with uncertainty. The **Revamp Agent** was forged to bridge this divide. It acts as a bridge between *what is*—your existing open-source software—and *what could be*—a novel, judge-pleasing innovation.

Through a symphony of specialized sub-agents, it performs a deep semantic reading of your code, simultaneously casting its gaze across the web to understand the pulse of current hackathons. It aligns technical reality with market desire, ensuring your project is not just functional, but destined for the podium.

### The Three Pillars of Transformation
*   **The Eye of Insight (Analysis)**: It peers into the depths of your repository, understanding structure, dependencies, and hidden patterns.
*   **The Mind of Strategy (Research)**: It traverses the digital realm, scraping hackathon criteria to uncover exactly what judges seek.
*   **The Hand of Creation (Implementation)**: It possesses the capability to weave new code, crafting patches and features to bring the strategy to life.

---

## 🔮 The Arsenal (Features)

*   **Prophetic Strategy Generation**: Delivers more than a report—it provides a battle plan. Expect detailed strategic positioning, novel feature concepts, and a roadmap for technical dominance.
*   **Council of Agents**: Orchestrated by the **Agno framework**, specialized agents (The Researcher, The Strategist, The Coder) collaborate in harmony to solve complex problems.
*   **Tools of Power**:
    *   **GitHub Integration**: To read the history of your code and inscribe its future.
    *   **Firecrawl**: To gather intelligence from the farthest reaches of the web.
    *   **LangWatch**: To maintain clarity and memory across the agent's thoughts.
*   **Dual Paths of Action**:
    *   **The Path of Wisdom (Analysis Mode)**: Receive a comprehensive strategy without altering a single line of code.
    *   **The Path of Action (Implementation Mode)**: Empower the agent to fork your repo and forge the changes directly.

---

## 🏛️ The Foundation (Tech Stack)

Built upon modern pillars of technology:

*   **The Core**: Python 3.13+
*   **The Framework**: [Agno](https://docs.agno.com/) (The Orchestrator)
*   **The Intellect**: OpenAI GPT-4o (Strategy), Cerebras/Mistral (Coding)
*   **The Tools**:
    *   **`uv`**: For swift and precise dependency management.
    *   **Firecrawl**: For relentless information gathering.
    *   **Scenario**: To simulate and test the agent's foresight.

---

## ⚡ The Ritual (Installation)

To summon the agent, one must first prepare the environment.

### The Guided Invocation (Recommended)
Let the wizard guide you through the setup, weaving the necessary spells (dependencies) and keys automatically.

```bash
python setup_wizard.py
```

### The Manual Rite
For those who prefer to shape their own destiny:

1.  **Claim the Repository:**
    ```bash
    git clone https://github.com/your-org/revamp.git
    cd revamp
    ```

2.  **Gather Supplies:**
    ```bash
    uv sync
    ```

3.  **Grant Permissions (Configuration):**
    inscribe your API keys into the sacred `.env` file.
    ```bash
    cp .env.example .env
    ```

---

## 🎮 The Command (Usage)

The agent awaits your instruction through multiple interfaces.

### 1. The Command Line (CLI)
*Direct communion with the core.*

**To seek a strategy for a specific battle:**
```bash
uv run revamp analyze --github https://github.com/user/repo --hackathon https://hackathon-url.com
```

**To discover new battlegrounds (Discovery Mode):**
```bash
uv run revamp analyze --topic "Generative AI"
```

**To authorize full transformation (Fork & Code):**
```bash
uv run revamp generate --github https://github.com/user/repo --hackathon https://hackathon-url.com --fork
```

### 2. The Web Interface
*A visual portal for the visionary.*

```bash
uv run revamp web
```
Open the portal at `http://localhost:8000`.

### 3. The Python API
*Weave the agent's power into your own creations.*

```python
from app.main import revamp_project

# Summon the strategy
result = revamp_project(
    github_url="https://github.com/user/repo",
    hackathon_url="https://hackathon-url.com"
)
print(result.strategy)
```

---

## 🤝 The Gathering (Contributing)

We invite all architects and visionaries to contribute. This project adheres to the **Better Agents** standard.

*   **The Law of Prompts**: Do not hardcode the agent's thoughts. Use `langwatch` CLI to manage prompts in `prompts/`.
*   **The Law of Testing**: Every new power must be proven. Write Scenario tests in `tests/scenarios/`.
*   **The Law of Order**: Use `uv` to keep our dependencies in harmony.

To verify the integrity of the build:
```bash
uv run pytest
```

---

## 📜 License

[License Information] - The code is free, but the wisdom is earned.

---

**"Go forth, and let your code tell a new story."**

---

## 📚 Chronicles (Resources)

*   [The Usage Guide](USAGE_GUIDE.md)
*   [The Developer's Codex (AGENTS.md)](AGENTS.md)
*   [Refactoring Summary](REFACTORING_SUMMARY.md)
*   [Agno Framework Documentation](https://docs.agno.com/)
