import streamlit as st
import os
import base64
from utils.parsing import extract_text
from utils.similarity import get_embedding, compute_similarity
from utils.keyword_extraction import extract_keywords, find_missing_keywords

# --- PDF Preview Helper ---
def show_pdf(file_path):
    """Embed a PDF file in the Streamlit app using an HTML iframe."""
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="700" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# --- Streamlit Page Config ---
st.set_page_config(page_title="Resume Ranker for Recruiters", layout="wide")

# --- App Title & Intro ---
st.title("📊 Resume Ranker for Recruiters")
st.markdown("""
Welcome to the **AI-powered resume ranking tool!**

#### Instructions:
<ol>
<li>Select a job role or paste your job description below.</li>
<li><b>Upload multiple resumes</b> (PDF or DOCX).</li>
<li>Get a ranked list with match scores, missing keywords, and quick view/download options.</li>
</ol>
""", unsafe_allow_html=True)

UPLOAD_DIR = "static"

# --- 1. Job Description Input Section ---
with st.container():
    st.header("1️⃣ Enter Job Description")
    job_roles = {
        "Data Scientist": """Responsibilities:
- Build predictive models using Python
- Analyze large datasets
- Communicate results to stakeholders
Requirements:
- Experience with machine learning and data analysis
- Strong Python skills
- Knowledge of SQL and data visualization tools""",
        "Software Engineer": """Responsibilities:
- Develop scalable applications
- Write clean, maintainable code
- Collaborate in agile teams
Requirements:
- Proficiency in Python, Java, or C++
- Experience with databases
- Familiarity with cloud platforms"""
    }
    jd_choice = st.radio(
        "Choose a job role template or paste your own:",
        ("Data Scientist", "Software Engineer", "Custom"),
        horizontal=True
    )
    if jd_choice == "Custom":
        job_description = st.text_area("Paste the Job Description here:", height=180)
    else:
        job_description = job_roles[jd_choice]
        st.text_area("Job Description", value=job_description, height=180, disabled=True)

    if not job_description.strip():
        st.warning("⚠️ Please provide a job description to continue.")

# --- 2. Resume Upload Section ---
st.header("2️⃣ Upload Resumes")
uploaded_files = st.file_uploader(
    "Upload one or more resumes (PDF or DOCX):",
    type=["pdf", "docx"],
    accept_multiple_files=True,
    help="You can select multiple files at once."
)

resume_texts, resume_filenames, resume_paths = [], [], []

if uploaded_files:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    for uploaded_file in uploaded_files:
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        text = extract_text(file_path)
        if text:
            resume_texts.append(text)
            resume_filenames.append(uploaded_file.name)
            resume_paths.append(file_path)
        else:
            st.error(f"❌ Could not extract text from: {uploaded_file.name}")

if resume_texts:
    # Show sample resume text
    with st.expander("📝 Show sample parsed resume text"):
        st.write(resume_texts[0][:1500] + "...")

# --- 3. Ranking and Results Section ---
if job_description.strip() and resume_texts:
    st.header("3️⃣ Ranking Results")

    # Compute embeddings and extract JD keywords just once
    jd_embedding = get_embedding(job_description)
    jd_keywords = extract_keywords(job_description, num_keywords=8)

    # Prepare results
    results = []
    for i, resume_text in enumerate(resume_texts):
        resume_embedding = get_embedding(resume_text)
        score = compute_similarity(jd_embedding, resume_embedding)
        missing = find_missing_keywords(jd_keywords, resume_text)
        results.append({
            "filename": resume_filenames[i],
            "score": score,
            "missing_keywords": missing,
            "path": resume_paths[i]
        })

    # Sort by score
    results = sorted(results, key=lambda x: x['score'], reverse=True)

    # --- Top 10 List ---
    st.subheader("🏅 Top Ranked Resumes")
    for idx, res in enumerate(results[:10]):
        with st.container():
            cols = st.columns([3, 2, 4])
            # Filename and score
            cols[0].markdown(f"**{idx+1}. {res['filename']}**")
            cols[1].markdown(f"🔢 **Match Score:** `{res['score']*100:.2f}%`")
            # Download/View buttons
            with open(res['path'], "rb") as file_data:
                btn1, btn2 = cols[2].columns(2)
                # View (opens PDF in browser for PDFs)
                if res['filename'].lower().endswith(".pdf"):
                    with btn1:
                        if st.button("👁️ View", key=f"view_{idx}"):
                            st.info("PDF preview opens below. Scroll to view.")
                            show_pdf(res['path'])
                else:
                    btn1.write("📄 No preview")

                # Download
                with btn2:
                    st.download_button(
                        label="⬇️ Download",
                        data=file_data,
                        file_name=res['filename'],
                        mime="application/octet-stream",
                        key=f"dl_{idx}"
                    )
            # Missing keywords
            if res['missing_keywords']:
                cols[0].markdown(
                    f"<span style='color:#ff5733'><b>Missing keywords:</b> {', '.join(res['missing_keywords'])}</span>",
                    unsafe_allow_html=True
                )
            else:
                cols[0].markdown("<span style='color:green'>✅ All key JD keywords found!</span>", unsafe_allow_html=True)
        st.markdown("---")

# --- Footer ---
st.markdown(
    "<div style='text-align:center; color:gray; font-size:0.9em;'>"
    "Made with ❤️ using Streamlit & SBERT | <a href='https://github.com/samir7837' target='_blank'>GitHub</a>"
    "</div>", unsafe_allow_html=True
)