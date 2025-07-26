"""
run_plan.py
Continuously builds a micro-SaaS business plan until it is finished,
regardless of token / iteration limits.
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Any

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.tools import Tool
from langchain_community.tools.tavily_search import TavilySearchResults

# --------------------------------------------------
# 1.  ENVIRONMENT & LLM
# --------------------------------------------------
load_dotenv()

llm = ChatGroq(
    model="llama3-70b-8192",
    temperature=0.7,
)

# --------------------------------------------------
# 2.  TOOLS
# --------------------------------------------------
tavily_tool = TavilySearchResults(max_results=5)

tools = [
    Tool(
        name="InternetSearch",
        func=tavily_tool.run,
        description="Use this to search the internet for information, such as frequent problems people face."
    )
]

# --------------------------------------------------
# 3.  PROMPT (unchanged from your original)
# --------------------------------------------------
prompt_template = PromptTemplate.from_template(
    """
    You are an AI agent tasked with following this instruction precisely:
    "make a business plan for micre saas serch for frequently problems from the interrnet and follw thise instruction to identify the problem Design a solution, system, or message that is:

    Built from atomic-level identity-based habits,

    Validated rapidly through Build-Measure-Learn feedback loops,

    Focused on scalable, controllable value (not time-for-money),

    Optimized with high-leverage mental models and routines of top performers,

    Protected from bias and impulsivity through slow thinking and discipline,

    Balanced against dopamine-driven distraction by designing for delayed gratification,

    And communicated using sticky, memorable ideas (Simple, Unexpected, Concrete, Credible, Emotional, Story-based).

    Ensure it compounds, adapts fast, scales wide, and sticks deep."

    Available tools: {tools}
    Tool names: {tool_names}

    Use your tools to search the internet for frequent problems, identify one suitable for a micro SaaS, design a solution following the criteria, and output a complete business plan.

    Begin!

    {agent_scratchpad}
    """
)

# --------------------------------------------------
# 4.  AGENT + EXECUTOR
# --------------------------------------------------
agent = create_react_agent(llm, tools, prompt_template)

# We keep max_iterations low so we can checkpoint often.
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=5,          # small chunk ⇒ quick restart
    handle_parsing_errors=True
)

# --------------------------------------------------
# 5.  STATE MANAGEMENT
# --------------------------------------------------
REPORT_FILE = Path("micro_saas_plan.md")

def load_previous() -> str:
    """Return everything written so far."""
    if REPORT_FILE.exists():
        return REPORT_FILE.read_text(encoding="utf-8")
    return ""

def append_chunk(text: str) -> None:
    """Append the latest chunk to the report."""
    with REPORT_FILE.open("a", encoding="utf-8") as f:
        f.write("\n" + text)

# --------------------------------------------------
# 6.  MAIN LOOP
# --------------------------------------------------
def run_until_complete() -> None:
    previous = load_previous()

    # Initial prompt if file is empty.
    if not previous.strip():
        previous = "# Micro-SaaS Business Plan\n\n"
        append_chunk(previous)

    # Build scratchpad from previous output so the agent sees what it wrote.
    scratchpad = previous

    while True:
        print("\n[CONTINUING] Resuming with scratchpad length:",
              len(scratchpad))

        response: Dict[str, Any] = agent_executor.invoke(
            {"input": scratchpad}   # feed prior text as context
        )

        new_text = response.get("output", "")

        # Simple heuristic: if the agent explicitly says "FINISHED" or
        # we have written > 10 000 tokens, we stop.
        finished = (
            "FINISHED" in new_text.upper()
            or len(new_text) < 50   # very short ⇒ probably stuck
        )

        append_chunk(new_text)
        scratchpad += new_text

        if finished:
            print("\n[DONE] Plan appears complete.")
            break

        print("\n[LOOP] Checkpoint saved. Restarting agent...\n")

# --------------------------------------------------
# 7.  FIRE IT UP
# --------------------------------------------------
if __name__ == "__main__":
    run_until_complete()