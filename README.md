# langchain_agent 🤖

AI-powered business plan generator using LangChain and Groq LLM. Automatically researches market opportunities and generates detailed business plans using proven frameworks.

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/Hasan393/langchain_agent.git
cd langchain_agent

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp langchain_books/.env.example langchain_books/.env
# Add your API keys to langchain_books/.env:
# GROQ_API_KEY=your_key
# TAVILY_API_KEY=your_key

# Run the agent
cd langchain_books
python main.py  # Recommended: Uses Tavily search
# or
python main2.py  # Alternative: Uses DuckDuckGo (may have issues)
```

## 📋 Features

- Market research using AI and internet search
- Business plan generation with Atomic Habits & Lean Startup principles
- Markdown report output with detailed sections
- Two search options: Tavily (main.py) or DuckDuckGo (main2.py)

## 🛠️ Project Structure

```
langchain_agent/
├── langchain_books/
│   ├── main.py      # Primary agent (recommended)
│   ├── main2.py     # Alternative agent
│   └── .env.example # API configuration
└── requirements.txt # Dependencies
```

## ⚙️ Requirements

- Python 3.8+
- Groq API key
- Tavily API key (for main.py)

## 📝 License

MIT License


<details>
<summary>🚀 Future Goals / Roadmap</summary>

### ✅ Goals

- [ ] 🧠 Streamline agent logic for web or Streamlit deployment
- [ ] 🎨 Design a beautiful and interactive UI (in Streamlit or custom web UI)
- [ ] 🔧 Optimize performance for faster agent response
- [ ] 📦 Package into a shareable tool or web app

</details>
