import streamlit as st
import pdfplumber
import docx

def get_resume_input():
    """
    Presents the user with options to paste or upload a resume,
    and returns the extracted text as a string.
    """
    upload_option = st.radio("Choose input method:", ["Paste Text", "Upload File"])
    resume_input = ""

    if upload_option == "Upload File":
        uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "docx"])

        if uploaded_file:
            file_type = uploaded_file.name.split(".")[-1].lower()

            try:
                if file_type == "pdf":
                    with pdfplumber.open(uploaded_file) as pdf:
                        resume_input = "\n".join(
                            page.extract_text() for page in pdf.pages if page.extract_text()
                        )

                elif file_type == "docx":
                    doc = docx.Document(uploaded_file)
                    resume_input = "\n".join([para.text for para in doc.paragraphs])

                else:
                    st.error("Unsupported file format.")
            except Exception as e:
                st.error(f"Error reading file: {e}")

    else:
        resume_input = st.text_area("📄 Your Current Resume", height=350)

    return resume_input
