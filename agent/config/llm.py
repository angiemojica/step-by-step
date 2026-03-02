from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()


def get_llm(model: str = "llama-3.3-70b-versatile", temperature: float = 0) -> ChatGroq:
    return ChatGroq(model=model, temperature=temperature)