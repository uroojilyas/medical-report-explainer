from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from extract_pdf import extract_text_from_pdf

load_dotenv()

# ---- 1. Load the LLM ----
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.3)

# ---- 2. Define the Prompt Template ----
prompt = ChatPromptTemplate.from_template("""
You are a helpful medical assistant. Your job is to explain medical reports 
in simple, plain English that a non-medical person can understand.

Use ONLY the information provided in the report below. 
Do not add outside knowledge. If something is not in the report, say so.

MEDICAL REPORT:
{report_text}

USER QUESTION:
{question}

Answer in simple, clear English:
""")

# ---- 3. Build the Chain ----
chain = prompt | llm

# ---- 4. Main function ----
def ask_question(pdf_path, question):
    # Step 1: Extract text from PDF
    report_text = extract_text_from_pdf(pdf_path)

    # Step 2: Run the chain
    response = chain.invoke({
        "report_text": report_text,
        "question": question
    })

    return response.content


# ---- 5. Test it ----
if __name__ == "__main__":
    pdf_path = r"files/CBC-test-report.pdf"

    # First question — explain the whole report
    print("=" * 50)
    print("Q: Can you explain this medical report in simple English?")
    print("=" * 50)
    answer = ask_question(pdf_path, "Can you explain this medical report in simple English?")
    print(answer)

    # Second question — specific value
    print("\n" + "=" * 50)
    print("Q: Are there any abnormal values I should be worried about?")
    print("=" * 50)
    answer2 = ask_question(pdf_path, "Are there any abnormal values I should be worried about?")
    print(answer2)