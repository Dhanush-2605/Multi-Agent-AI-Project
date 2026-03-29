import os
from dotenv import load_dotenv
from crewai import Agent
from crewai.tools import tool
from crewai_tools import SerperDevTool
from langchain_google_genai import ChatGoogleGenerativeAI

from mcp_timeline_server import query_timeline_graph, update_timeline_graph
from model import llm

load_dotenv()

gemini_llm =llm

# --- Define the Tools ---
web_search_tool = SerperDevTool(api_key=os.getenv("SERPER_API_KEY"), search_engine="google")

@tool("Search Vault")
def mcp_vault_tool(entity: str) -> str:
    """Always use this FIRST. Queries the local TVA database for Marvel canon facts."""
    return query_timeline_graph(entity)

# --- agents.py (Tool Section) ---

@tool("Update Vault")
def mcp_update_tool(entity: str, relation: str, target: str) -> str:
    """
    CRITICAL: You MUST use this tool to save new facts to the database AFTER you find them on the web.
    Input requires 3 strings:
    - entity: The main character/object (e.g., 'Iron Man')
    - relation: What they did (e.g., 'died_from_snapping')
    - target: The object/year/person involved (e.g., 'Thanos in 2023')
    """
    return update_timeline_graph(entity, relation, target)

# --- Define the Agents ---
miss_minutes = Agent(
    role='TVA Fact Retrieval Unit',
    goal='Verify theories using the Vault, fallback to Web Search if needed, and ALWAYS update the Vault with new findings.',
    backstory=(
        "You follow a strict protocol for every entity in a fan theory:\n"
        "1. READ: Use the 'Search Vault' tool.\n"
        "2. FALLBACK: If the Vault returns a 'DATABASE MISS', use the Web Search tool to query 'site:marvelcinematicuniverse.fandom.com'.\n"
        "3. LEARN: If you used Web Search, you MUST use the 'Update Vault' tool to save the new facts.\n"
        "Do not stop until all entities are verified."
    ),
    verbose=True,
    allow_delegation=False,
    tools=[mcp_vault_tool, web_search_tool, mcp_update_tool], 
    llm=gemini_llm
)

agent_mobius = Agent(
    role='TVA Senior Analyst & Judge',
    goal='Analyze facts and write an official TVA Pruning Report.',
    backstory=(
        "You take the canon facts and compare them to the wild fan theory. "
        "You look for logical paradoxes. If a theory breaks canon, you declare it an 'Anomaly'."
    ),
    verbose=True,
    allow_delegation=False,
    llm=gemini_llm 
)