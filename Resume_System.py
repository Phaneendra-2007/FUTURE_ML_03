import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="AI Resume Screener", layout="wide")

# -----------------------------
# FORCE WHITE UI
# -----------------------------
st.markdown("""
<style>
.stApp {
    background-color: #ffffff;
    color: #000000;
}

/* Inputs */
textarea, input {
    background-color: #f9fafb !important;
    color: black !important;
}

/* Buttons */
button {
    background-color: #2563eb !important;
    color: white !important;
    border-radius: 8px;
}

/* Cards text fix */
h1, h2, h3, h4, h5, h6, p, label {
    color: black !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.title("🧠 AI Resume Screening Dashboard")
st.caption("Smart hiring assistant using Machine Learning & NLP")

# -----------------------------
# LAYOUT
# -----------------------------
col1, col2 = st.columns(2)

# -----------------------------
# LEFT SIDE
# -----------------------------
with col1:
    st.subheader("📌 Job Profile")

    job_desc = st.text_area("Job Description", height=200)

    skills_input = st.text_input(
        "Required Skills (comma separated)",
        "python, machine learning, sql"
    )

    st.markdown("### 🎯 Target Skills")
    skills = [s.strip().lower() for s in skills_input.split(",")]

    for skill in skills:
        st.markdown(f"- 🔹 {skill}")

# -----------------------------
# RIGHT SIDE
# -----------------------------
with col2:
    st.subheader("📂 Resume Upload")

    uploaded_files = st.file_uploader(
        "Upload Resumes (TXT only)",
        accept_multiple_files=True,
        type=["txt"]
    )

    if uploaded_files:
        st.success(f"{len(uploaded_files)} file(s) uploaded")

# -----------------------------
# BUTTON
# -----------------------------
if st.button("🚀 Run Screening"):

    if not job_desc:
        st.warning("⚠️ Please enter job description")

    else:
        resumes = []
        names = []

        # Read uploaded files
        if uploaded_files:
            for file in uploaded_files:
                content = file.read().decode("utf-8")
                resumes.append(content)
                names.append(file.name)
        else:
            # Sample resumes
            names = ["Alice", "Bob", "Charlie", "David"]
            resumes = [
                "Python ML developer with NLP experience",
                "Java backend engineer with Spring Boot",
                "Data analyst skilled in SQL and Power BI",
                "Deep learning engineer with AI research"
            ]

        # -----------------------------
        # TF-IDF MODEL
        # -----------------------------
        texts = [job_desc] + resumes

        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform(texts)

        scores = cosine_similarity(vectors[0:1], vectors[1:]).flatten()

        df = pd.DataFrame({
            "Candidate": names,
            "Resume Text": resumes,
            "Match Score (%)": scores * 100
        })

        df = df.sort_values(by="Match Score (%)", ascending=False)

        # -----------------------------
        # SKILL MATCH
        # -----------------------------
        def skill_match(resume):
            count = sum([1 for skill in skills if skill in resume.lower()])
            return (count / len(skills)) * 100 if skills else 0

        df["Skill Match (%)"] = df["Resume Text"].apply(skill_match)

        # -----------------------------
        # RESULTS TABLE
        # -----------------------------
        st.markdown("---")
        st.subheader("📊 Screening Results")

        st.dataframe(
            df[["Candidate", "Match Score (%)", "Skill Match (%)"]],
            use_container_width=True
        )

        # -----------------------------
        # TOP CANDIDATE
        # -----------------------------
        top = df.iloc[0]

        st.markdown("### 🏆 Top Candidate")
        st.success(f"{top['Candidate']} → {top['Match Score (%)']:.2f}% Match Score")

        # -----------------------------
        # WHITE CARDS UI
        # -----------------------------
        st.markdown("### 📋 Candidate Insights")

        for i, row in df.iterrows():

            if row["Match Score (%)"] > 70:
                color = "#16a34a"
            elif row["Match Score (%)"] > 40:
                color = "#f59e0b"
            else:
                color = "#dc2626"

            st.markdown(f"""
            <div style="
                background:#ffffff;
                padding:20px;
                border-radius:12px;
                margin-bottom:15px;
                border-left:5px solid {color};
                box-shadow:0px 4px 10px rgba(0,0,0,0.1);
            ">
                <h3 style="color:#111827;">👤 {row['Candidate']}</h3>
                
                <p style="color:#2563eb;">
                    Match Score: <b>{row['Match Score (%)']:.2f}%</b>
                </p>
                
                <div style="background:#e5e7eb; border-radius:10px;">
                    <div style="
                        width:{row['Match Score (%)']}%;
                        background:{color};
                        padding:6px;
                        border-radius:10px;
                        text-align:center;
                        color:white;">
                        {row['Match Score (%)']:.1f}%
                    </div>
                </div>

                <p style="color:#16a34a; margin-top:10px;">
                    Skill Match: <b>{row['Skill Match (%)']:.2f}%</b>
                </p>
            </div>
            """, unsafe_allow_html=True)