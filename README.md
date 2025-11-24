# 📧 Gmail AI Agent

This project is an AI-powered email assistant that leverages **LangChain**, **Ollama LLM**, and the **Gmail API** to automatically fetch, analyze, and generate professional replies for Gmail conversations. It combines asynchronous API calls, LLM reasoning, and a tool-based architecture for flexible email management.

---

## 🔹 Features

### 1️⃣ Gmail API Integration
- Securely connects to Gmail using OAuth 2.0.
- Supports fetching emails and threads by `thread_id`.
- Handles message parsing including text and HTML content.
- Organizes emails grouped by conversation threads.

### 2️⃣ MCP Server
- Uses **FastMCP** to create an MCP tool server.
- Provides an asynchronous API for querying Gmail conversations.
- Exposes tools like `get_conversation` to fetch formatted email threads.

### 3️⃣ AI Agent
- Uses **OllamaLLM** with `qwen3:1.7b` model.
- Integrates with LangChain's `zero-shot-react-description` agent.
- Automatically generates professional replies for the last email in a thread.
- Supports additional tools for future extensions.





