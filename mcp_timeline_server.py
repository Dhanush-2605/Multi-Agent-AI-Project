# The In-Memory Knowledge Graph
sacred_timeline_graph = {
    "Thanos": [
        {"relation": "sacrificed", "target": "Gamora on Vormir"},
        {"relation": "snapped", "target": "Half of all life in 2018"}
    ],
    "Time Stone": [
        {"relation": "housed_in", "target": "Eye of Agamotto"},
        {"relation": "rule", "target": "Careless use creates temporal paradoxes."}
    ]
}

def query_timeline_graph(entity: str) -> str:
    """Queries the local TVA database for an entity."""
    entity_data = sacred_timeline_graph.get(entity)
    
    if not entity_data:
        return f"DATABASE MISS: No canon data found for '{entity}'."

    result = f"Canon Data for [{entity}]:\n"
    for edge in entity_data:
        result += f"- {entity} --({edge['relation']})--> {edge['target']}\n"
    return result

def update_timeline_graph(entity: str, relation: str, target: str) -> str:
    """Updates the database with new facts found on the web."""
    if entity not in sacred_timeline_graph:
        sacred_timeline_graph[entity] = []
        
    new_edge = {"relation": relation, "target": target}
    
    if new_edge not in sacred_timeline_graph[entity]:
        sacred_timeline_graph[entity].append(new_edge)
        return f"✅ VAULT UPDATED: [{entity}] --({relation})--> [{target}]"
    else:
        return "Fact already exists in the Vault."