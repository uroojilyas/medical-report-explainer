#  Medical Report Explainer

An AI-powered RAG (Retrieval-Augmented Generation) application that explains medical reports in plain English and answers follow-up questions using conversational memory.

---

##  Features

- Upload any medical PDF report
- Get an instant plain English explanation
- Ask follow-up questions in a chat interface
- Conversation memory that remembers previous questions
- Semantic search powered by Pinecone vector database

---

##  Tech Stack

| Layer | Technology |
|---|---|
| LLM | Groq (LLaMA 3) |
| RAG Framework | LangChain |
| Vector Database | Pinecone |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Backend | Django REST Framework |
| Frontend | Streamlit |
| PDF Extraction | pdfplumber |

---

##  Architecture

**Upload Phase**

1. User uploads a PDF file
2. pdfplumber extracts the text
3. Text is split into small chunks using LangChain TextSplitter
4. Each chunk is converted to a vector using all-MiniLM-L6-v2
5. Vectors are stored in Pinecone vector database

**Question Phase**

1. User types a question
2. Question is converted to a vector
3. Pinecone finds the top 5 most relevant chunks
4. Relevant chunks and question are sent to Groq LLaMA 3
5. A plain English answer is returned to the user

---

##  Installation

**1. Clone the repository**

```
git clone https://github.com/uroojilyas/medical-report-explainer.git
cd medical-report-explainer
```

**2. Create a virtual environment**

```
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**

```
pip install -r requirements.txt
```

**4. Create a .env file in the project root**

```
DJANGO_SECRET_KEY=your_django_secret_key
GROQ_API_KEY=your_groq_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=medical-reports
DEBUG=True
```

**5. Run the Django backend**

```
python manage.py migrate
python manage.py runserver
```

**6. Run the Streamlit frontend**

```
streamlit run streamlit_app.py
```

---

