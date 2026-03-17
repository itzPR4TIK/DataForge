# 🔥 DataForge

Turn any CSV file into a clean, professional PDF report instantly.

## What it does
- Upload any CSV file
- Instantly see data preview and statistics
- Generate bar, line, pie and horizontal bar charts
- Download a fully formatted PDF report

## Tech Stack
- **Python** — core language
- **Streamlit** — web UI
- **Pandas** — data processing
- **Matplotlib** — chart generation
- **ReportLab** — PDF generation

## How to Run

1. Clone the repository
   git clone https://github.com/itzPR4TIK/DataForge.git

2. Install dependencies
   pip install -r requirements.txt

3. Run the app
   streamlit run app.py

4. Open browser at http://localhost:8501

## Project Structure
DataForge/
├── app.py                  → Streamlit UI
├── requirements.txt        → dependencies
├── sample_data/
│   └── sales.csv           → sample data for testing
└── utils/
    ├── data_processor.py   → CSV reading and analysis
    ├── chart_generator.py  → chart generation
    └── pdf_generator.py    → PDF building