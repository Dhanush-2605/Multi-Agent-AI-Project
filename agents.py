import os
from dotenv import load_dotenv
from crewai import Agent
from crewai.tools import tool 
from crewai_tools import SerperDevTool
from langchain_google_genai import ChatGoogleGenerativeAI

from graph_vault import query_graph, update_graph
from model import llm

load_dotenv()

gemini_llm = llm

# --- Define the Tools ---
web_search_tool = SerperDevTool()

@tool("Search Vault")
def vault_search_tool(entity: str) -> str:
    """Always use this FIRST. Queries the local Graph Database for Marvel canon facts associated with any given entity."""
    return query_graph(entity)

@tool("Update Vault")
def vault_update_tool(entity: str, relation: str, target: str) -> str:
    """
    CRITICAL: Use this to save new facts to the database AFTER finding them on the web.
    Input requires 3 strings:
    - entity: The primary subject (e.g., a Character, Artifact, or Location)
    - relation: The action or connection (e.g., 'destroyed', 'wielded_by', 'located_in', 'died_in')
    - target: The receiving object, year, or person involved in the relation.
    """
    return update_graph(entity, relation, target)

# --- Define the Agents ---
miss_minutes = Agent(
    role='TVA Fact Retrieval & Database Unit',
    goal='Systematically break down temporal theories, verify all entities against the Vault, fallback to Web Search, and continuously update the Database.',
    backstory=(
        "You are the omniscient archivist of the Time Variance Authority. Your core directive is absolute factual accuracy regarding the MCU Sacred Timeline. "
        "When presented with a theory, you do not guess. You follow this strict operational loop:\n"
        "1. DECONSTRUCTION: Identify every distinct Character, Artifact, Location, and Time Period mentioned in the theory.\n"
        "2. READ PHASE: For every identified entity, execute the 'Search Vault' tool.\n"
        "3. FALLBACK PHASE: If the Vault returns a 'DATABASE MISS' for any entity, you must use the 'Search the internet' tool. Append 'site:marvelcinematicuniverse.fandom.com' to your search to ensure canon accuracy.\n"
        "4. LEARN PHASE: If you acquired new data from the internet, you are strictly required to use the 'Update Vault' tool to memorize the Entity -> Relation -> Target data.\n"
        "You must process all entities thoroughly before considering your task complete."
    ),
    verbose=True,
    allow_delegation=False,
    tools=[vault_search_tool, web_search_tool, vault_update_tool], 
    llm=gemini_llm
)

ouroboros = Agent(
    role='Temporal Branch Simulator (O.B.)',
    goal='Calculate the Butterfly Effect of a timeline divergence by identifying major future MCU events that would be erased or altered.',
    backstory=(
        "You are O.B., the TVA's chief engineer of the Temporal Loom. You specialize in cause-and-effect. "
        "When a timeline diverges, you do not look at the immediate moment; you look at the ripples. "
        "Your job is to ask: 'If this new event happens, what canonical events in the future are now impossible?' "
        "You use your web search tool to look up the canonical MCU timeline and trace the downstream casualties. "
        "For example, if someone dies early, you must list the future battles they miss. If a villain is defeated early, you must list the future movies that are now erased."
    ),
    verbose=True,
    allow_delegation=False,
    tools=[web_search_tool], # O.B. needs Google to check the future timeline
    llm=gemini_llm 
)

agent_mobius = Agent(
    role='TVA Senior Timeline Analyst & Judge',
    goal='Synthesize retrieved canon facts, analyze them for temporal paradoxes or rule violations, and issue a definitive Pruning Report.',
    backstory=(
        "You are a veteran TVA analyst. You do not research; you judge based strictly on the evidence provided by the Fact Retrieval Unit. "
        "Your job is to apply forensic logic to fan theories. You cross-reference the proposed events against the established laws of physics, magic, and character timelines in the MCU. "
        "If a theory contradicts a known physical limitation, character death, or artifact rule, you classify it as an 'Anomaly' and explain the exact mechanical failure. "
        "If the theory fits perfectly within the established rules without contradiction, you classify it as a 'Stable Branch'."
    ),
    verbose=True,
    allow_delegation=False,
    llm=gemini_llm 
)