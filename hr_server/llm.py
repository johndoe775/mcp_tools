from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.environ.get("gemini_api_key")

llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=api_key
)


# Initialize LLM
class LLM:
    def __init__(
        self,
        model="gemini-pro",
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
        self.llm = ChatGoogleGenerativeAI(**self.params)
