#Update test
import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import os
from dotenv import load_dotenv

# --- Custom CSS for UI/UX Enhancements ---
st.markdown("""
<style>
    .main {
        background-color: #f0f2f6; /* Soft background */
    }
    .stButton>button {
        background-color: #4CAF50; /* Green */
        color: white;
        border-radius: 12px;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border: none;
        transition: all 0.3s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #45a049;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        transform: scale(1.02);
    }
    .stTextArea {
        border-radius: 12px;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.1);
        padding: 15px;
        background-color: white;
    }
    .stFileUploader {
        border-radius: 12px;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.1);
        padding: 15px;
        background-color: white;
    }
    .stSpinner + div {
        border-radius: 12px;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.1);
        padding: 15px;
        background-color: white;
        margin-top: 10px;
    }
    .stCard {
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.1);
        padding: 20px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize model (use latest)
model = genai.GenerativeModel("gemini-1.5-flash")

# Streamlit App
st.set_page_config(page_title="📘 StudyMate - Smart PDF Summarizer", layout="wide")

st.title("📘 StudyMate - Smart PDF Summarizer")
st.write("Upload your study material PDF and get **well-structured, point-wise notes** instantly ✨")

# File upload
uploaded_file = st.file_uploader("📂 Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    # Extract text
    reader = PdfReader(uploaded_file)
    raw_text = ""
    for page in reader.pages:
        raw_text += page.extract_text() + "\n"

    if not raw_text.strip(): # Check if extracted text is empty or just whitespace
        st.warning("⚠️ Could not extract text from the PDF. This might happen with scanned documents or image-based PDFs. Please try a different PDF or ensure it contains selectable text.")
        st.stop() # Stop further execution if no text is extracted

    st.subheader("📄 Extracted Text Preview")
    st.markdown("<div class='stCard'>", unsafe_allow_html=True)
    st.text_area("Preview", raw_text[:2000] + ("..." if len(raw_text) > 2000 else ""), height=200, help="This is a preview of the text extracted from your PDF. Only the first 2000 characters are shown.")
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("✨ Generate Professional Notes"):
        with st.spinner("Analyzing your PDF and preparing notes... ⏳"):
            prompt = f"""
            You are StudyMate, an expert study assistant.
            The user has uploaded study material. 
            
            TASK:
            - Read the following PDF content carefully.
            - Extract the key details and summarize them clearly.
            - Present the output in **structured bullet points** with proper headings.
            - Use bold text for important terms, and keep formatting professional.
            - Ensure clarity and readability for exam preparation.

            PDF Content:
            {raw_text}
            """

            response = model.generate_content(prompt)

        st.subheader("✅ Professional Point-wise Notes")
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        st.markdown(response.text)
        st.markdown("</div>", unsafe_allow_html=True)
