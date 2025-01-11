from pandasai.llm.local_llm import LocalLLM
import psutil
import streamlit as st
import pandas as pd
from pandasai import SmartDataframe, Agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from PIL import Image
import base64
from io import BytesIO
import html

load_dotenv()
#model= LocalLLM(api_base="http://localhost:11434/v1", model="llama3-chatqa:8b")

model = ChatGroq(
        model="llama-3.1-70b-versatile",
        temperature=0,
        max_tokens=1024,
        timeout=None,
        max_retries=5,
        # other params...
        )


#"llama3-chatqa:8b-v1.5" Doesnt seem to work well with pandasai
st.title("Data analysis with PandasAI")
uploaded_file = st.file_uploader("Upload a CSV or XLSX file", type=['csv', 'xlsx'])

# Load images for user and bot
bot_image = Image.open("images/chatbot.jpg")  
user_image = Image.open("images/user.png")  

def image_to_base64(image):
    """Convert image to base64 for rendering in HTML."""
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

bot_image_base64 = image_to_base64(bot_image)
user_image_base64 = image_to_base64(user_image)

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            data=pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            data = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file format. Please upload a CSV or XLSX file.")
            data = None
            
        if data is not None:
            st.write(data.head(5))
    
            try:
                df=SmartDataframe(data,config={"llm":model,"enable_cache": False})
                agent=Agent(df, config={"llm":model,"enable_cache": False},
                    description="You are a data analysis agent. Your main goal is to help non-technical users to analyze data")
            except Exception as e:
                st.error(f"Failed to initialize the agent: {e}")
                
            if "history" not in st.session_state:
                st.session_state.history = []

            user_input=st.text_area("Ask a question about the data:", "")

            
            if st.session_state.history:
               
                st.write("### Conversation History:")  
                for chat in st.session_state.history:
                    if chat["role"] == "user":
                        st.markdown(f"""
                        <div class="chat-box user-message">
                            <div class="chat-message">
                                <img src="data:image/png;base64,{user_image_base64}" alt="User" width="40" height="40" />
                                <div class="chat-text">**You**: {chat['content']}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    elif chat["role"] == "assistant":
                        st.markdown(f"""
                        <div class="chat-box bot-message">
                            <div class="chat-message">
                                <img src="data:image/png;base64,{bot_image_base64}" alt="Bot" width="40" height="40" />
                                <div class="chat-text">**Bot**: {chat['content']}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
           
            st.markdown(
                """
                <style>
                .chat-box {
                    display: flex;
                    align-items: center;
                    margin-bottom: 10px;
                    max-width: 700px;
                    }
                .user-message {
                    justify-content: flex-end;
                    flex-direction: row-reverse;
                    background-color: #e6e6ff;
                    border-radius: 15px;
                    padding: 10px;
                    max-width: 60%;
                    word-wrap: break-word;
                    margin-left: auto;
                }
                .bot-message {
                    justify-content: flex-start;
                    background-color: #d1e7dd;
                    border-radius: 15px;
                    padding: 10px;
                    max-width: 60%;
                    word-wrap: break-word;
                    margin-right: auto;
                }
                .chat-message {
                    display: flex;
                    align-items: center;
                }
                .chat-message img {
                    width: 40px;
                    height: 40px;
                    margin: 5px;
                    border-radius: 50%;
                }
                </style>
                """, unsafe_allow_html=True
            )
            
            

            

            if user_input:
                try:
                    st.session_state.history.append({"role": "user", "content": user_input})
                    #Agent response
                    response = agent.chat(user_input)
                    response_text = response  # PandasAI's answer
                    st.session_state.history.append({"role": "assistant", "content": response_text})
                    #Agent code  
                    generated_code  = agent.context.intermediate_values['current_code_executed']
       
                    #Agent reasoning
                    reasoning = agent.explain()  # Reasoning if requested

                    # Display agent's response
                    st.write(f"**Bot**: {response_text}")
                    if generated_code :     
                        with st.expander("Code", expanded=True):
                            st.code(generated_code, language='python') 
                    if reasoning:
                        with st.expander("Reasoning", expanded=True):
                            st.write(reasoning)
                        
                except Exception as e:
                        st.error(f"An error occurred during the analysis: {e}")
      
        #if st.button("Generate:"):
     #   if prompt:
      #      with st.spinner("Generating response..."):
       #         st.write(df.chat(prompt))
                #st.write(agent.chat(prompt))
            if st.button("Clear Chat History"):
                st.session_state.history = []
                
    except Exception as e:
        st.error(f"Failed to process the file: {e}")

