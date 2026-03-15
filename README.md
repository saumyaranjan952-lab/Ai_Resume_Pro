# AI-Based Resume Analyzer and Skill Gap Detection System

This project is a complete AI-based application built with Python and Streamlit. It allows users to upload their resumes (PDF or DOCX), extracts text, analyzes it against predefined job roles using Natural Language Processing (NLP), and detects skill gaps. It also provides a score, matches visualizations, and generates a downloadable PDF report.

## Features
- **Resume Text Extraction:** Extracts text seamlessly from PDF or DOCX files.
- **NLP-based Skill Extraction:** Utilizes `spaCy` to process natural text.
- **Predefined Database:** Comes with a predefined dataset of roles & their required skills.
- **Skill Gap Detection:** Compares extracted skills with required ones.
- **Match Percentage Calculation:** Provides a resume score out of 100 based on matching skills.
- **Data Visualizations:** Interactive Plotly pie charts mapping the discovered skills.
- **Downloadable Reports:** Offers the user a PDF export generated via `ReportLab`.
- **Clean UI:** Streamlit Web UI prioritizing user experience.

## Project Structure
```text
ResumeAnalyzer/
│
├── app.py                # Main Streamlit application
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
├── data/
│   └── job_roles.json    # Predefined dataset for roles & skills
└── utils/
    ├── __init__.py       # Package initializer
    ├── extractor.py      # Functions for PDF/DOCX text extraction
    └── analyzer.py       # Functions for NLP analysis and skill match algorithms
```

## Setup & Running the Project

1. **Navigate to the Project Directory**
   Open your terminal or command prompt and change directory to the project folder:
   ```bash
   cd "d:/clg project/PYTHON/ResumeAnalyzer"
   ```

2. **Create a Virtual Environment (Optional but Recommended)**
   ```bash
   python -m venv venv
   
   # Activate on Windows
   venv\Scripts\activate
   
   # Activate on Linux/Mac
   source venv/bin/activate
   ```

3. **Install Dependencies**
   Install all necessary libraries (including `streamlit`, `spacy`, `PyPDF2`, `python-docx`):
   ```bash
   pip install -r requirements.txt
   ```
   *Note: If `spaCy` has trouble auto-downloading its model from the requirement list, you can manually run:*
   `python -m spacy download en_core_web_sm`

4. **Launch the Application**
   ```bash
   streamlit run app.py
   ```

5. **Access the Web Interface**
   Once launched, it should automatically open your browser to `http://localhost:8501`. Upload a `.pdf` or `.docx` resume, select your target role, and view the AI's analysis!
