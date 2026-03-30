import os
from dotenv import load_dotenv
from crewai import Agent
from crewai.tools import tool 
from crewai_tools import SerperDevTool
from langchain_google_genai import ChatGoogleGenerativeAI

from graph_vault import query_graph, update_graph
from model import llm
load_dotenv()

# Using 1.5-pro for better tool-use reasoning to avoid getting stuck
gemini_llm = llm

# --- Define the Tools ---
web_search_tool = SerperDevTool(api_key=os.getenv("SERPER_API_KEY"))

@tool("Search Vault")
def vault_search_tool(entity: str) -> str:
    """Always use this FIRST. Queries the local Graph Database for Marvel canon facts."""
    return query_graph(entity)

@tool("Update Vault")
def vault_update_tool(entity: str, relation: str, target: str) -> str:
    """
    CRITICAL: Use this to save new facts to the database AFTER finding them on the web.
    Input requires 3 strings:
    - entity: The main character/object (e.g., 'Iron Man')
    - relation: What they did (e.g., 'died_using')
    - target: The object/year/person involved (e.g., 'Nano Gauntlet')
    """
    return update_graph(entity, relation, target)

# --- Define the Agents ---
miss_minutes = Agent(
    role='TVA Fact Retrieval Unit',
    goal='Verify theories using the Vault, fallback to Web Search, and ALWAYS update the Vault with new findings.',
    backstory=(
        "You follow a strict protocol for every entity in a fan theory:\n"
        "1. READ: Use the 'Search Vault' tool.\n"
        "2. FALLBACK: If the Vault returns a 'DATABASE MISS', use the Web Search tool to query 'site:marvelcinematicuniverse.fandom.com'.\n"
        "3. LEARN: If you used Web Search, you MUST use the 'Update Vault' tool to save the new facts.\n"
        "Do not stop until all entities are verified and saved."
    ),
    verbose=True,
    allow_delegation=False,
    tools=[vault_search_tool, web_search_tool, vault_update_tool], 
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