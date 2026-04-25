# ❤️ AI Cardiovascular Health Monitor

An advanced AI-powered healthcare application that predicts **Cardiovascular Disease (CVD) risk** using Machine Learning. Built with Python, Tkinter, and Scikit-learn, this system provides real-time risk analysis, medical insights, and visualizations.

---

## Preview

![Demo](https://github.com/eshwarg14/AI-ML/raw/95cfd502e1f3990b1c6030068cbce8d11e49ad2e/Images/HM.png)

---

## ✨ Features

- ❤️ Predicts cardiovascular disease risk  
- 🤖 Machine Learning model (Random Forest)  
- 📊 Real-time probability visualization  
- 📈 Feature importance analysis  
- 💓 Live ECG simulation  
- 🧠 Medical insights & recommendations  
- 🖥️ Advanced GUI with Tkinter  
- 📋 Detailed patient report generation  

---

## 🧠 What is Cardiovascular Disease (CVD)?

CVD refers to conditions affecting the heart and blood vessels.

👉 Common causes:
- High blood pressure  
- High cholesterol  
- Smoking  
- Obesity  
- Lack of physical activity  

---

## 🤖 Machine Learning Model

This project uses:

### 🌳 Random Forest Classifier

- Ensemble learning method  
- Uses multiple decision trees  
- Improves accuracy and reduces overfitting  

---

## 🧠 Technologies Used

```
pandas
numpy
scikit-learn
tkinter
matplotlib
seaborn
```

📦 Install dependencies:

```bash
pip install pandas numpy scikit-learn matplotlib seaborn
```

---

## ▶️ How to Run

```bash
python main.py
```

---

## 📁 Project Structure

```
├── main.py              # Main application
├── cardio_train.csv     # Dataset (place in same folder)
└── README.md
```

---

## 📊 Dataset

- 📄 File: `cardio_train.csv`  
- 📍 Place it **in the same folder as main.py**  
- Contains patient data:
  - Age  
  - Gender  
  - Height & Weight  
  - Blood Pressure  
  - Cholesterol & Glucose  
  - Lifestyle factors  

---

## 🛠️ Step-by-Step Working

### 1️⃣ Data Loading
- Dataset loaded using pandas  
- Removes invalid columns  

---

### 2️⃣ Data Preprocessing

- Convert age from days → years  
- Calculate BMI  
- Remove invalid/outlier values  

---

### 3️⃣ Feature Selection

Key features used:
- Age, Gender  
- Height, Weight, BMI  
- Blood Pressure (ap_hi, ap_lo)  
- Cholesterol, Glucose  
- Smoking, Alcohol, Activity  

---

### 4️⃣ Data Splitting

- 80% → Training  
- 20% → Testing  

---

### 5️⃣ Feature Scaling

- Uses **StandardScaler**  
- Ensures better model performance  

---

### 6️⃣ Model Training

- Random Forest with:
  - 100 trees  
  - Controlled depth  
  - Balanced class weights  

---

### 7️⃣ Model Evaluation

- Accuracy score  
- Classification report  
- Feature importance  

---

### 8️⃣ Prediction System

- User inputs medical data  
- Features processed  
- Model predicts:
  - ✅ No CVD  
  - ⚠️ High CVD Risk  

---

### 9️⃣ Visualization

- 📊 Bar graph → Probability (CVD vs No CVD)  
- 💓 ECG simulation → Real-time animation  

---

## 📊 Output Details

- Risk classification  
- Probability percentage  
- Medical analysis  
- Identified risk factors  
- Personalized recommendations  

---

## ⚠️ Important Notes

- 🐍 Python 3.8+ required  
- 📷 GUI-based application  
- ⚠️ Not a medical diagnosis tool (educational use only)  

---

## 🔧 Important Fix

Your dataset path currently uses:

```
E:\JrBotics\...
```

👉 Replace with:

```python
possible_paths = ["cardio_train.csv"]
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
