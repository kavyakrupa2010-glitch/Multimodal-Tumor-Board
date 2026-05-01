# Multimodal AI Tumor Board 🩺

A demonstration of a Multimodal, Multi-Agent AI system designed to simulate a clinical Tumor Board.

Traditional AI diagnostic tools often act as "black boxes," outputting probability scores without explaining their reasoning. This project solves that by using **CrewAI** to orchestrate a transparent, step-by-step debate between three distinct AI medical personas. It also leverages the **Google Gemini API** to process raw pathology slide images directly, bypassing the need for complex, custom-trained computer vision models.

## 🏗️ Architecture

This project is both **Multimodal** (it processes both image and text data) and **Multi-Agent** (it coordinates multiple AI personas).

1. **Presentation Layer (`app.py`):** A streamlined Streamlit web interface for uploading pathology slides and patient history.
2. **Vision Edge Layer (`vision_tool.py`):** Uses Google `gemini-2.5-flash` to "look" at the uploaded image and mathematically translate the cellular structures, atypia, and necrosis into a highly structured clinical text summary.
3. **Cognitive Orchestration Layer (`board_orchestrator.py`):** Uses CrewAI to route the data through three agents:
   - 🔬 **Chief Pathologist:** Drafts a formal pathology report based on the visual data.
   - 🩻 **Lead Radiologist:** Cross-references the pathology with the patient history to assess systemic risk.
   - 🩺 **Chief Oncologist:** Synthesizes all inputs to deliver a final, actionable treatment plan.

## 🚀 Quickstart (Local Windows/Mac)

### 1. Prerequisites
- Python 3.10 or 3.11 installed. *(Note: Python 3.14 may lack pre-compiled wheels for certain dependencies).*
- A [Google Gemini API Key](https://aistudio.google.com/).

### 2. Setup
Open your terminal and clone/navigate to this directory. Then, create a virtual environment and install dependencies:

```bash
# Create a virtual environment
python -m venv venv

# Activate it (Windows)
.\venv\Scripts\activate
# OR Activate it (Mac/Linux)
source venv/bin/activate

# Install the required packages
pip install -r requirements.txt
```

### 3. Run the Application
With the virtual environment activated, start the Streamlit server:

```bash
streamlit run app.py
```
This will automatically open the web UI at `http://localhost:8501`.

## 🐳 Quickstart (Docker)
If you prefer to run this in an isolated Ubuntu container, ensure you have Docker Desktop installed.

```bash
docker-compose up --build
```
The app will be served at `http://localhost:8501`.

## 🧪 How to Test
1. Obtain a Gemini API key and paste it into the sidebar of the web app.
2. Upload a sample pathology slide. (Two mock slides, `benign_thyroid_cyst.png` and `lung_adenocarcinoma.png`, are included in this repo for immediate testing).
3. Provide a brief patient history.
4. Click **"Start Tumor Board Analysis"** and watch the agents collaborate!
