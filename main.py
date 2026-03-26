import os
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from crewai_tools import SerperDevTool
from model import llm
load_dotenv()

# 1. Set your Gemini API key
my_key = os.getenv("API_KEY") 
serper_key = os.getenv("SERPER_API_KEY")
# print(my_k)

# # Pass it directly into the object
# llm = ChatGoogleGenerativeAI(
#         model="gemini-1.5-flash",
#         google_api_key="AIzaSyDcBwKSrjrlvqFJceSE9tWJgUSwrSNsYy8",
#         temperature=0.2



#     )
SerperDevTool(api_key=serper_key)

print("Welcome to your AI Research Team!")
topic = input("What technical topic would you like the agents to research today? \n> ")




researcher = Agent(
    role='Senior Technology Analyst',
goal=f'Gather highly technical, up-to-date documentation and facts on {topic}',
    backstory='You are a veteran tech analyst. You excel at finding precise, factual, and cutting-edge information.',
    verbose=True,
    allow_delegation=False,
    llm=llm # Passing Gemini to the agent
)

# 4. Define Agent Two: The Writer
writer = Agent(
    role='Technical Content Strategist',
goal=f'Format the research on {topic} into a clear, readable engineering guide',
    backstory='You are a renowned tech writer known for turning dense, academic research into engaging blog posts.',
    verbose=True,
    allow_delegation=False,
    llm=llm # Passing Gemini to the agent
)

task1 = Task(
description=f'Search the web for the latest documentation on {topic}. Extract key features, use cases, and realistic code examples or architecture patterns.',    
expected_output=f'A raw but detailed research report containing facts, use cases, and technical details about {topic}.',    
agent=researcher
)

# 6. Define Task Two: Writing
task2 = Task(
description=f'Using the researcher\'s report, write a polished, structured engineering guide on {topic}.',
expected_output='A well-formatted Markdown guide with a title, introduction, technical explanation, and a code block or design pattern.',    
agent=writer
)

# 7. Form the Crew and execute!
tech_crew = Crew(
    agents=[researcher, writer],
    tasks=[task1, task2],
    process=Process.sequential
)

print(f"\nKicking off research on: {topic}...")
result = tech_crew.kickoff()



print("######################")
print("FINAL OUTPUT:")
print("######################")
print(result)













