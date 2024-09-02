
import os
from dotenv import load_dotenv
import yaml
import shutil
from langchain_google_genai import ChatGoogleGenerativeAI
import chromadb

print("Environment variables are loaded:", load_dotenv())
class LoadConfig:
    def __init__(self) -> None:
        with open(h"config/app_config.yml")) as cfg:
            app_config = yaml.load(cfg, Loader=yaml.FullLoader)
            self.load_directories(app_config=app_config)
            self.load_llm_configs(app_config=app_config)
            self.load_chroma_client()
            self.load_rag_config(app_config=app_config)
