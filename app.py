import streamlit as st
import openai
import os
from resume_input_handler import get_resume_input  # <- Import your helper module

# Set your OpenAI API key
openai.api_key =  os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    st.error("OpenAI API key not found. Please set it in secrets.toml or environment variables.")
    st.stop()

# Page setup
st.set_page_config(page_title="AI Resume Optimizer", layout="wide")
st.title("🧠 Resume Optimizer Based on Job Role")
st.markdown("Paste your resume or upload a file, and enter your target job description. This app will tailor your resume to improve alignment.")

# Get resume input (via file upload or text input)
resume_input = get_resume_input()

# Job description input
job_description = st.text_area("🎯 Job Description or Role", height=350)

# Optimize button
if st.button("🚀 Optimize Resume"):
    if not resume_input.strip() or not job_description.strip():
        st.warning("Both resume and job description are required.")
    else:
        with st.spinner("Optimizing your resume with AI..."):
            prompt = f"""
You are a professional resume coach. Improve the following resume to better align with this job description. Focus on:
- Including relevant keywords
- Rewriting bullet points to match required skills/responsibilities
- Tailoring the summary or objective

Job Description:
{job_description}

Resume:
{resume_input}

Return only the improved resume, without any explanation.
"""
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a resume optimization expert."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1500
                )
                optimized_resume = response.choices[0].message.content.strip()

                st.success("✅ Resume optimized successfully!")
                st.subheader("📑 Optimized Resume")
                st.text_area("", value=optimized_resume, height=400)

                st.download_button(
                    label="⬇️ Download Optimized Resume",
                    data=optimized_resume,
                    file_name="optimized_resume.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"⚠️ Error optimizing resume: {e}")
