from crewai import Task
from agents import miss_minutes, agent_mobius

fan_theory_input = "What if Iron Man used the Time Stone to survive the snap in 2023?"

# --- tasks.py ---

from crewai import Task
from agents import miss_minutes, agent_mobius

fan_theory_input = "What if Iron Man used the Time Stone to survive the snap in 2023?"

fact_check_task = Task(
    description=(
        f"Analyze this theory: '{fan_theory_input}'.\n\n"
        f"1. Extract the core entities (e.g., 'Iron Man', 'Time Stone').\n"
        f"2. Use the 'Search Vault' tool to check for local data.\n"
        f"3. If the Vault returns a miss, use the 'Search the internet' tool to find the canon rules.\n"
        f"4. CRITICAL PROTOCOL: If you found new information on the internet, you CANNOT finish this task until you successfully execute the 'Update Vault' tool to save it. You must pass the entity, relation, and target to the tool.\n"
    ),
    expected_output=(
        "1. A bulleted list of verified MCU canon facts related to the theory.\n"
        "2. An 'Update Log' at the bottom explicitly stating which entities you successfully saved to the Vault using the Update tool."
    ),
    agent=miss_minutes
)

# ... (Keep judge_task exactly the same) ...

judge_task = Task(
    description=(
        f"Read the theory: '{fan_theory_input}'.\n"
        f"Read the facts retrieved by Miss Minutes.\n\n"
        f"Draft an official TVA Pruning Report. State clearly if this is a 'Stable Branch' or an 'Anomaly', "
        f"and explain exactly why."
    ),
    expected_output='A Markdown formatted TVA Pruning Report.',
    agent=agent_mobius,
    human_input=True # <-- THE HITL OVERRIDE: The system will ask for your permission here!
)