from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_webpage
import os 
from dotenv import load_dotenv
load_dotenv

llm = ChatMistralAI(
    model="mistral-small-latest", # Or "mistral-small-latest" / "codestral-latest"
    temperature=0.1
)

def build_search_agent():
    return create_agent(
            model=llm, 
            tools= [web_search]
    )

def build_scrape_agent():
    return create_agent(
        model=llm,
        tools= [scrape_webpage]
    ) 

writer_prompt = ChatPromptTemplate.from_messages([
    ("system" , "you are an expert research writer. write clear, structured and insightful reports."),
    ("human" , """write a detailed research report on the topic below.
Topic: {topic}
research gathered:
{research}

structure the report as :
Intro
Key finding(minimum 3 well explained points)
Conclusion
Sources
be detailed , factual, and professional"""),
])

writer_chain = writer_prompt | llm | StrOutputParser()
