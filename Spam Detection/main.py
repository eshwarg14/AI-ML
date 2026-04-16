import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
from scipy.sparse import hstack
import tkinter as tk
from tkinter import messagebox, scrolledtext

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "url", text)
    return text

def extra_features(text):
    return [
        len(text),
        sum(c.isupper() for c in text),
        text.count("!"),
        sum(c.isdigit() for c in text),
        int("free" in text.lower()),
        int("win" in text.lower()),
        int("urgent" in text.lower())
    ]

df = pd.read_csv(r"spam.csv", encoding="latin-1")
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
df.columns = ['label', 'message']

label = df['label'].map({'spam': 1, 'ham': 0})

clean = df['message'].apply(clean_text)

X_train, X_test, y_train, y_test = train_test_split(
    clean, label, test_size=0.2, random_state=42
)

vectorizer_word = TfidfVectorizer(
    max_features=8000,
    ngram_range=(1,3)
)

vectorizer_char = TfidfVectorizer(
    analyzer='char',
    ngram_range=(3,5),
    max_features=5000
)

X_train_word = vectorizer_word.fit_transform(X_train)
X_test_word = vectorizer_word.transform(X_test)

X_train_char = vectorizer_char.fit_transform(X_train)
X_test_char = vectorizer_char.transform(X_test)

X_train_extra = pd.DataFrame([extra_features(t) for t in X_train])
X_test_extra = pd.DataFrame([extra_features(t) for t in X_test])

X_train_final = hstack([X_train_word, X_train_char, X_train_extra])
X_test_final = hstack([X_test_word, X_test_char, X_test_extra])

model = LinearSVC(class_weight='balanced')
model.fit(X_train_final, y_train)

preds = model.predict(X_test_final)
acc = accuracy_score(y_test, preds)
print(f"Model Accuracy: {acc*100:.2f}%")

class SpamDetectorGUI:
    def __init__(self, root):
        self.root = root
        root.title("Spam Detector")
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

        cleaned = clean_text(text)

        word_vec = vectorizer_word.transform([cleaned])
        char_vec = vectorizer_char.transform([cleaned])
        extra_vec = pd.DataFrame([extra_features(text)])

        final_vec = hstack([word_vec, char_vec, extra_vec])

        pred = model.predict(final_vec)[0]

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
