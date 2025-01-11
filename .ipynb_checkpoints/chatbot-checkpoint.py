from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_community.agent_toolkits import create_sql_agent
from sqlalchemy import create_engine
from dotenv import load_dotenv
from typing import List, Tuple
import os


class ChatBot:
    @staticmethod
    def respond (chatbot:List,message:str)->Tuple:
        """
        Args:
           chatbot (List)= list representing the cahtbot's conversation history
           message (str)=user's input message to the chatbot
       Returns:
           A tuple with a placeholder value and the updated conversation history list
        """
        #loading database
        if os.path.exists('./data/sqldb.db'):
            db=SQLDatabase.from_uri(f"sqlite:///data/sqldb.db")
        else:
            chatbot.append(
                (message, f"SQL DB does not exist. Please first create the 'sqldb.db'"))
            return "",chatbot

        #Loading llm
        llm = ChatGroq(
        model="llama-3.1-70b-versatile",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=5,
        # other params...
        )

        agent_executor = create_sql_agent(llm, db=db, verbose=False)
        response=agent_executor.invoke({"input": message})
        response = response["output"]
        
        chatbot.append(
                (message, response))
        
        return "",chatbot


