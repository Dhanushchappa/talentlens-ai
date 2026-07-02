import streamlit as st
import pandas as pd
import pdfplumber
import re
import plotly.express as px
import io
from sentence_transformers import CrossEncoder
from PIL import Image
logo = Image.open("ml logo.png")


# ================= LOAD SKILLS =================
@st.cache_resource
def load_model():
    return CrossEncoder(
        "cross-encoder/ms-marco-MiniLM-L-6-v2"
    )

cross_model = load_model()


# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="TalentLens AI",
    page_icon=logo,
    layout="wide",
    initial_sidebar_state="expanded"
)


# ================= PREMIUM SAAS CSS =================
st.markdown("""
<style>

/* Main Background */
html, body, .stApp, [data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at top right, rgba(59,130,246,0.35), transparent 30%),
        radial-gradient(circle at bottom left, rgba(6,182,212,0.25), transparent 30%),
        linear-gradient(135deg, #0f172a, #1e3a8a) !important;
    color: white;
}

/* Remove header */
header, [data-testid="stHeader"] {
    background: transparent !important;
}

[data-testid="stToolbar"] {
    visibility: visible !important;
}

/* Optional: make toolbar blend with background */
[data-testid="stToolbar"] > div {
    background: transparent !important;
}
/* Typography */
h1, h2, h3, h4, h5, h6, p, label, span, div {
    color: white !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(17, 24, 39, 0.90);
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255,255,255,0.12);
}

/* Buttons */
.stButton > button {
    width: 100%;
    height: 3em;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.15);
    font-weight: bold;
    color: white;
    background: rgba(37,99,235,0.45);
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 32px rgba(6,182,212,0.35);
}

/* Uploaders + radio */
[data-testid="stFileUploader"],
[data-testid="stRadio"] {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
    padding: 12px;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.12);
}

/* Text Area */
textarea {
    border-radius: 12px !important;
}

/* Tables */
[data-testid="stDataFrame"] {
    background: rgba(255,255,255,0.05);
    border-radius: 16px;
}

/* Metric Cards */
.metric-card {
    background: rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.15);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    backdrop-filter: blur(14px);
    text-align: center;
    transition: all 0.3s ease;
}

.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 36px rgba(6,182,212,0.35);
}
/* Candidate Cards */
.candidate-card {
    background: rgba(255,255,255,0.06);
    padding: 20px;
    border-radius: 18px;
    margin-bottom: 15px;
    border: 1px solid rgba(255,255,255,0.12);
    backdrop-filter: blur(14px);
}

</style>
""", unsafe_allow_html=True)

# ================= TITLE =================
col1, col2 = st.columns([1, 5])

with col1:
    st.image(logo, width=120)

with col2:
    st.markdown("""
    <h1 style='color:white; margin-bottom:0;'>
        TalentLens AI
    </h1>
    <h4 style='color:#cbd5e1; font-weight:400; margin-top:0;'>
        AI Resume Analyzer & Hiring Assistant
    </h4>
    """, unsafe_allow_html=True)
