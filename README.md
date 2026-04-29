```markdown
#  Medical Report Explainer

An AI-powered RAG application that explains medical reports in plain English and answers follow-up questions using conversational memory.

## Features
- Upload any medical PDF report
- Get instant plain English explanation
- Ask follow-up questions in a chat interface
- Conversation memory (remembers previous questions)
- Semantic search using Pinecone vector database

## Tech Stack
- **LangChain** — RAG pipeline and conversation memory
- **Groq (LLaMA 3)** — LLM for generating explanations
- **Pinecone** — Vector database for semantic search
- **sentence-transformers** — Local embedding model (all-MiniLM-L6-v2)
- **Django REST Framework** — Backend API
- **Streamlit** — Frontend UI
- **pdfplumber** — PDF text extraction

##  Architecture

**Upload Phase:**
1. User uploads PDF → pdfplumber extracts text
2. Text split into small chunks using LangChain TextSplitter
3. Each chunk converted to vector using all-MiniLM-L6-v2
4. Vectors stored in Pinecone vector database

**Question Phase:**
1. User question converted to vector
2. Pinecone finds top 5 most relevant chunks
3. Relevant chunks + question sent to Groq LLaMA 3
4. Plain English answer returned to user

##  Installation

### 1. Clone the repository
git clone https://github.com/uroojilyas/medical-report-explainer.git
cd medical-report-explainer
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create `.env` file
```
DJANGO_SECRET_KEY=your_django_secret_key
GROQ_API_KEY=your_groq_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=medical-reports
DEBUG=True
```

### 5. Run Django backend
```bash
python manage.py migrate
python manage.py runserver
```

### 6. Run Streamlit frontend
```bash
streamlit run streamlit_app.py
```

## How to Use
1. Open `http://localhost:8501` in your browser
2. Upload your medical report PDF
3. Read the plain English explanation
4. Ask follow-up questions in the chat
