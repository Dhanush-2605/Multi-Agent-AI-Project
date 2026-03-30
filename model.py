
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
    model="gemini/gemini-2.5-flash",  # ✅ correct
    api_key=os.getenv("API_KEY"),
    temperature=0.2,
)


# curl https://generativelanguage.googleapis.com/v1beta/models \
#   -H "Authorization: Bearer AIzaSyCCnNAnVyRukqAcwF_9wBKpCWaqatN9W7k"
# Deep Research Pro Preview
#  curl "https://generativelanguage.googleapis.com/v1beta/models?key=AIzaSyCCnNAnVyRukqAcwF_9wBKpCWaqatN9W7k"