import tkinter as tk
from tkinter import messagebox
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

df = pd.read_csv(r"D:\JrBotics\AI Projects\AI Updated\8\music_dataset.csv")   
df.columns = df.columns.str.strip()
df["mood"]     = df["mood"].str.strip().str.lower()
df["type"]     = df["type"].str.strip()
df["language"] = df["language"].str.strip()

FEATURES = ["energy", "valence", "tempo", "acousticness", "danceability"]

le = LabelEncoder()
df["mood_encoded"] = le.fit_transform(df["mood"])

X = df[FEATURES]
y = df["mood_encoded"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred   = model.predict(X_test)
ACCURACY = accuracy_score(y_test, y_pred)
REPORT   = classification_report(y_test, y_pred,
                                  target_names=le.classes_, zero_division=0)

MOOD_META = {
    "happy":     {"emoji": "😊", "color": "#FFD700"},
    "sad":       {"emoji": "😢", "color": "#6495ED"},
    "energetic": {"emoji": "⚡", "color": "#FF4500"},
    "romantic":  {"emoji": "❤️", "color": "#FF69B4"},
    "relaxed":   {"emoji": "🌿", "color": "#32CD32"},
    "focused":   {"emoji": "🎯", "color": "#00CED1"},
    "angry":     {"emoji": "🔥", "color": "#FF2400"},
    "nostalgic": {"emoji": "🌙", "color": "#DDA0DD"},
}
BG      = "#0A0B14"
BG_CARD = "#12152B"
BG_ROW  = "#1A1E35"
ACCENT  = "#7C5CBF"
TEXT    = "#E8ECF8"
MUTED   = "#4A5070"
GREEN   = "#32CD32"


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("RAGA.AI - ML Mood Music Recommender")
        self.root.configure(bg=BG)
        self.root.geometry("1080x680")
        self.root.resizable(False, False)

        self.mood   = tk.StringVar(value="happy")
        self.ftype  = tk.StringVar(value="both")
        self.count  = tk.IntVar(value=5)
        self.status = tk.StringVar(value="Model ready · Select mood and click Recommend ♪")
        self.mood_btns = {}

        self._ui()
        self._select("happy")

    def _ui(self):
        hdr = tk.Frame(self.root, bg=BG)
        hdr.pack(fill="x", padx=20, pady=(14, 2))
        tk.Label(hdr, text="RAGA.AI", font=("Georgia", 22, "bold"),
                 fg=ACCENT, bg=BG).pack(side="left")
        tk.Label(hdr, text="  ML Mood Recommender · Indian & Western",
                 font=("Courier New", 9), fg=MUTED, bg=BG).pack(side="left", pady=6)

        stats = tk.Frame(self.root, bg=BG_CARD)
        stats.pack(fill="x", padx=20, pady=(0, 8))
        tk.Label(stats,
                 text=f"  🤖 RandomForest · Train: {len(X_train)} | Test: {len(X_test)} | "
                      f"Accuracy: {ACCURACY*100:.1f}%  ",
                 font=("Courier New", 9), fg=GREEN, bg=BG_CARD,
                 pady=5).pack(side="left")
        tk.Button(stats, text="📊 View Report", font=("Courier New", 8),
                  fg=TEXT, bg=BG_ROW, bd=0, padx=8, pady=4, cursor="hand2",
                  command=self._show_report).pack(side="right", padx=6, pady=4)
        tk.Button(stats, text="🔮 Predict Mood", font=("Courier New", 8),
                  fg=BG, bg=ACCENT, bd=0, padx=8, pady=4, cursor="hand2",
                  command=self._predict_window).pack(side="right", padx=(0, 4), pady=4)

        tk.Label(self.root, text="SELECT MOOD", font=("Courier New", 8),
                 fg=MUTED, bg=BG).pack(anchor="w", padx=20, pady=(2, 3))
        mf = tk.Frame(self.root, bg=BG)
        mf.pack(fill="x", padx=20)
        for i, (mood, m) in enumerate(MOOD_META.items()):
            b = tk.Button(mf, text=f"{m['emoji']} {mood.capitalize()}",
                          font=("Courier New", 9, "bold"), fg=TEXT, bg=BG_ROW,
                          bd=0, pady=6, padx=10, cursor="hand2",
                          command=lambda mo=mood: self._select(mo))
            b.grid(row=0, column=i, padx=3)
            self.mood_btns[mood] = b

        cf = tk.Frame(self.root, bg=BG)
        cf.pack(fill="x", padx=20, pady=8)
        tk.Label(cf, text="TYPE:", font=("Courier New", 9), fg=MUTED, bg=BG).pack(side="left")
        for val, lbl in [("both","🌐 Both"),("Indian","🇮🇳 Indian"),("Western","🌍 Western")]:
            tk.Radiobutton(cf, text=lbl, variable=self.ftype, value=val,
                           font=("Courier New", 9), fg=TEXT, bg=BG,
                           selectcolor=BG_CARD, activebackground=BG,
                           bd=0, cursor="hand2").pack(side="left", padx=5)
        tk.Label(cf, text="  COUNT:", font=("Courier New", 9), fg=MUTED, bg=BG).pack(side="left")
        for n in [3, 5, 8, 10]:
            tk.Radiobutton(cf, text=str(n), variable=self.count, value=n,
                           font=("Courier New", 9), fg=TEXT, bg=BG,
                           selectcolor=BG_CARD, activebackground=BG,
                           bd=0, cursor="hand2").pack(side="left", padx=4)
        tk.Button(cf, text="♪  RECOMMEND", font=("Courier New", 10, "bold"),
                  fg=BG, bg=ACCENT, activebackground="#9B7FD4",
                  bd=0, pady=7, padx=18, cursor="hand2",
                  command=self._recommend).pack(side="right")

        cols   = ["#", "Song Title",   "Artist",  "Film / Album", "Language", "Type", "Energy","Valence"]
        widths = [ 3,   28,             22,         20,             10,          7,      7,       7]
        self.col_widths = widths
        hrow = tk.Frame(self.root, bg=BG_ROW)
        hrow.pack(fill="x", padx=20)
        for c, w in zip(cols, widths):
            tk.Label(hrow, text=c, font=("Courier New", 8, "bold"),
                     fg=ACCENT, bg=BG_ROW, width=w, anchor="w",
                     pady=6, padx=4).pack(side="left")

        outer = tk.Frame(self.root, bg=BG_CARD)
        outer.pack(fill="both", expand=True, padx=20, pady=(0, 4))
        canvas = tk.Canvas(outer, bg=BG_CARD, bd=0, highlightthickness=0)
        sb = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        self.body = tk.Frame(canvas, bg=BG_CARD)
        self.body.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.body, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        tk.Label(self.root, textvariable=self.status, font=("Courier New", 9),
                 fg=MUTED, bg=BG).pack(anchor="w", padx=20, pady=(0, 8))

    def _select(self, mood):
        self.mood.set(mood)
        for m, b in self.mood_btns.items():
            b.configure(bg=MOOD_META[m]["color"] if m == mood else BG_ROW,
                        fg=BG if m == mood else TEXT)

    def _recommend(self):
        mood  = self.mood.get()
        ftype = self.ftype.get()
        n     = self.count.get()

        filtered = df[df["mood"] == mood]
        if ftype != "both":
            filtered = filtered[filtered["type"] == ftype]

        picks = filtered.sample(min(n, len(filtered))).to_dict("records")

        for w in self.body.winfo_children():
            w.destroy()

        meta = MOOD_META.get(mood, {})
        self.status.set(
            f"{meta.get('emoji','')}  {len(picks)} tracks · mood='{mood}' · "
            f"dataset={len(df)} songs · accuracy={ACCURACY*100:.1f}%")

        for i, song in enumerate(picks):
            bg  = BG_ROW if i % 2 == 0 else BG_CARD
            row = tk.Frame(self.body, bg=bg)
            row.pack(fill="x")
            tc  = "#FF9933" if song["type"] == "Indian" else "#4169E1"
            for val, w, col in [
                (f"{i+1}.",                      self.col_widths[0], TEXT),
                (song["title"],                  self.col_widths[1], meta.get("color", TEXT)),
                (song["artist"],                 self.col_widths[2], TEXT),
                (song["film_album"],             self.col_widths[3], MUTED),
                (song["language"],               self.col_widths[4], TEXT),
                (song["type"],                   self.col_widths[5], tc),
                (f'{song["energy"]:.2f}',        self.col_widths[6], "#88AAFF"),
                (f'{song["valence"]:.2f}',       self.col_widths[7], "#FFAA88"),
            ]:
                tk.Label(row, text=str(val), font=("Courier New", 9),
                         fg=col, bg=bg, width=w, anchor="w",
                         pady=5, padx=4).pack(side="left")

    def _show_report(self):
        win = tk.Toplevel(self.root)
        win.title("Classification Report")
        win.configure(bg=BG)
        win.geometry("520x400")
        tk.Label(win, text="📊 Model Classification Report",
                 font=("Courier New", 11, "bold"), fg=ACCENT, bg=BG).pack(pady=(12, 4))
        tk.Label(win, text=f"Algorithm: Random Forest  |  Accuracy: {ACCURACY*100:.1f}%",
                 font=("Courier New", 9), fg=GREEN, bg=BG).pack()
        tk.Label(win, text=f"Train samples: {len(X_train)}   Test samples: {len(X_test)}",
                 font=("Courier New", 9), fg=MUTED, bg=BG).pack(pady=(0, 8))
        txt = tk.Text(win, font=("Courier New", 9), bg=BG_CARD, fg=TEXT,
                      bd=0, padx=12, pady=8)
        txt.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        txt.insert("end", REPORT)
        txt.configure(state="disabled")

    def _predict_window(self):
        win = tk.Toplevel(self.root)
        win.title("🔮 Predict Mood from Audio Features")
        win.configure(bg=BG)
        win.geometry("400x380")
        win.resizable(False, False)

        tk.Label(win, text="🔮 Predict Mood from Features",
                 font=("Courier New", 11, "bold"), fg=ACCENT, bg=BG).pack(pady=(14, 6))
        tk.Label(win, text="Enter values between 0.0 – 1.0 (tempo: 50–200)",
                 font=("Courier New", 8), fg=MUTED, bg=BG).pack(pady=(0, 10))

        sliders = {}
        limits  = {"energy":(0,1,0.01),"valence":(0,1,0.01),
                   "tempo":(50,200,1),"acousticness":(0,1,0.01),"danceability":(0,1,0.01)}
        defaults= {"energy":0.6,"valence":0.7,"tempo":100,"acousticness":0.3,"danceability":0.6}

        for feat, (mn, mx, res) in limits.items():
            row = tk.Frame(win, bg=BG)
            row.pack(fill="x", padx=20, pady=3)
            tk.Label(row, text=f"{feat:<14}", font=("Courier New", 9),
                     fg=TEXT, bg=BG, width=14, anchor="w").pack(side="left")
            var = tk.DoubleVar(value=defaults[feat])
            sl  = tk.Scale(row, variable=var, from_=mn, to=mx, resolution=res,
                           orient="horizontal", bg=BG, fg=TEXT, troughcolor=BG_ROW,
                           highlightthickness=0, bd=0, length=180, showvalue=True,
                           font=("Courier New", 8))
            sl.pack(side="left")
            sliders[feat] = var

        result_var = tk.StringVar(value="")
        tk.Label(win, textvariable=result_var, font=("Courier New", 12, "bold"),
                 fg=GREEN, bg=BG).pack(pady=8)

        def predict():
            vals = [[sliders[f].get() for f in FEATURES]]
            pred = model.predict(vals)[0]
            mood = le.inverse_transform([pred])[0]
            proba= model.predict_proba(vals)[0]
            conf = proba.max() * 100
            meta = MOOD_META.get(mood, {})
            result_var.set(f"{meta.get('emoji','?')}  {mood.upper()}  ({conf:.1f}% confidence)")

        tk.Button(win, text="  PREDICT MOOD  ", font=("Courier New", 10, "bold"),
                  fg=BG, bg=ACCENT, bd=0, pady=8, cursor="hand2",
                  command=predict).pack(pady=4)


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
