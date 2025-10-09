import os
import yaml
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()
api_key = os.environ["groq"]


class LLM:
    def __init__(
        self,
        model="llama-3.3-70b-versatile",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=api_key,
    ):
        self.params = {
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "timeout": timeout,
            "max_retries": max_retries,
            "api_key": api_key,
        }
        self.llm = ChatGroq(**self.params)
