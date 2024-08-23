from pandasai.llm.local_llm import LocalLLM
import psutil
import streamlit as st
import pandas as pd
from pandasai import SmartDataframe, Agent

model= LocalLLM(api_base="http://localhost:11434/v1", model="llama3-chatqa:8b")
#"llama3-chatqa:8b-v1.5" Doesnt seem to work well with pandasai
st.title("Data analysis with PandasAI")
uploaded_file=st.file_uploader("Upload a CSV file",type=['csv'])

if uploaded_file is not None:
    data=pd.read_csv(uploaded_file)
    st.write(data.head(5))
    #agent=Agent(data, config={"llm": model,"enable_cache": False})
    df=SmartDataframe(data,config={"llm":model,"enable_cache": False})
    prompt=st.text_area("Enter your  prompt:")

    if st.button("Generate:"):
        if prompt:
            with st.spinner("Generating response..."):
                st.write(df.chat(prompt))
                #st.write(agent.chat(prompt))



