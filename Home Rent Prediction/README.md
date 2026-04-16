# 🏠 AI House Rent Predictor

A Machine Learning-based application that predicts house rent based on features like number of rooms, size, floor, and area rating. Built with Python, Tkinter, and Scikit-learn, this project provides real-time predictions with interactive UI and visualization.

---

## Preview

![Demo](Images/rent1.png)
![Demo](Images/rent2.png)

---

## ✨ Features

- 🏠 Predict house rent instantly  
- 🤖 Machine Learning model (Linear Regression)  
- 🎛️ Interactive sliders for input  
- 📊 Real-time prediction display  
- 📈 Actual vs Predicted graph  
- 🖥️ Modern GUI using Tkinter  
- 🎯 Color-coded rent output  

---

## 🧠 What is House Price Prediction?

House rent prediction is a **regression problem** where we estimate the price based on features like:

- Number of rooms  
- Size (sqft)  
- Floor level  
- Area rating  

---

## 🤖 Machine Learning Model

### 📈 Linear Regression

- Predicts continuous values (like rent)  
- Finds relationship between input features and output  
- Uses best-fit line approach  

👉 Formula concept:
```
y = m1x1 + m2x2 + ... + c
```

---

## 🧠 Technologies Used

```
pandas
matplotlib
scikit-learn
tkinter
```

📦 Install dependencies:

```bash
pip install pandas matplotlib scikit-learn
```

---

## ▶️ How to Run

```bash
python main.py
```

---

## 📁 Project Structure

```
├── main.py                 # Main application
├── House Data.csv          # Dataset (place in same folder as main.py)
└── README.md
```

---

## 📊 Dataset

- 📄 File: `House Data.csv`  
- 📍 Place it **in the same folder as main.py**  

### Features:

- Number of Rooms  
- Home Size (sqft)  
- Floor  
- Area Rating (1-5)  
- Rent Price (INR)  

---

## 🛠️ Step-by-Step Working

### 1️⃣ Data Loading
- Dataset loaded using pandas  

---

### 2️⃣ Feature Selection

Input features:
- Rooms  
- Size  
- Floor  
- Area rating  

Target:
- Rent price  

---

### 3️⃣ Train-Test Split

- 80% → Training  
- 20% → Testing  

---

### 4️⃣ Model Training

- Algorithm: **Linear Regression**  
- Learns relationship between features and rent  

---

### 5️⃣ Model Evaluation

- Metric: **R² Score**

👉 Measures how well model fits data  
- Closer to 1 → Better model  

---

### 6️⃣ Prediction System

- User inputs values via sliders  
- Data passed to model  
- Rent is predicted instantly  

---

### 7️⃣ Visualization

- 📊 Scatter plot:
  - X-axis → Actual rent  
  - Y-axis → Predicted rent  
- 📈 Diagonal line → Perfect prediction  

---

## 🎨 Output Logic

- 🟢 Low Rent (< 30,000)  
- 🟡 Medium Rent (< 60,000)  
- 🔴 High Rent (> 60,000)  

---

## ⚠️ Important Notes

- 🐍 Python 3.8+ required  
- 📷 GUI-based application  
- 📊 Accuracy depends on dataset quality  

---

## 🔧 Important Fix

Your dataset path currently is:

```
E:\JrBotics\...
```

👉 Replace with:

```python
df = pd.read_csv("House Data.csv")
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

---

## 🚀 Future Improvements

- Advanced models (Random Forest, XGBoost) 🤖  
- Location-based pricing 📍  
- Web app version 🌐  
- Real-time dataset integration 📊  
