import os
import json
import networkx as nx
from networkx.readwrite import json_graph

# The file where our database will live
VAULT_FILE = "tva_database.json"

def load_vault() -> nx.DiGraph:
    """Loads the graph from the hard drive, or creates a new one if it doesn't exist."""
    if os.path.exists(VAULT_FILE):
        # Load existing data
        with open(VAULT_FILE, "r") as file:
            data = json.load(file)
            return json_graph.node_link_graph(data, directed=True)
    else:
        # Create a new graph and add the seed data
        g = nx.DiGraph()
        g.add_edge("Thanos", "Gamora", relation="sacrificed on Vormir")
        g.add_edge("Time Stone", "Eye of Agamotto", relation="housed in")
        return g

def save_vault(graph: nx.DiGraph):
    """Saves the current graph to the hard drive."""
    data = json_graph.node_link_data(graph)
    with open(VAULT_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Initialize the graph by loading it from disk!
sacred_timeline = load_vault()

# (To ensure our initial seed data gets saved immediately if this is the first run)
if not os.path.exists(VAULT_FILE):
    save_vault(sacred_timeline)

def query_graph(entity: str) -> str:
    """Queries the NetworkX graph for an entity's relationships."""
    if not sacred_timeline.has_node(entity):
        return f"DATABASE MISS: No canon data found for '{entity}'."

    result = f"Canon Data for [{entity}]:\n"
    
    # Get outgoing relationships
    for _, target, data in sacred_timeline.out_edges(entity, data=True):
        result += f"- {entity} --({data['relation']})--> {target}\n"
        
    # Get incoming relationships
    for source, _, data in sacred_timeline.in_edges(entity, data=True):
        result += f"- {source} --({data['relation']})--> {entity}\n"

    if result == f"Canon Data for [{entity}]:\n":
         return f"Entity '{entity}' exists in database, but has no recorded relationships."
         
    return result

def update_graph(entity: str, relation: str, target: str) -> str:
    """Adds a new node and edge to the graph AND saves it to disk."""
    sacred_timeline.add_edge(entity, target, relation=relation)
    
    # CRITICAL: Save to the hard drive immediately after updating!
    save_vault(sacred_timeline)
    
    return f"✅ VAULT UPDATED & SAVED TO DISK: [{entity}] --({relation})--> [{target}]"

def get_all_vault_data() -> str:
    """Returns a fully formatted string of every entity and relationship currently in the graph."""
    if sacred_timeline.number_of_nodes() == 0:
        return "The Vault is currently empty."

    output = "🌌 CURRENT TVA VAULT STATUS 🌌\n"
    output += "="*40 + "\n"

    output += "Recorded Entities:\n"
    for node in sacred_timeline.nodes():
        output += f"  • {node}\n"

    output += "\nEstablished Lore (Relationships):\n"
    for source, target, data in sacred_timeline.edges(data=True):
        relation = data.get('relation', 'connected_to')
        output += f"  • [{source}] --({relation})--> [{target}]\n"

    output += "="*40
    return output

# --- RUN THIS FILE DIRECTLY TO TEST ---
if __name__ == "__main__":
    print(get_all_vault_data())