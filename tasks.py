from crewai import Task
from agents import miss_minutes, agent_mobius

fan_theory_input = "What if Iron Man used the Time Stone to survive the snap in 2023?"

fact_check_task = Task(
    description=(
        f"Analyze this theory: '{fan_theory_input}'.\n\n"
        f"1. Extract the core entities (e.g., 'Iron Man', 'Time Stone').\n"
        f"2. Use the 'Search Vault' tool to check for local data.\n"
        f"3. If you get a 'DATABASE MISS', use the web search tool to find the canon rules.\n"
        f"4. CRITICAL: You cannot finish this task until you execute the 'Update Vault' tool to save any new facts you found on the web.\n"
    ),
    expected_output=(
        "1. A bulleted list of verified MCU canon facts.\n"
        "2. An 'Update Log' explicitly listing the exact Entity -> Relation -> Target you saved to the Vault."
    ),
    agent=miss_minutes
)

judge_task = Task(
    description=(
        f"Read the theory: '{fan_theory_input}'.\n"
        f"Read the facts retrieved by Miss Minutes.\n\n"
        f"Draft an official TVA Pruning Report. State clearly if this is a 'Stable Branch' or an 'Anomaly', "
        f"and explain exactly why based on the rules of the MCU."
    ),
    expected_output='A Markdown formatted TVA Pruning Report.',
    agent=agent_mobius,
    human_input=True # Pause for human review
)