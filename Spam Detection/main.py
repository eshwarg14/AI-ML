import pandas as pd
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
import tkinter as tk
from tkinter import messagebox, scrolledtext

nltk.download('stopwords')
nltk.download('wordnet')

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    words = text.split()
    words = [lemmatizer.lemmatize(w) for w in words if w not in stop_words]
    return " ".join(words)

df = pd.read_csv(r"spam.csv", encoding="latin-1")
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
df.columns = ['label', 'message']
label = df['label'].map({'spam': 1, 'ham': 0})

clean = df['message'].apply(clean_text)

X_train, X_test, y_train, y_test = train_test_split(
    clean, label, test_size=0.2, random_state=42
)

vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1,2),
    stop_words='english'
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

model = LinearSVC()
model.fit(X_train_vec, y_train)

preds = model.predict(X_test_vec)
acc = accuracy_score(y_test, preds)
print(f"Model Accuracy: {acc*100:.2f}%")

class SpamDetectorGUI:
    def __init__(self, root):
        self.root = root
        root.title("📧 AI Spam Detector (High Accuracy)")
        root.geometry("600x400")

        tk.Label(root, text=f"Model Accuracy: {acc*100:.2f}%",
                 font=("Arial", 10, "bold"), fg="blue").pack()

        self.input_box = scrolledtext.ScrolledText(root, height=6)
        self.input_box.pack(pady=10)

        btn_frame = tk.Frame(root)
        btn_frame.pack()

        tk.Button(btn_frame, text="Check", bg="#4CAF50", fg="white",
                  command=self.check).grid(row=0, column=0, padx=5)

        tk.Button(btn_frame, text="Clear", bg="#FF9800", fg="white",
                  command=self.clear).grid(row=0, column=1, padx=5)

        self.result = tk.Label(root, text="Result will appear here",
                               font=("Arial", 12, "bold"))
        self.result.pack(pady=20)

    def check(self):
        text = self.input_box.get("1.0", tk.END).strip()
        if not text:
            return messagebox.showwarning("Empty", "Enter message")

        clean = clean_text(text)
        vec = vectorizer.transform([clean])
        pred = model.predict(vec)[0]

        if pred == 1:
            self.result.config(text="⚠️ SPAM DETECTED", fg="red")
        else:
            self.result.config(text="✅ NOT SPAM", fg="green")

    def clear(self):
        self.input_box.delete("1.0", tk.END)
        self.result.config(text="Result will appear here", fg="black")

root = tk.Tk()
SpamDetectorGUI(root)
root.mainloop()
