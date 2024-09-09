from pandasai.llm.local_llm import LocalLLM
import psutil
import streamlit as st
import pandas as pd
from pandasai import SmartDataframe, Agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import logging
from io import StringIO

load_dotenv()
#model= LocalLLM(api_base="http://localhost:11434/v1", model="llama3-chatqa:8b")

#To get code from console log (any other way to obtain the code used by the agent?)
# Step 1: Create a StringIO object to store logs
log_stream = StringIO()

# Step 2: Set up logging to use the StringIO object
stream_handler = logging.StreamHandler(log_stream)
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)

#Function to extract the code from the log
def get_text_between(text, start, end):
    """
    Extracts the text between two specified substrings.

    :param text: The full text from which to extract the substring.
    :param start: The substring marking the beginning of the desired text.
    :param end: The substring marking the end of the desired text.
    :return: The extracted substring, or an empty string if not found.
    """
    if start in text and end in text:
        return text.split(start)[1].split(end)[0]
    return ""



model = ChatGroq(
        model="llama-3.1-70b-versatile",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=5,
        # other params...
        )


#"llama3-chatqa:8b-v1.5" Doesnt seem to work well with pandasai
st.title("Data analysis with PandasAI")
uploaded_file=st.file_uploader("Upload a CSV file",type=['csv'])

if uploaded_file is not None:
    data=pd.read_csv(uploaded_file)
    st.write(data.head(5))
    #agent=Agent(data, config={"llm": model,"enable_cache": False})
    
    df=SmartDataframe(data,config={"llm":model,"enable_cache": False})
    agent=Agent(df, config={"llm":model,"enable_cache": False},
                description="You are a data analysis agent. Your main goal is to help non-technical users to analyze data")
    
    if "history" not in st.session_state:
        st.session_state.history = []
    
    user_input=st.text_input("Ask a question about the data:", "")
    show_code = st.checkbox("Show Code", value=False)
    #show_reasoning = st.checkbox("Show Reasoning", value=False)

    if user_input:
        st.session_state.history.append({"role": "user", "content": user_input})
        #Agent response
        response = agent.chat(user_input)
        response_text = response  # PandasAI's answer
        #Agent code
        logger.info("PandasAI Result: %s", response) #COnsoloe log 
        log_contents = log_stream.getvalue() #Get the console log as a string
        generated_code = get_text_between(log_contents,"### GENERATED CODE","Reason step by step and at the end answer") # Code used to produce the result

        #Agent reasoning
        
        reasoning = agent.explain()  # Reasoning if requested
        
        st.session_state.history.append({"role": "assistant", "content": generated_code})

        if show_code:           
            st.session_state.history.append({"role": "code", "content": generated_code })

        if reasoning:
            if st.button("Explain"):
                with st.expander("Reasoning", expanded=True):
                    st.write(reasoning)
    
    st.write("### Conversation History:")  
    for chat in st.session_state.history:
        if chat["role"] == "user":
            st.write(f"**You:** {chat['content']}")
        elif chat["role"] == "assistant":
            st.write(f"**Bot:** {chat['content']}")
        #elif chat["role"] == "reasoning":
         #   st.write(f"**Reasoning:** {chat['content']}")  
        elif chat["role"] == "code":
            st.write(f"**Code used by the Bot:**\n```python\n{chat['content']}\n```")
    
    #if st.button("Generate:"):
     #   if prompt:
      #      with st.spinner("Generating response..."):
       #         st.write(df.chat(prompt))
                #st.write(agent.chat(prompt))
    if st.button("Clear Chat History"):
        st.session_state.history = []


