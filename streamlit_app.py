import streamlit as st
import requests

# ---- CONFIG ----
DJANGO_URL = "http://127.0.0.1:8000/api"

# ---- PAGE SETUP ----
st.set_page_config(
    page_title="Medical Report Explainer",
    layout="centered"
)

st.title(" Medical Report Explainer")
st.caption("Upload your medical report and ask questions in plain English")

if "session_id" not in st.session_state:
    st.session_state.session_id = None         # Groq session ID

if "explanation" not in st.session_state:
    st.session_state.explanation = None        # Initial PDF explanation

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []         # List of Q&A pairs for display



# SECTION 1: PDF UPLOAD
st.subheader(" Step 1: Upload Your Medical Report")

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=['pdf'],
    help="Upload your medical report, blood test, or lab results"
)

if uploaded_file is not None:
    # Show upload button only when file is selected
    if st.button(" Analyze Report", type="primary"):

        with st.spinner("Reading your report and generating explanation..."):
            try:
                # Send PDF to Django backend
                response = requests.post(
                    f"{DJANGO_URL}/upload/",
                    files={"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                )

                if response.status_code == 200:
                    data = response.json()

                    # Save to session_state so it survives reruns
                    st.session_state.session_id = data["session_id"]
                    st.session_state.explanation = data["explanation"]
                    st.session_state.chat_history = []  # Reset chat for new report

                    st.success(" Report analyzed successfully!")

                else:
                    st.error(f"Error: {response.json().get('error', 'Something went wrong')}")

            except requests.exceptions.ConnectionError:
                st.error(" Cannot connect to Django server. Make sure it's running on port 8000.")


# SECTION 2: SHOW EXPLANATION
if st.session_state.explanation:
    st.subheader(" Report Explanation")

    # Display the explanation in a nice box
    st.info(st.session_state.explanation)

    st.divider()

    # SECTION 3: CHAT FOR FOLLOW-UP QUESTIONS
    st.subheader(" Ask Follow-up Questions")
    st.caption("Ask anything about your report.. ")

    # Display chat history
    # This loops through saved Q&A pairs and displays them
    for chat in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(chat["question"])
        with st.chat_message("assistant"):
            st.write(chat["answer"])

    # Chat input box (appears at bottom like ChatGPT)
    question = st.chat_input("Ask a question about your report...")

    if question:
        # Show user message immediately
        with st.chat_message("user"):
            st.write(question)

        # Get answer from Django
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = requests.post(
                        f"{DJANGO_URL}/ask/",
                        json={
                            "session_id": st.session_state.session_id,
                            "question": question
                        }
                    )

                    if response.status_code == 200:
                        answer = response.json().get("answer")
                        st.write(answer)

                        # Save to chat history
                        st.session_state.chat_history.append({
                            "question": question,
                            "answer": answer
                        })

                    else:
                        st.error(f"Error: {response.json().get('error')}")

                except requests.exceptions.ConnectionError:
                    st.error(" Cannot connect to Django server.")

# SECTION 4: SIDEBAR INFO
with st.sidebar:
    st.header(" How to Use")
    st.markdown("""
    1. **Upload** your medical report PDF
    2. Click **Analyze Report**
    3. Read the plain English explanation
    4. **Ask questions** in the chat below
    """)

    st.divider()

    # Show session status
    if st.session_state.session_id:
        st.success(" Report loaded")
        if st.button(" Clear & Upload New Report"):
            st.session_state.session_id = None
            st.session_state.explanation = None
            st.session_state.chat_history = []
            st.rerun()
    else:
        st.warning(" No report uploaded yet")

    st.divider()
    st.caption(" This app explains reports in simple English. Always consult a doctor for medical advice.")