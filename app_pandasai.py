from pandasai.llm.local_llm import LocalLLM
import streamlit as st
import pandas as pd
from pandasai import SmartDataframe, Agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize model (ChatGroq)
model = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=0,
    max_tokens=1024,
    timeout=None,
    max_retries=5,
)

# Streamlit App
st.title("Data Analysis with PandasAI")
uploaded_file = st.file_uploader("Upload a CSV or XLSX file", type=['csv', 'xlsx'])

# Clear chat button functionality
if st.button("Clear Chat"):
    st.session_state.messages = []  # Clear chat memory
    st.rerun()  # Rerun the app to update the UI

# Check if a file is uploaded
if uploaded_file is not None:
    try:
        # Load the file
        if uploaded_file.name.endswith('.csv'):
            data = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            data = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file format. Please upload a CSV or XLSX file.")
            data = None

        if data is not None:
            st.write(data.head(5))  # Display first 5 rows

            # Initialize SmartDataframe and Agent
            try:
                df = SmartDataframe(data, config={"llm": model, "enable_cache": False})
                agent = Agent(df, config={"llm": model, "enable_cache": False},
                              description="You are a data analysis agent. Your main goal is to help non-technical users to analyze data.")
            except Exception as e:
                st.error(f"Failed to initialize the agent: {e}")

            # Initialize chat history
            if "messages" not in st.session_state:
                st.session_state.messages = []
                
            # Display chat messages from history on app rerun
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])


            if prompt := st.chat_input("Enter your message"):
                try:
                    # Add user message to chat history
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    
                    # Display user message in chat message container
                    with st.chat_message("user"):
                        st.markdown(prompt)


                    # Construct the chat history for the agent (concatenate all messages)
                    #conversation_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])
                    
                    # Display assistant response in chat message container
                    with st.chat_message("assistant"):
                        
                        response = agent.chat(prompt)
                        #response = agent.chat(conversation_history)
                        st.markdown(response)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                    # Display generated code and reasoning if available
                    generated_code = agent.context.intermediate_values.get('current_code_executed', None)
                    if generated_code:
                        with st.expander("Generated Code", expanded=True):
                            st.code(generated_code, language='python')
                    
                    reasoning = agent.explain() if agent else None
                    if reasoning:
                        with st.expander("Reasoning", expanded=True):
                            st.write(reasoning)
                except Exception as e:
                        st.error(f"An error occurred during the analysis: {e}")

    except Exception as e:
        st.error(f"Failed to process the file: {e}")
