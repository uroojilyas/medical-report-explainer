from dotenv import load_dotenv
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import uuid

load_dotenv()

# ---- 1. Initialize Pinecone ----
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))

# ---- 2. Initialize Embedding Model ----
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# ---- 3. Text Splitter ----
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,       # each chunk = max 500 characters
    chunk_overlap=50,     # 50 chars overlap between chunks
)


def store_pdf_in_pinecone(report_text: str, session_id: str):
    """
    Takes extracted PDF text, splits into chunks,
    converts to vectors, stores in Pinecone.
    Returns number of chunks stored.
    """

    # Step 1: Split text into chunks
    chunks = text_splitter.split_text(report_text)
    print(f"Split into {len(chunks)} chunks")

    # Step 2: Convert chunks to vectors
    vectors = embedding_model.encode(chunks)
    # vectors is now a list of 384-dimension arrays

    # Step 3: Prepare data for Pinecone
    # Pinecone needs: (id, vector, metadata)
    pinecone_data = []
    for i, (chunk, vector) in enumerate(zip(chunks, vectors)):
        pinecone_data.append({
            "id": f"{session_id}_chunk_{i}",   # unique ID per chunk
            "values": vector.tolist(),          # the actual vector
            "metadata": {
                "text": chunk,                  # original text (for retrieval)
                "session_id": session_id,       # which user uploaded this
                "chunk_index": i                # position in document
            }
        })

    # Step 4: Upload to Pinecone in batches
    batch_size = 50
    for i in range(0, len(pinecone_data), batch_size):
        batch = pinecone_data[i:i + batch_size]
        index.upsert(vectors=batch)

    print(f"Stored {len(chunks)} chunks in Pinecone")
    return len(chunks)


def search_pinecone(question: str, session_id: str, top_k: int = 5):
    """
    Converts question to vector, searches Pinecone
    for most relevant chunks from THIS user's session.
    Returns top_k most relevant text chunks.
    """

    # Step 1: Convert question to vector
    question_vector = embedding_model.encode(question).tolist()

    # Step 2: Search Pinecone
    # filter = only search chunks from THIS user's PDF
    results = index.query(
        vector=question_vector,
        top_k=top_k,
        include_metadata=True,
        filter={"session_id": {"$eq": session_id}}
    )

    # Step 3: Extract text from results
    relevant_chunks = []
    for match in results.matches:
        relevant_chunks.append(match.metadata["text"])

    return relevant_chunks


def delete_session_vectors(session_id: str):
    """
    Deletes all vectors for a session from Pinecone.
    Called when user uploads a new report.
    """
    # Fetch IDs belonging to this session and delete them
    index.delete(filter={"session_id": {"$eq": session_id}})
    print(f"Deleted vectors for session {session_id}")