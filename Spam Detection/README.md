# 📧 AI Spam Detector (Machine Learning + NLP)

A high-accuracy spam detection system built using Machine Learning and Natural Language Processing (NLP). This project classifies messages as **Spam** or **Not Spam (Ham)** using TF-IDF and Support Vector Machine (SVM), with a user-friendly Tkinter GUI.

---

## 📸 Demo / Preview

![Demo](https://github.com/eshwarg14/AI-ML/raw/3b93621a73af51b3f3ddcb676032cf60c4a4a1ab/Images/SD.png)
![Demo](https://github.com/eshwarg14/AI-ML/raw/3b93621a73af51b3f3ddcb676032cf60c4a4a1ab/Images/SD1.png)

---

## ✨ Features

- 📧 Detects spam messages instantly  
- 🧠 Uses NLP for text preprocessing  
- 🤖 Machine Learning model (SVM)  
- 📊 Displays model accuracy  
- 🖥️ GUI-based application (Tkinter)  
- ⚡ Fast prediction  

---

## 🧠 Concepts Used

### 🔹 Natural Language Processing (NLP)
Used to clean and process text data:
- Lowercasing  
- Removing punctuation  
- Removing stopwords  
- Lemmatization  

---

### 🔹 Machine Learning (ML)
Used to classify messages:
- TF-IDF Vectorization  
- Support Vector Machine (SVM)  

---

## 🧠 Technologies Used

```
pandas
nltk
scikit-learn
tkinter
```

📦 Install dependencies:

```bash
pip install pandas nltk scikit-learn
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
├── spam.csv       # Dataset (place in same folder as main.py)
├── Images/        # Demo screenshots
└── README.md
```

---

## 📊 Dataset

- 📄 File: `spam.csv`  
- 📍 **Place this file directly in the same folder as `main.py`**  
- Contains labeled messages:
  - `spam` → unwanted messages  
  - `ham` → normal messages  

---

## 🛠️ Step-by-Step Working

### 1️⃣ Data Loading
- Dataset is loaded using pandas  
- Columns cleaned and renamed  

---

### 2️⃣ Text Preprocessing (NLP)

Function: `clean_text()`

- Convert text to lowercase  
- Remove punctuation  
- Remove stopwords (e.g., "is", "the")  
- Apply lemmatization (e.g., "running" → "run")  

---

### 3️⃣ Feature Extraction (TF-IDF)

- Converts text into numerical format  
- Important words get higher weight  
- Uses:
  - Unigrams + Bigrams  
  - Max 5000 features  

---

### 4️⃣ Model Training

- Algorithm: **Linear SVM (Support Vector Machine)**  
- Splits data:
  - 80% training  
  - 20% testing  

---

### 5️⃣ Model Evaluation

- Accuracy calculated using:
```text
accuracy_score()
```

👉 Displays accuracy in GUI

---

### 6️⃣ Prediction (GUI)

- User enters message  
- Text is cleaned  
- Converted to vector  
- Model predicts:

```
1 → Spam  
0 → Not Spam
```

---

### 7️⃣ Output Display

- ⚠️ SPAM DETECTED (Red)  
- ✅ NOT SPAM (Green)  

---

## ⚠️ Important Notes

- 🐍 Python 3.8+ required  
- 📏 Accuracy depends on dataset quality  
- 💡 Works better with proper sentences  

---

## 🔧 Important Fix

Update your dataset path:

```python
df = pd.read_csv("spam.csv", encoding="latin-1")
```

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
