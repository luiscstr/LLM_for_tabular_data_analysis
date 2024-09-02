
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_community.agent_toolkits import create_sql_agent
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

#load_ext dotenv
load_dotenv()
print(load_dotenv())

#Connecting to database
db=SQLDatabase.from_uri(f"sqlite:///data/sqldb.db")

#Load the LLM
llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=5,
    # other params...
)

agent_executor = create_sql_agent(llm, db=db, verbose=True)