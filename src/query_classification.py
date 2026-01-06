from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

def classify_query(query: str) -> str:
    # For demo purposes, default to document search to avoid API costs
    return "document"