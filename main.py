import os
from crewai import Agent, Task, Crew, Process, LLM
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. Set your Gemini API key
my_key = os.getenv("API_KEY") 

# # Pass it directly into the object
# llm = ChatGoogleGenerativeAI(
#         model="gemini-1.5-flash",
#         google_api_key="AIzaSyDcBwKSrjrlvqFJceSE9tWJgUSwrSNsYy8",
#         temperature=0.2



#     )

llm = LLM(
model="gemini/gemini-2.5-flash",
    api_key=my_key,
    temperature=0.2
)

# print(llm.invoke("Hello, Gemini! Can you tell me a joke?"))

researcher = Agent(
    role='Senior Technology Analyst',
    goal='Uncover the latest advancements in solid-state batteries',
    backstory='You are a veteran tech analyst. You excel at finding precise, factual, and cutting-edge information.',
    verbose=True,
    allow_delegation=False,
    llm=llm # Passing Gemini to the agent
)

# 4. Define Agent Two: The Writer
writer = Agent(
    role='Technical Content Strategist',
    goal='Craft compelling and easy-to-understand articles on complex tech topics',
    backstory='You are a renowned tech writer known for turning dense, academic research into engaging blog posts.',
    verbose=True,
    allow_delegation=False,
    llm=llm # Passing Gemini to the agent
)

task1 = Task(
    description='Analyze the current state of solid-state batteries in 2026. Identify key breakthroughs and major companies involved.',
    expected_output='A comprehensive bulleted summary of the latest solid-state battery advancements.',
    agent=researcher
)

# 6. Define Task Two: Writing
task2 = Task(
    description='Using the insights provided by the researcher, write an engaging blog post explaining why solid-state batteries are the future of EVs.',
    expected_output='A 4-paragraph blog post with a catchy title, an introduction, main body, and conclusion.',
    agent=writer
)

# 7. Form the Crew and execute!
tech_crew = Crew(
    agents=[researcher, writer],
    tasks=[task1, task2],
    process=Process.sequential
)

# Start the process
result = tech_crew.kickoff()

print("######################")
print("FINAL OUTPUT:")
print("######################")
print(result)













