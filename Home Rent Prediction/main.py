import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

df      = pd.read_csv(r"House Data.csv")
X       = df[["Number of Rooms", "Home Size (sqft)", "Floor", "Area Rating (1-5)"]]
y       = df["Rent Price (INR)"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model   = LinearRegression().fit(X_train, y_train)
y_pred  = model.predict(X_test)
r2      = r2_score(y_test, y_pred)

root = tk.Tk()
root.title("House Rent Predictor")
root.geometry("980x620")
root.configure(bg="#0f172a")

hdr = tk.Frame(root, bg="#1e293b", pady=12)
hdr.pack(fill=tk.X)
tk.Label(hdr, text="🏠  House Rent Predictor", font=("Consolas", 15, "bold"),
         fg="#38bdf8", bg="#1e293b").pack(side=tk.LEFT, padx=20)
tk.Label(hdr, text=f"Model R² = {r2:.4f}  |  {len(df)} samples",
         font=("Consolas", 9), fg="#475569", bg="#1e293b").pack(side=tk.RIGHT, padx=20)

left  = tk.Frame(root, bg="#0f172a", padx=24, pady=20, width=300)
left.pack(side=tk.LEFT, fill=tk.Y); left.pack_propagate(False)
right = tk.Frame(root, bg="#0f172a", padx=10, pady=16)
right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

def make_slider(label, from_, to, var):
    tk.Label(left, text=label, font=("Segoe UI", 10),
             fg="#94a3b8", bg="#0f172a").pack(anchor="w", pady=(10,0))
    row = tk.Frame(left, bg="#0f172a"); row.pack(fill=tk.X)
    val = tk.Label(row, text=str(var.get()), font=("Consolas", 10, "bold"),
                   fg="#f1f5f9", bg="#0f172a", width=6)
    val.pack(side=tk.RIGHT)
    tk.Scale(row, variable=var, from_=from_, to=to, orient=tk.HORIZONTAL,
             bg="#0f172a", fg="#94a3b8", troughcolor="#1e293b",
             activebackground="#38bdf8", highlightthickness=0, showvalue=False,
             command=lambda _: val.config(text=str(var.get()))
             ).pack(fill=tk.X, side=tk.LEFT, expand=True)

rooms_v  = tk.IntVar(value=2)
size_v   = tk.IntVar(value=800)
floor_v  = tk.IntVar(value=1)
rating_v = tk.IntVar(value=3)

make_slider("Number of Rooms",    1,    10, rooms_v)
make_slider("Home Size (sqft)",   200, 5000, size_v)
make_slider("Floor",              0,    30, floor_v)
make_slider("Area Rating (1-5)",  1,     5, rating_v)

result_lbl = tk.Label(left, text="—", font=("Consolas", 26, "bold"),
                       fg="#34d399", bg="#0f172a")

def predict():
    inp  = pd.DataFrame([{"Number of Rooms": rooms_v.get(),
                           "Home Size (sqft)": size_v.get(),
                           "Floor": floor_v.get(),
                           "Area Rating (1-5)": rating_v.get()}])
    rent = model.predict(inp)[0]
    result_lbl.config(text=f"Rs.{rent:,.0f}",
                      fg="#34d399" if rent < 30000 else
                         "#facc15" if rent < 60000 else "#f87171")

tk.Button(left, text="Predict Rent", font=("Consolas", 11, "bold"),
          bg="#166534", fg="white", activebackground="#15803d",
          relief=tk.FLAT, pady=9, cursor="hand2",
          command=predict).pack(fill=tk.X, pady=(22, 6))
tk.Label(left, text="Estimated Rent:", font=("Segoe UI", 9),
         fg="#475569", bg="#0f172a").pack(anchor="w")
result_lbl.pack(anchor="w")

tk.Label(right, text="Actual vs Predicted Rent Price",
         font=("Consolas", 11, "bold"), fg="#38bdf8", bg="#0f172a").pack(anchor="w")

fig, ax = plt.subplots(figsize=(6.2, 4.8))
fig.patch.set_facecolor("#0f172a")
ax.set_facecolor("#1e293b")
ax.scatter(y_test, y_pred, color="#38bdf8", edgecolors="#0ea5e9", alpha=0.7, s=40)
ax.plot([y.min(), y.max()], [y.min(), y.max()], color="#f87171", lw=1.5, ls="--")
ax.set_xlabel("Actual Rent (INR)", color="#94a3b8")
ax.set_ylabel("Predicted Rent (INR)", color="#94a3b8")
ax.tick_params(colors="#64748b")
for sp in ax.spines.values(): sp.set_edgecolor("#334155")
fig.tight_layout()

FigureCanvasTkAgg(fig, master=right).get_tk_widget().pack(fill=tk.BOTH, expand=True)

root.mainloop()
