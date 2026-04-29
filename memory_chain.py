from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from vector_store import search_pinecone   # 👈 new import

load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.3)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful medical assistant. Explain medical reports
in simple, plain English that a non-medical person can understand.
Use ONLY the information from the relevant sections below.
If something is not in the provided sections, say so clearly.

RELEVANT SECTIONS FROM MEDICAL REPORT:
{report_context}"""),                    # 👈 changed from report_text to report_context

    MessagesPlaceholder(variable_name="chat_history"),

    ("human", "{question}"),
])

chain = prompt | llm

store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="chat_history",
)


def ask_with_memory(question: str, session_id: str):
    """
    1. Search Pinecone for relevant chunks
    2. Send only relevant chunks + question to Groq
    """

    # Step 1: Find relevant chunks from Pinecone
    relevant_chunks = search_pinecone(question, session_id)

    # Step 2: Join chunks into context string
    report_context = "\n\n---\n\n".join(relevant_chunks)

    # 🧠 This is REAL RAG now:
    # Instead of sending 50,000 tokens (whole PDF)
    # We send only ~2,500 tokens (5 relevant chunks)

    # Step 3: Ask with memory
    response = chain_with_memory.invoke(
        {
            "report_context": report_context,
            "question": question
        },
        config={"configurable": {"session_id": session_id}}
    )

    return response.content