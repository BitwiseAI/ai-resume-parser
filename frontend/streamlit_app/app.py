import io, os
import requests
import streamlit as st
import pandas as pd
from config import API_URL

st.set_page_config(layout="wide")

# --- Helper function to read sample files ---
def read_sample_file(filename):
    # Construct path relative to this script's location
    # frontend/streamlit_app/app.py -> data/samples/filename
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "..", "..", "data", "samples", filename)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"Sample file not found at {file_path}"

# --- Settings Sidebar ---
st.sidebar.header("Settings")
api_url = st.sidebar.text_input("API URL", value=API_URL)
model_name = st.sidebar.selectbox("Model", ["gpt-4o-mini", "gpt-4o"], index=0)
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.2, 0.1)
demo_password = st.sidebar.text_input("Demo password", type="password")

headers = {}
if demo_password:
    headers["Authorization"] = f"Bearer {demo_password}"

st.title("Resume ↔ JD Parser & Fit Scorer")

# --- Tabs for Single and Batch mode ---
tab_single, tab_batch, tab_history = st.tabs(["Single Parse", "Batch Parse", "Recent Runs"])

with tab_single:
    col1, col2 = st.columns(2)
    with col1:
        resume_text = st.text_area("Resume", value=read_sample_file("sample_resume.txt"), height=300)
    with col2:
        job_text = st.text_area("Job Description", value=read_sample_file("sample_job.txt"), height=300)

    if st.button("Parse & Score"):
        if not resume_text or not job_text:
            st.error("Resume and Job Description cannot be empty.")
        else:
            with st.spinner("Parsing..."):
                try:
                    r = requests.post(
                        f"{api_url}/parse",
                        json={
                            "resume_text": resume_text, 
                            "job_text": job_text,
                            "model": model_name,
                            "temperature": temperature
                        },
                        headers=headers,
                        timeout=60
                    )
                    if r.ok:
                        data = r.json()
                        st.subheader("Result")
                        st.write(f"**Score:** {data.get('score')}/100")
                        st.write(f"**Skills:** {', '.join(data.get('skills', []))}")
                        st.write(f"**Reasons:** {data.get('reasons')}")
                        st.json(data)
                    else:
                        st.error(f"API Error: {r.status_code} - {r.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Connection Error: {e}")

with tab_batch:
    st.header("Batch Resume Parsing")
    jd_batch = st.text_area("Job Description (applies to all resumes)", height=180, key="jd_batch", value=read_sample_file("sample_job.txt"))
    files = st.file_uploader("Upload multiple resume .txt files", type=["txt"], accept_multiple_files=True)
    
    if st.button("Run Batch Parse"):
        if not jd_batch or not files:
            st.error("Job Description and at least one resume file are required.")
        else:
            with st.spinner(f"Parsing {len(files)} resumes..."):
                rows = []
                progress_bar = st.progress(0)
                for i, f in enumerate(files):
                    resume_text_batch = f.read().decode("utf-8", errors="ignore")
                    try:
                        r = requests.post(
                            f"{api_url}/parse", 
                            json={
                                "resume_text": resume_text_batch, 
                                "job_text": jd_batch,
                                "model": model_name,
                                "temperature": temperature
                            }, 
                            headers=headers, 
                            timeout=60
                        )
                        if r.ok:
                            data = r.json()
                            rows.append({
                                "file": f.name,
                                "score": data.get("score"),
                                "skills": ", ".join(data.get("skills", [])[:10]),
                                "reasons": data.get("reasons", "")[:200]
                            })
                        else:
                            rows.append({"file": f.name, "score": None, "skills": "", "reasons": f"ERROR {r.status_code} - {r.text}"})
                    except requests.exceptions.RequestException as e:
                        rows.append({"file": f.name, "score": None, "skills": "", "reasons": f"CONNECTION_ERROR: {e}"})
                    progress_bar.progress((i + 1) / len(files))

            if rows:
                df = pd.DataFrame(rows)
                st.dataframe(df, use_container_width=True)
                
                # --- Download Buttons ---
                col_csv, col_excel = st.columns(2)
                with col_csv:
                    st.download_button("📥 Download CSV", df.to_csv(index=False).encode('utf-8'), "batch_results.csv", "text/csv")
                with col_excel:
                    xlsx_buf = io.BytesIO()
                    with pd.ExcelWriter(xlsx_buf, engine="xlsxwriter") as writer:
                        df.to_excel(writer, sheet_name="results", index=False)
                    st.download_button("📊 Download Excel", xlsx_buf.getvalue(), "results.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

with tab_history:
    st.header("Recent Runs")
    if st.button(
        "Refresh History"):
        try:
            r = requests.get(f"{api_url}/runs?limit=20", headers=headers, timeout=15)
            if r.ok:
                items = r.json().get("items", [])
                if items:
                    st.write(f"Showing {len(items)} latest runs")
                    hist_df = pd.DataFrame(items)
                    st.dataframe(hist_df, use_container_width=True)
                else:
                    st.info("No runs yet.")
            else:
                st.warning(f"Runs fetch failed: {r.status_code} - {r.text}")
        except Exception as e:
            st.error(f"Runs fetch error: {e}")
