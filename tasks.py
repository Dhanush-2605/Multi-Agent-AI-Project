from crewai import Task
from agents import miss_minutes, agent_mobius,ouroboros

# You can change this to Thor, Hulk, or anything else now!
fan_theory_input = "What happen if steve rogers didn't wake up in the 21st century and instead stayed in the 1940s with Peggy Carter?"
fact_check_task = Task(
    description=(
        "Conduct a thorough factual investigation of the following MCU timeline scenario: '{fan_theory_input}'.\n\n"
        "Execute the following investigative protocol STRICTLY in order:\n"
        "1. Entity Extraction: Identify all core components of this theory (Characters, Artifacts, Locations, Events).\n"
        "2. Vault Verification: Query the 'Search Vault' tool for every extracted entity.\n"
        "3. Web Fallback: For any entity missing from the Vault, use the web search tool to find official MCU canon.\n"
        "4. DATABASE INJECTION (CRITICAL): You MUST actually call and execute the 'Update Vault' tool with the new facts you found. Do NOT just write text. You must trigger the python tool.\n"
        "5. Final Report: ONLY write your Final Answer AFTER the 'Update Vault' tool has returned a success message."
    ),
    expected_output=(
        "A structured investigation document containing:\n"
        "- [Extracted Entities]: A list of the core subjects investigated.\n"
        "- [Verified Canon Facts]: A detailed, bulleted list of the absolute official MCU rules.\n"
        "- [Update Log]: You MUST copy and paste the exact success string returned by your 'Update Vault' tool here. If you did not execute the tool, your task is a failure."
    ),
    agent=miss_minutes
)

simulate_branch_task = Task(
    description=(
        "Review the hypothetical divergence: '{fan_theory_input}'.\n"
        "Review the baseline facts provided by the Fact Retrieval Unit.\n\n"
        "Simulate the temporal ripple effect. Identify the exact moment the timeline branches. "
        "Then, use your search tools to verify what *actually* happened in canon after this moment, "
        "and explicitly calculate what is now erased from existence. You must find at least 3 major downstream consequences."
    ),
    expected_output=(
        "A 'Temporal Ripple Report' detailing:\n"
        "- The Point of Divergence.\n"
        "- The Immediate Consequence.\n"
        "- Downstream Casualties (A bulleted list of future MCU canonical events, movies, or character arcs that are now erased or fundamentally broken)."
    ),
    agent=ouroboros
)
judge_task = Task(
    description=(
        "Review the original timeline scenario: '{fan_theory_input}'.\n"
        "Review the Temporal Ripple Report provided by O.B.\n\n" # <-- Mobius now reads O.B.'s report!
        "Draft an official, highly professional TVA Pruning Report. "
        "Because this theory erases major future canonical events, you MUST declare it an 'Anomaly'. "
        "Detail the exact downstream casualties that force this pruning."
    ),
    expected_output='A Markdown formatted TVA Pruning Report...',
    agent=agent_mobius,
    human_input=True
)
