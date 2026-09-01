"""
Streamlit UI for the research agent pipeline.

This file expects your pipeline function `run_research_agent(topic: str) -> dict`
to be importable. Adjust the import line below to match wherever your pipeline
module actually lives (e.g. `from src.gen_ai.pipeline import run_research_agent`
or `from pipeline import run_research_agent`).

Run with:
    streamlit run app.py
"""
import os
import streamlit as st

# Expose Streamlit secret as an environment variable for Langchain/Mistral
if "MISTRAL_API_KEY" in st.secrets:
    os.environ["MISTRAL_API_KEY"] = st.secrets["MISTRAL_API_KEY"]

from pipeline import run_research_agent

import streamlit as st

# ---------------------------------------------------------------------------
# Adjust this import to match your project structure.
# If your pipeline code (the file with run_research_agent) is at
# src/gen_ai/pipeline.py, use:
#     from src.gen_ai.pipeline import run_research_agent
# If it's at src/gen_ai/main.py, use:
#     from src.gen_ai.main import run_research_agent
# ---------------------------------------------------------------------------
from pipeline import run_research_agent  # <-- change "pipeline" to your actual module name


st.set_page_config(
    page_title="AI Research Agent by pranjal dwivedi",
    page_icon="🔎",
    layout="wide",
)

st.title("🔎 AI Research Agent")
st.caption("Enter a topic. A search agent finds sources, a reader agent scrapes the best one, and a writer agent drafts a report.")

# Keep results across reruns
if "state" not in st.session_state:
    st.session_state.state = None

with st.form("research_form"):
    topic = st.text_input("Research topic", placeholder="e.g. Latest developments in solid-state batteries")
    submitted = st.form_submit_button("Run research", type="primary")

if submitted:
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        status_box = st.empty()
        try:
            with st.spinner("Running the research pipeline... this can take a minute."):
                status_box.info("🔍 Search agent is gathering sources...")
                result = run_research_agent(topic)
            status_box.empty()
            st.session_state.state = result
            st.success("Done! See the report below.")
        except Exception as e:
            status_box.empty()
            st.error(f"Pipeline failed: {e}")

state = st.session_state.state

if state:
    report = state.get("report")
    # writer_chain output might be a string or an object with `.content`
    report_text = getattr(report, "content", report)

    st.subheader("📄 Final Report")
    st.markdown(report_text if report_text else "_No report generated._")

    st.download_button(
        "Download report (.md)",
        data=(report_text or ""),
        file_name="research_report.md",
        mime="text/markdown",
    )

    with st.expander("🔍 Raw search results"):
        st.write(state.get("search_results", "No search results captured."))

    with st.expander("🕸️ Scraped content"):
        st.write(state.get("scraped_content", "No scraped content captured."))
else:
    st.info("Enter a topic above and click **Run research** to get started.")