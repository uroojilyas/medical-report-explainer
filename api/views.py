from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import tempfile
import os
import uuid

from extract_pdf import extract_text_from_pdf
from memory_chain import ask_with_memory
from vector_store import store_pdf_in_pinecone, delete_session_vectors  

pdf_store = {}

@api_view(['POST'])
def upload_report(request):
    if 'file' not in request.FILES:
        return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

    pdf_file = request.FILES['file']

    if not pdf_file.name.endswith('.pdf'):
        return Response({'error': 'Only PDF files are allowed'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            for chunk in pdf_file.chunks():
                tmp.write(chunk)
            tmp_path = tmp.name

        report_text = extract_text_from_pdf(tmp_path)
        os.unlink(tmp_path)

        if not report_text.strip():
            return Response({'error': 'Could not extract text from PDF.'}, status=status.HTTP_400_BAD_REQUEST)

        session_id = str(uuid.uuid4())

        store_pdf_in_pinecone(report_text, session_id)

        initial_explanation = ask_with_memory(
            question="Please explain this medical report in simple English. List any abnormal values and what they mean.",
            session_id=session_id
        )

        return Response({
            'session_id': session_id,
            'explanation': initial_explanation,
            'message': 'Report uploaded successfully'
        })

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def ask_question(request):
    session_id = request.data.get('session_id')
    question = request.data.get('question')

    if not session_id:
        return Response({'error': 'session_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    if not question:
        return Response({'error': 'question is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        answer = ask_with_memory(
            question=question,
            session_id=session_id
        )

        return Response({'answer': answer, 'session_id': session_id})

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)