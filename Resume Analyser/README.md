# 📄 AI ATS Resume Analyzer

An advanced AI-powered Resume Analyzer that evaluates resumes against job descriptions using ATS (Applicant Tracking System) logic. Built with Python, Tkinter, and AI APIs, this tool provides **ATS score, keyword analysis, strengths, and improvements**.

---

## Preview

![Demo](Images/ats1.png)
![Demo](Images/ats2.png)

---

## ✨ Features

- 📄 Upload or paste resume (PDF/TXT supported)  
- 📋 Analyze against job description  
- 🤖 AI-powered ATS evaluation  
- 📊 ATS Score (0–100)  
- 🔍 Keyword matching & missing keywords  
- 💪 Strengths & improvement suggestions  
- 📈 Section-wise scoring  
- ⚡ Quick fixes for resume optimization  
- 🖥️ Modern GUI with Tkinter  

---

## 🧠 What is ATS?

**ATS (Applicant Tracking System)** is software used by companies to:

- Filter resumes  
- Match keywords  
- Rank candidates  

👉 If your resume doesn’t match ATS → it may be rejected before HR sees it

---

## 🤖 How This Project Works

- 📄 Resume text is extracted (PDF or manual input)  
- 📋 Job description is provided  
- 🤖 AI analyzes:
  - Skills match  
  - Keywords  
  - Experience relevance  
- 📊 Outputs structured JSON:
  - ATS Score  
  - Strengths  
  - Weaknesses  
  - Suggestions  

---

## 🧠 Technologies Used

```
tkinter
requests
threading
json
PyPDF2
```

📦 Install dependencies:

```bash
pip install requests PyPDF2
```

---

## ▶️ How to Run

```bash
python main.py
```

---

## 📁 Project Structure

```
├── main.py        # Main application
└── README.md
```

---

## 📄 Resume Input Options

- ✏️ Paste resume text  
- 📄 Upload PDF file  
- 📃 Upload TXT file  

---

## 🔑 API Setup

1. 🌐 Go to: https://openrouter.ai  
2. 🔐 Login / Signup  
3. 🔑 Generate API key  

Replace in code:

```python
API_KEY = "your-api-key"
```

---

## 🛠️ How It Works (Detailed)

### 1️⃣ Input Processing
- Resume text extracted  
- Job description provided  

---

### 2️⃣ AI Analysis

- Sent to AI model via API  
- Model returns structured JSON  

---

### 3️⃣ Parsing & Validation

- Cleans invalid JSON  
- Handles incomplete responses  

---

### 4️⃣ Output Visualization

- 🎯 Circular ATS score  
- 📊 Section-wise bar graph  
- 🟢 Matched keywords  
- 🔴 Missing keywords  
- 📋 Strengths & improvements  

---

## 📊 Output Example

- ATS Score: 78/100  
- Matched Keywords: Python, ML, Data Analysis  
- Missing Keywords: SQL, Docker  
- Improvements: Add projects, optimize skills section  

---

## ⚠️ Requirements

- 🐍 Python 3.8+  
- 🌐 Internet connection  
- 🔑 OpenRouter API key  

---

## 👨‍💻 Authors

**Eshwar G & Shivani R**

---

## 📄 License

This project is licensed under the MIT License.

---

## ⭐ Support

If you like this project:

- ⭐ Star the repo  
- 🍴 Fork it  
- 🛠️ Contribute  

---

## 🚀 Future Improvements

- Resume auto-builder 📄  
- LinkedIn profile analysis 🔗  
- Multi-job comparison 📊  
- Cloud deployment ☁️  
