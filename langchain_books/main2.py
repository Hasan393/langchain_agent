# # agent.py
# """
# LangChain agent that:
# 1. Reads the instruction below and makes decisions.
# 2. Uses the internet (via DuckDuckGo search).
# 3. Follows the atomic-habit / Lean-startup / mental-model playbook.
# 4. Saves output to report.md (report.md1, report.md2 … if already exists).
# 5. Uses Groq via LangChain (ChatGroq).
# 6. Loads all keys from .env via python-dotenv.
# """

# import os
# import re
# from pathlib import Path
# from typing import List

# from dotenv import load_dotenv
# from langchain.agents import AgentExecutor, create_react_agent
# from langchain.tools import Tool
# from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
# from langchain_groq import ChatGroq
# from langchain.prompts import PromptTemplate

# # ------------------------------------------------------------------
# # 0. Load environment variables
# # ------------------------------------------------------------------
# load_dotenv()  # looks for .env in cwd

# # ------------------------------------------------------------------
# # 1. LLM (Groq)
# # ------------------------------------------------------------------
# llm = ChatGroq(
#     model="llama3-8b-8192",  # or any Groq model you prefer
#     temperature=0.2,
#     groq_api_key=os.getenv("GROQ_API_KEY"),
# )

# # ------------------------------------------------------------------
# # 2. Internet search tool (DuckDuckGo)
# # ------------------------------------------------------------------
# search = DuckDuckGoSearchAPIWrapper(max_results=5)

# def search_internet(query: str) -> str:
#     """Return concatenated snippets for the query."""
#     return "\n".join(search.results(query, max_results=5))

# search_tool = Tool(
#     name="internet_search",
#     description="Search the web for up-to-date information.",
#     func=search_internet,
# )

# # ------------------------------------------------------------------
# # 3. Agent prompt
# # ------------------------------------------------------------------
# SYSTEM_PROMPT = """
# You are an expert micro-SaaS strategist.  
# Your ONLY goal is to create a business plan that follows the exact playbook below:

# 1. Search the internet for FREQUENT, PAINFUL problems people are discussing.
# 2. Pick ONE problem that is:
#    - Recurring
#    - Emotionally charged
#    - Not yet elegantly solved
# 3. Design a micro-SaaS solution that is:
#    - Built from atomic-level identity-based habits (tiny repeatable actions that compound).
#    - Validated rapidly through Build-Measure-Learn loops (MVP → metric → pivot).
#    - Focused on scalable, controllable value (subscription, not hourly).
#    - Optimized with high-leverage mental models (Pareto, Eisenhower, Flywheel, etc.).
#    - Protected from bias by forcing slow-thinking checklists and disciplined routines.
#    - Balanced against dopamine distraction by designing for delayed gratification (lock-in, streaks, commitment devices).
#    - Communicated with sticky, memorable ideas (SUCCES: Simple, Unexpected, Concrete, Credible, Emotional, Stories).
# 4. Ensure the plan compounds, adapts fast, scales wide, and sticks deep.

# Output a concise markdown report with these sections:
# - Problem (with evidence snippets)
# - Solution (micro-SaaS idea)
# - Atomic Habit Loop
# - Build-Measure-Learn roadmap
# - Mental models used
# - Anti-bias & delayed-gratification design
# - Sticky messaging (tagline + story)
# - Revenue model & scalability notes

# Do NOT add extra conversational text—only the report.
# """

# prompt = PromptTemplate.from_template(
#     """{system}

# Tools available:
# {tools}
# Tool names: {tool_names}

# Current scratchpad:
# {agent_scratchpad}

# Thought: {thought}
# Action: {action}
# Action Input: {action_input}
# Observation: {observation}
# ... (continue until ready)
# Final Answer: <your markdown report>"""
# )

# # ------------------------------------------------------------------
# # 4. Build ReAct agent
# # ------------------------------------------------------------------
# agent = create_react_agent(
#     llm=llm,
#     tools=[search_tool],
#     prompt=prompt.partial(
#         system=SYSTEM_PROMPT,
#         tools="\n".join([t.name + ": " + t.description for t in [search_tool]]),
#         tool_names=", ".join([t.name for t in [search_tool]])
#     ),
# )
# executor = AgentExecutor(agent=agent, tools=[search_tool], verbose=True, handle_parsing_errors=True)

# # ------------------------------------------------------------------
# # 5. Save helper
# # ------------------------------------------------------------------
# def save_report(markdown: str) -> Path:
#     base = Path("report.md")
#     counter = 0
#     while True:
#         name = base.with_suffix(f".md{counter}" if counter else ".md")
#         if not name.exists():
#             name.write_text(markdown, encoding="utf-8")
#             return name
#         counter += 1

# # ------------------------------------------------------------------
# # 6. Run
# # ------------------------------------------------------------------
# if __name__ == "__main__":
#     result = executor.invoke({"input": "Create the micro-SaaS business plan now."})
#     file_path = save_report(result["output"])
#     print(f"Report saved to {file_path.resolve()}")