import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.tools import Tool
from langchain_community.tools.tavily_search import TavilySearchResults

# Load environment variables from .env file
load_dotenv()

# Set up the LLM (Groq model)
llm = ChatGroq(
    model="llama3-70b-8192",
    temperature=0.7,  # Balanced creativity and determinism
)

# Set up the internet search tool (Tavily)
tavily_tool = TavilySearchResults(max_results=5)

# Define tools for the agent
tools = [
    Tool(
        name="InternetSearch",
        func=tavily_tool.run,
        description="Use this to search the internet for information, such as frequent problems people face."
    )
]

# Define the prompt template with the user's exact instruction
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

# Create the ReAct agent
agent = create_react_agent(llm, tools, prompt_template)

# Create the agent executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=10)

# Run the agent and get the output
response = agent_executor.invoke({"input": ""})  # No additional input needed; prompt has the instruction
output = response['output']

# Function to save output to a file with incremental naming
def save_to_report(content):
    base_filename = "report"
    extension = ".md"
    counter = 0
    filename = f"{base_filename}{extension}"
    
    while os.path.exists(filename):
        counter += 1
        filename = f"{base_filename}{counter}{extension}"
    
    with open(filename, 'w') as f:
        f.write(content)
    print(f"Output saved to {filename}")

# Save the output
save_to_report(output)