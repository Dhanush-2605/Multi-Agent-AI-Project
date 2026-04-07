from crewai import Crew, Process
from agents import miss_minutes, agent_mobius,ouroboros
from tasks import fact_check_task, judge_task,simulate_branch_task

tva_crew = Crew(
    agents=[miss_minutes, ouroboros, agent_mobius], # Add O.B. in the middle
    tasks=[fact_check_task, simulate_branch_task, judge_task], # Add simulation in the middle
    process=Process.sequential,
    max_rpm=10, 
    verbose=True
)

if __name__ == "__main__":
    print("⏳ Booting up the Time Variance Authority...")
    print("⚠️  NOTE: You will be asked to manually approve the final report before it is saved!\n")
    
    result = tva_crew.kickoff()
    
    with open("TVA_Pruning_Report.md", "w", encoding="utf-8") as file:
        file.write(str(result))
        
    print("\n✅ Operation Complete! Check TVA_Pruning_Report.md")