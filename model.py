
import os
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from crewai_tools import SerperDevTool
load_dotenv()

# 1. Set your Gemini API key
my_key = os.getenv("API_KEY") 
serper_key = os.getenv("SERPER_API_KEY")

llm = LLM(
model="gemini/gemini-2.5-flash",
    api_key=my_key,
    temperature=0.2
)
