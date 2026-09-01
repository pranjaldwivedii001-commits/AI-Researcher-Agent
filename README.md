# AI-Researcher-Agent
A search agent that finds sources, a reader agent scrapes the best one, and a writer agent drafts a report on a requested topic.

An autonomous research assistant powered by **LangChain**, **LangGraph**, and **Mistral AI**. This application takes a research topic or query, performs web searches, scrapes relevant content, and synthesizes a comprehensive report directly through an interactive **Streamlit** web interface.

## Key Features

* **Autonomous Agent Workflow:** Built using LangGraph to orchestrate multi-step research and writing processes.
* **Web Search Integration:** Dynamically fetches up-to-date information from the web using search tools.
* **Web Scraping:** Extracts and parses raw content from target web pages using BeautifulSoup.
* **AI-Powered Synthesis:** Generates structured, detailed markdown research reports utilizing Mistral AI's chat models.
* **Interactive UI:** A clean, user-friendly frontend built with Streamlit.

---

## Project Structure

```text
AI-Researcher-Agent/
├── agents.py         # Defines search agents, scrape agents, and writer chains
├── app.py            # Streamlit web application interface
├── pipeline.py       # Orchestrates the execution flow between agents
├── tools.py          # Custom tools for web search and scraping
├── pyproject.toml    # Project metadata and dependencies configuration
├── uv.lock           # Dependency lock file
└── README.md         # Project documentation

