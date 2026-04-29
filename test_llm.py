from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()

# Initialize the LLM
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.3)

# Send a message
response = llm.invoke([
    HumanMessage(content="What does high creatinine in a blood test mean? Explain in simple English.")
])

print(response.content)