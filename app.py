import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai
from dotenv import load_dotenv
import os
# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.markdown("""
<style>
div.stDownloadButton > button {
    height: 60px;
    font-size: 20px;
    font-weight: bold;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- GEMINI API ----------------
load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)
model = genai.GenerativeModel("gemini-2.5-flash")

# ---------------- HEADER ----------------
st.title("📄 AI Resume Analyzer")
st.caption("Upload your resume and get ATS-based AI feedback")

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader(
    "Upload Your Resume (PDF)",
    type=["pdf"]
)

if uploaded_file is not None:

    try:
        reader = PdfReader(uploaded_file)

        resume_text = ""

        for page in reader.pages:
            text = page.extract_text()
            if text:
                resume_text += text

        st.success("✅ Resume Uploaded Successfully!")

        with st.expander("📃 View Extracted Resume Content"):
            st.text_area(
                "Resume Content",
                resume_text,
                height=300
            )

        # ---------- ANALYZE BUTTON ----------
        if st.button("🚀 Analyze Resume"):

            prompt = f"""
            You are an expert career advisor and ATS specialist.

            Analyze the resume and provide the output in the following format.

            # ATS Score
            ATS Score: 85/100.

            # Skills Identified
            Separate Technical Skills and Soft Skills.

            # Strengths
            List only 3 strengths.

            # Weaknesses
            List 2 weaknesses.

            # Suitable Job Roles
            Provide the Top 5 most suitable job roles.

            For each role provide:
            - Job Role
            - Match Percentage
            - Reason

            # Missing Skills
            List important missing skills.

            # Resume Improvement Suggestions
            Provide actionable suggestions.
            and List only 3 suggestions.

            Resume:
            {resume_text}
            """

            with st.spinner("🔍 Analyzing Resume... Please wait"):
                response = model.generate_content(prompt)

            st.success("✅ Analysis Complete!")

            st.markdown("---")
            st.subheader("📊 Resume Analysis Report")
            st.markdown(response.text)

            st.markdown("<br>", unsafe_allow_html=True)

            col1, col2, col3 = st.columns([1,2,1])

            with col2:
                st.download_button(
                    label="📄 Download Analysis Report",
                    data=response.text,
                    file_name="resume_analysis_report.txt",
                    mime="text/plain",
                    use_container_width=True
                )

    except Exception as e:
        st.error(f"Error: {e}")