from crewai import Task
from agents import miss_minutes, agent_mobius

# You can change this to Thor, Hulk, or anything else now!
fan_theory_input = "What if Thor aimed for the head in Wakanda, survived the battle, and used the Infinity Gauntlet himself?"

fact_check_task = Task(
    description=(
        f"Conduct a thorough factual investigation of the following MCU timeline scenario: '{fan_theory_input}'.\n\n"
        f"Execute the following investigative protocol:\n"
        f"1. Entity Extraction: Identify all core components of this theory (Characters, Artifacts, Locations, Events).\n"
        f"2. Vault Verification: Query the 'Search Vault' tool for every extracted entity to gather established rules and histories.\n"
        f"3. Web Fallback: For any entity or rule missing from the Vault, use the web search tool to find the official MCU canon.\n"
        f"4. Database Injection: You CANNOT complete this task until you execute the 'Update Vault' tool for any new facts discovered via web search.\n"
    ),
    expected_output=(
        "A structured investigation document containing:\n"
        "- [Extracted Entities]: A list of the core subjects investigated.\n"
        "- [Verified Canon Facts]: A detailed, bulleted list of the absolute official MCU rules and histories pertaining to those entities.\n"
        "- [Update Log]: A strict log showing exactly which (Entity -> Relation -> Target) pairs you successfully injected into the Vault using the update tool. If no updates were needed, state 'No Vault Updates Required'."
    ),
    agent=miss_minutes
)

judge_task = Task(
    description=(
        f"Review the original timeline scenario: '{fan_theory_input}'.\n"
        f"Review the investigation document provided by the Fact Retrieval Unit.\n\n"
        f"Draft an official, highly professional TVA Pruning Report. Your analysis must strictly rely on the provided facts.\n"
        f"You must explicitly state if the scenario is a 'Stable Branch' (canonically possible) or an 'Anomaly' (breaks established rules). "
        f"Detail the exact logical contradictions or rule violations that inform your verdict."
    ),
    expected_output='A Markdown formatted TVA Pruning Report with the following sections: [Scenario], [Evidence Review], [Logical Analysis], and [Final Verdict].',
    agent=agent_mobius,
    human_input=True
)