# ================= FUNCTIONS =================
def extract_pdf_text(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text


def extract_txt_text(uploaded_file):
    return uploaded_file.read().decode("utf-8")


def clean(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def extract_keywords(text):
    text = clean(text)
    words = set(text.split())

    # remove tiny words
    keywords = {w for w in words if len(w) > 2}

    return keywords

def skill_match_score(resume_text, jd_text):
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(jd_text)

    if len(jd_keywords) == 0:
        return 50

    matched = resume_keywords.intersection(jd_keywords)

    score = (len(matched) / len(jd_keywords)) * 100
    return round(score, 2)




import math
def convert_to_ats(raw_score, skill_score):
    # Semantic score from CrossEncoder (-10 to +10 → 0–100)
    semantic_score = ((raw_score + 10) / 20) * 100
    semantic_score = max(0, min(100, semantic_score))

    final_score = (0.6 * semantic_score) + (0.4 * skill_score)

    return round(final_score, 2)



def explain_score(score):
    if score >= 90:
        return (
            "Highly Suitable",
            "The resume strongly aligns with the job description."
        )
    elif score >= 75:
        return (
            "Suitable",
            "The resume matches most job requirements with minor gaps."
        )
    elif score >= 55:
        return (
            "Moderately Suitable",
            "The resume partially matches the job description."
        )
    else:
        return (
            "Not Suitable",
            "The resume shows limited alignment with the job description."
        )


# ================= SIDEBAR INPUT PANEL =================
with st.sidebar:
    st.image(logo, width=180)
    st.markdown("## TalentLens AI")

    st.markdown("## 📥 Input Panel")

    resume_files = st.file_uploader(
        "Upload Resumes (PDF or TXT)",
        type=["pdf", "txt"],
        accept_multiple_files=True
    )

    jd_option = st.radio(
        "Job Description Input Method",
        ["Paste Text", "Upload PDF", "Upload TXT"]
    )

    job_description = ""

    if jd_option == "Paste Text":
        job_description = st.text_area(
            "Paste Job Description",
            height=200
        )

    elif jd_option == "Upload PDF":
        jd_file = st.file_uploader(
            "Upload JD PDF",
            type=["pdf"],
            key="jd_pdf"
        )
        if jd_file:
            job_description = extract_pdf_text(jd_file)

    elif jd_option == "Upload TXT":
        jd_file = st.file_uploader(
            "Upload JD TXT",
            type=["txt"],
            key="jd_txt"
        )
        if jd_file:
            job_description = extract_txt_text(jd_file)

    analyze = st.button("Analyze Resume")


# ================= ANALYSIS =================
if analyze:

    if resume_files and job_description:

        # ================= ATS =================
        results = []

        for resume_file in resume_files:

            if resume_file.name.endswith(".pdf"):
                resume_text = extract_pdf_text(resume_file)
            else:
                resume_text = extract_txt_text(resume_file)

            raw_score = cross_model.predict(
                [(resume_text, job_description)]
            )[0]

            skill_score = skill_match_score(
                resume_text,
                job_description
            )

            score = round(convert_to_ats(
                raw_score,
                skill_score
            ),1)

            label, explanation = explain_score(score)

            results.append((
                resume_file.name,
                score,
                label,
                explanation
            ))

        results = sorted(results, key=lambda x: x[1], reverse=True)

        total_resumes = len(results)
        best_score = round(results[0][1], 2)
        avg_score = round(sum(r[1] for r in results) / len(results), 2)

        # ================= KPI CARDS =================
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <h4>📄 Total Resumes</h4>
                    <h2>{total_resumes}</h2>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <h4>🏆 Best ATS Score</h4>
                    <h2>{best_score:.1f}%</h2>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f"""
                <div class="metric-card">
                    <h4>📊 Avg ATS Score</h4>
                    <h2>{avg_score:.1f}%</h2>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("---")

        # ================= HR ANALYTICS =================
        st.subheader("📈 HR Analytics Dashboard")

        chart_df = pd.DataFrame(
            results,
            columns=["Resume", "Score", "Suitability", "Explanation"]
        )

        col1, col2 = st.columns(2)

        with col1:
            fig_score = px.bar(
                chart_df,
                x="Resume",
                y="Score",
                title="ATS Score by Resume",
                text="Score"
            )
            st.plotly_chart(fig_score, use_container_width=True)

        st.markdown("---")

        # ================= CANDIDATE CARDS =================
        for i, (name, score, label, explanation) in enumerate(results, 1):
            st.markdown(
                f"""
                <div class="candidate-card">
                    <h3>#{i} — {name}</h3>
                    <p><b>ATS Score:</b> {score:.1f}%</p>
                    <p><b>Suitability:</b> {label}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.info(explanation)

        # ================= TABLE =================
        df_results = pd.DataFrame(
            results,
            columns=["Resume", "Score", "Suitability", "Explanation"]
        )

        df_results["Score"] = df_results["Score"].round(1)

        st.subheader("🏆 Resume Ranking")
        st.dataframe(df_results, use_container_width=True)

        # ================= DOWNLOAD OPTIONS =================
        csv = df_results.to_csv(index=False).encode("utf-8")

        excel_buffer = io.BytesIO()

        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
            df_results.to_excel(
                writer,
                index=False,
                sheet_name="Ranking"
            )

        excel_data = excel_buffer.getvalue()

        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name="resume_ranking.csv",
                mime="text/csv",
                use_container_width=True
            )

        with col2:
            st.download_button(
                label="📊 Download Excel",
                data=excel_data,
                file_name="resume_ranking.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

    else:
        st.warning("Upload resumes and job description first")


