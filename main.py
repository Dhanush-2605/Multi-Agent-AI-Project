from crewai import Crew, Process
from agents import miss_minutes, agent_mobius
from tasks import fact_check_task, judge_task

tva_crew = Crew(
    agents=[miss_minutes, agent_mobius],
    tasks=[fact_check_task, judge_task],
    process=Process.sequential,
    verbose=True
)

if __name__ == "__main__":
    print("⏳ Booting up the Time Variance Authority...")
    print("⚠️  NOTE: You will be asked to manually approve the final report before it is saved!\n")
    
    result = tva_crew.kickoff()
    
    with open("TVA_Pruning_Report.md", "w", encoding="utf-8") as file:
        file.write(str(result))
        
    print("\n✅ Operation Complete! Check TVA_Pruning_Report.md")