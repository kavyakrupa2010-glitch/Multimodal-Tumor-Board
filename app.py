import streamlit as st
import os

from vision_tool import analyze_pathology_image
from board_orchestrator import run_tumor_board

st.set_page_config(page_title="Multimodal Tumor Board", page_icon="🩺", layout="wide")

# Modern, clean aesthetics
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6
    }
    .main {
        background-color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    .stButton>button {
        background-color: #2e66ff;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
        box-shadow: 0 4px 6px rgba(50, 50, 93, 0.11), 0 1px 3px rgba(0, 0, 0, 0.08);
        transition: all 0.15s ease;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 7px 14px rgba(50, 50, 93, 0.1), 0 3px 6px rgba(0, 0, 0, 0.08);
        background-color: #1b53ed;
    }
    h1, h2, h3 {
        color: #111827;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

st.title("🩺 Multimodal Tumor Board")
st.subheader("Powered by CrewAI + Gemini Vision")

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    api_key_input = st.text_input("Gemini API Key", type="password", help="Get this from Google AI Studio")
    if api_key_input:
        os.environ["GEMINI_API_KEY"] = api_key_input
        st.success("API Key registered for this session.")
    else:
        st.warning("Please enter your Gemini API Key to run the board.")
        
    st.divider()
    st.markdown("""
    **Agents in this Board:**
    - 🔬 **Chief Pathologist**
    - 🩻 **Lead Radiologist**
    - 🩺 **Chief Oncologist**
    """)

col1, col2 = st.columns([1, 1.5])

with col1:
    st.header("1. Case Inputs")
    uploaded_image = st.file_uploader("Upload Pathology Slide (.jpg, .png)", type=["jpg", "jpeg", "png"])
    
    patient_history = st.text_area(
        "Patient History & Notes", 
        value="Patient is a 58-year-old male presenting with a chronic cough and recent weight loss. A chest CT showed a 3cm upper right lobe mass. A biopsy was subsequently performed.",
        height=150
    )
    
    start_board = st.button("🚀 Start Tumor Board Analysis", use_container_width=True)

with col2:
    st.header("2. Board Discussion & Verdict")
    
    if start_board:
        if not os.getenv("GEMINI_API_KEY"):
            st.error("Please enter a Gemini API Key in the sidebar.")
        elif not uploaded_image:
            st.error("Please upload a pathology slide image.")
        else:
            with st.spinner("Step 1: Gemini Vision analyzing the pathology slide..."):
                # Save the uploaded file temporarily
                temp_path = f"temp_{uploaded_image.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_image.getbuffer())
                
                # Run vision model
                vision_analysis = analyze_pathology_image(temp_path)
                
                with st.expander("🔬 Raw Vision Analysis (Gemini Flash)", expanded=False):
                    st.write(vision_analysis)
                    
            with st.spinner("Step 2: Tumor Board Agents discussing the case... (This takes 30-60 secs)"):
                try:
                    final_verdict = run_tumor_board(vision_analysis, patient_history)
                    
                    st.success("Tumor Board Consensus Reached!")
                    st.markdown("### 📋 Final Tumor Board Verdict")
                    st.markdown(final_verdict)
                except Exception as e:
                    st.error(f"Agent Orchestration Failed: {str(e)}")
                    st.info("Tip: Check if the Gemini API Key is valid and has sufficient quota.")
                    
            # Cleanup temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
    else:
        st.info("Upload inputs and click 'Start Tumor Board Analysis' to see the agents in action.")
