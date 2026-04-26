# 🎧 RAGA.AI – ML Mood-Based Music Recommender

An AI-powered music recommendation system that suggests songs based on user mood using Machine Learning. Built with Python, Tkinter, and Scikit-learn, this system analyzes audio features and predicts mood to recommend songs.

---

## Preview

![Demo](https://github.com/eshwarg14/AI-ML/raw/a510c0ab7cf87ba107064759b54e18f231a6adae/Images/MRR.png)

---

## ✨ Features

- 🎧 Mood-based song recommendations  
- 🤖 Machine Learning model (Random Forest)  
- 🎯 Select mood manually OR predict from features  
- 🌐 Supports Indian & Western music  
- 📊 Model accuracy and classification report  
- 🎛️ Feature-based mood prediction  
- 🖥️ Advanced GUI with Tkinter  
- 🎨 Color-coded UI based on mood  

---

## 🧠 What is a Recommendation System?

A recommendation system suggests items (songs, movies, etc.) based on:

- User preferences  
- Patterns in data  
- Machine learning models  

---

## 🤖 Machine Learning Model

### 🌳 Random Forest Classifier

- Ensemble learning method  
- Uses multiple decision trees  
- Improves accuracy and stability  

---

## 🧠 Input Features

The model uses audio features:

- ⚡ Energy  
- 😊 Valence (happiness level)  
- 🎵 Tempo  
- 🎻 Acousticness  
- 💃 Danceability  

---

## 🧠 Technologies Used

```
pandas
numpy
scikit-learn
tkinter
```

📦 Install dependencies:

```bash
pip install pandas numpy scikit-learn
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
├── music_dataset.csv    # Dataset (place in same folder)
└── README.md
```

---

## 📊 Dataset

- 📄 File: `music_dataset.csv`  
- 📍 Place it **in the same folder as main.py**  

### Contains:

- Song title  
- Artist  
- Album  
- Language  
- Type (Indian / Western)  
- Audio features (energy, tempo, etc.)  
- Mood label  

---

## 🛠️ Step-by-Step Working

### 1️⃣ Data Loading
- Dataset loaded using pandas  
- Cleaned (strip spaces, normalize text)  

---

### 2️⃣ Label Encoding

- Converts mood labels → numeric values  

---

### 3️⃣ Train-Test Split

- 80% → Training  
- 20% → Testing  

---

### 4️⃣ Model Training

- Random Forest with 100 trees  
- Learns patterns between features and mood  

---

### 5️⃣ Model Evaluation

- Accuracy score  
- Classification report  

---

### 6️⃣ Recommendation System

- User selects mood  
- Filters dataset  
- Randomly selects songs  
- Displays results  

---

### 7️⃣ Mood Prediction (Advanced)

- User inputs audio features  
- Model predicts mood  
- Shows confidence score  

---

## 🎯 Output Features

- 🎵 Recommended songs  
- 🎯 Predicted mood  
- 📊 Confidence score  
- 🎨 Color-coded UI  

---

## ⚠️ Important Notes

- 🐍 Python 3.8+ required  
- 📊 Accuracy depends on dataset quality  
- 🎧 Not connected to real streaming services  

---

## 🔧 Important Fix

Your dataset path currently is:

```
E:\JrBotics\...
```

👉 Replace with:

```python
df = pd.read_csv("music_dataset.csv")
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

- Spotify API integration 🎧  
- Deep learning recommendation 🤖  
- User preference learning 🧠  
- Mobile app version 📱  
