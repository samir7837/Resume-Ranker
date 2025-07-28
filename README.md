# 📊 Resume Ranker for Recruiters

An AI-powered Streamlit web app to **rank resumes against a job description**, helping recruiters quickly shortlist the best candidates. Upload multiple resumes, compare them semantically to a job description, and get a ranked, actionable shortlist—instantly!

---

## 🚀 Features

- **Upload multiple resumes** (PDF or DOCX)
- **Paste or select a job description** (built-in templates or custom)
- **Automatic resume parsing** for text extraction
- **Semantic ranking** using state-of-the-art embeddings (SBERT)
- **Top 10 results** with match scores (%)
- **Missing keywords** per resume (see what’s NOT in a candidate’s resume)
- **Preview PDF resumes in-browser**
- **Download or View** each resume with one click
- **Clean, responsive UI** built with Streamlit

---

## 📦 Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/YOUR-USERNAME/resume-ranker.git
    cd resume-ranker
    ```

2. **(Recommended) Create a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

---

## ▶️ Usage

1. **Run the Streamlit app:**
    ```sh
    streamlit run app.py
    ```

2. **Open your browser** (Streamlit will print a local URL, usually [http://localhost:8501](http://localhost:8501))

3. **Follow the instructions in the app:**
    - Select or paste a job description
    - Upload one or more resumes (PDF or DOCX)
    - View ranked results, missing keywords, and download or preview resumes

---

## 🛠️ Project Structure

```
resume-ranker/
│
├── app.py                     # Main Streamlit app
├── requirements.txt           # Python dependencies
├── README.md                  # Project overview & instructions
│
├── utils/                     # Utility modules
│   ├── parsing.py             # Resume/job description parsing logic
│   ├── similarity.py          # Embedding & similarity functions
│   └── keyword_extraction.py  # Functions to extract keywords
│
├── static/                    # For storing uploaded/viewable resumes
└── .streamlit/                # Streamlit configuration (optional)
```

---

## 🧠 How it Works

- **Parsing:** Extracts text from PDFs (using `pdfplumber`) and DOCX files (`python-docx`).
- **Embeddings:** Uses [sentence-transformers](https://www.sbert.net/) (`all-MiniLM-L6-v2`) for semantic similarity.
- **Ranking:** Calculates cosine similarity between job description and each resume.
- **Keyword Extraction:** Uses [KeyBERT](https://github.com/MaartenGr/KeyBERT) to find top keywords from the job description and highlight missing ones in each resume.
- **UI:** Built with Streamlit for instant web-based interaction.

---

## 📝 Example Job Descriptions

- Data Scientist
- Software Engineer
- *(Or paste your own!)*

---

## 📚 Requirements

- Python 3.8+
- See `requirements.txt` for full list

---

## 🖼️ Credits

- [Streamlit](https://streamlit.io/)
- [Sentence-Transformers (SBERT)](https://www.sbert.net/)
- [KeyBERT](https://github.com/MaartenGr/KeyBERT)
- [pdfplumber](https://github.com/jsvine/pdfplumber)
- [python-docx](https://python-docx.readthedocs.io/en/latest/)

---

## 🛡️ License

MIT

---

## 🤝 Contributing

Pull requests, suggestions, and issues are welcome!

---

## ✨ Author

Built with ❤️ by Samir](https://github.com/samir7837)
