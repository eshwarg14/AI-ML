import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import requests, threading, json, re
import PyPDF2
   
API_KEY = ""
URL     = "https://openrouter.ai/api/v1/chat/completions"
MODEL   = "openrouter/free"          

SYSTEM = """You are an expert ATS (Applicant Tracking System) analyst and career coach.
Analyze the resume and job description provided.
Return ONLY a valid JSON object with this exact structure (no markdown, no extra text):
{
  "ats_score": <integer 0-100>,
  "verdict": "<one line summary>",
  "matched_keywords": ["kw1", "kw2", ...],
  "missing_keywords": ["kw1", "kw2", ...],
  "strengths": ["point1", "point2", ...],
  "improvements": ["point1", "point2", ...],
  "section_scores": {
    "Experience": <0-100>,
    "Skills": <0-100>,
    "Education": <0-100>,
    "Formatting": <0-100>,
    "Keywords": <0-100>
  },
  "quick_fixes": ["fix1", "fix2", ...]
}"""

def extract_pdf_text(path):
    if not PDF_OK:
        return None
    try:
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            return "\n".join(p.extract_text() or "" for p in reader.pages)
    except Exception as e:
        return f"PDF read error: {e}"

def call_api(resume_text, jd_text):
    prompt = (
        f"RESUME:\n{resume_text[:3000]}\n\n"
        f"JOB DESCRIPTION:\n{jd_text[:2000]}\n\n"
        "Respond ONLY with the JSON object. No explanation, no markdown fences."
    )
    raw = ""
    try:
        r = requests.post(URL,
            headers={"Authorization": f"Bearer {API_KEY}",
                     "Content-Type": "application/json",
                     "HTTP-Referer": "http://localhost",
                     "X-Title": "ATSAnalyzer"},
            json={"model": MODEL,
                  "max_tokens": 1200,
                  "messages": [{"role": "system", "content": SYSTEM},
                                {"role": "user",   "content": prompt}]},
            timeout=60)
        data = r.json()
        if "choices" not in data:
            return {"error": data.get("error", {}).get("message", str(data))}
        raw = data["choices"][0]["message"]["content"].strip()
        raw = re.sub(r"```json|```", "", raw).strip()
        start, end = raw.find("{"), raw.rfind("}")
        if start != -1 and end != -1:
            raw = raw[start:end+1]
        raw = re.sub(r",\s*([}\]])", r"\1", raw)
        return json.loads(raw)
    except json.JSONDecodeError:
        score_match = re.search(r'"ats_score"\s*:\s*(\d+)', raw)
        score = int(score_match.group(1)) if score_match else 0
        return {
            "ats_score": score,
            "verdict": "Partial result — model returned incomplete JSON. Try again.",
            "matched_keywords": [],
            "missing_keywords": [],
            "strengths": ["AI response was truncated. Results may be incomplete."],
            "improvements": ["Try again — free models occasionally cut off responses."],
            "section_scores": {"Experience": 0, "Skills": 0, "Education": 0, "Formatting": 0, "Keywords": 0},
            "quick_fixes": ["Click Analyze again for a fresh attempt."]
        }
    except Exception as e:
        return {"error": str(e)}

def score_color(s):
    if s >= 75: return "#00c853"
    if s >= 50: return "#ffab00"
    return "#ff1744"

def draw_circle_score(canvas, score, color):
    canvas.delete("all")
    W = 130
    canvas.config(width=W, height=W, bg="#0d1117")
    pad = 12
    canvas.create_oval(pad, pad, W-pad, W-pad, outline="#1e2a3a", width=8)
    extent = int(score / 100 * 359)
    canvas.create_arc(pad, pad, W-pad, W-pad, start=90, extent=-extent,
                      outline=color, width=8, style="arc")
    canvas.create_text(W//2, W//2-6, text=str(score), font=("Consolas", 22, "bold"),
                       fill=color)
    canvas.create_text(W//2, W//2+16, text="/ 100", font=("Consolas", 9),
                       fill="#4a5568")

def draw_bar(frame, label, score, color):
    row = tk.Frame(frame, bg="#0d1117")
    row.pack(fill=tk.X, pady=3)
    tk.Label(row, text=f"{label:<12}", font=("Consolas", 10), fg="#a0aec0",
             bg="#0d1117", width=12, anchor="w").pack(side=tk.LEFT)
    bar_bg = tk.Frame(row, bg="#1e2a3a", height=14, width=200)
    bar_bg.pack(side=tk.LEFT, padx=6)
    bar_bg.pack_propagate(False)
    fill_w = max(1, int(score / 100 * 200))
    tk.Frame(bar_bg, bg=color, width=fill_w, height=14).place(x=0, y=0)
    tk.Label(row, text=f"{score}%", font=("Consolas", 9, "bold"),
             fg=color, bg="#0d1117").pack(side=tk.LEFT)

def pill_list(frame, items, bg, fg):
    wrap = tk.Frame(frame, bg="#0d1117")
    wrap.pack(fill=tk.X, pady=(0,6))
    for item in items:
        tk.Label(wrap, text=f"  {item}  ", font=("Consolas", 9),
                 bg=bg, fg=fg, padx=4, pady=2, relief="flat").pack(
                 side=tk.LEFT, padx=3, pady=2)

def bullet_list(frame, items, icon, fg):
    for item in items:
        tk.Label(frame, text=f"{icon}  {item}", font=("Segoe UI", 10),
                 fg=fg, bg="#0d1117", wraplength=340, justify="left",
                 anchor="w").pack(fill=tk.X, pady=2, padx=4)

root = tk.Tk()
root.title("ATS Resume Analyzer")
root.geometry("1100x720")
root.configure(bg="#0d1117")
root.resizable(True, True)

top = tk.Frame(root, bg="#161b22", pady=14)
top.pack(fill=tk.X)
tk.Label(top, text="◈  ATS Resume Analyzer", font=("Consolas", 16, "bold"),
         fg="#58a6ff", bg="#161b22").pack(side=tk.LEFT, padx=20)
tk.Label(top, text="Powered by AI", font=("Consolas", 9),
         fg="#30363d", bg="#161b22").pack(side=tk.RIGHT, padx=20)

pane = tk.PanedWindow(root, orient=tk.HORIZONTAL, bg="#0d1117",
                      sashwidth=4, sashrelief=tk.FLAT)
pane.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

left = tk.Frame(pane, bg="#0d1117", padx=16, pady=12)
pane.add(left, minsize=400)

def section_label(parent, text):
    tk.Label(parent, text=text, font=("Consolas", 11, "bold"),
             fg="#58a6ff", bg="#0d1117").pack(anchor="w", pady=(10,4))

section_label(left, "▸ Resume Text")

resume_hint = tk.Label(left, text="Paste your resume below, or load a PDF →",
                       font=("Segoe UI", 9), fg="#4a5568", bg="#0d1117")
resume_hint.pack(anchor="w")

resume_bar = tk.Frame(left, bg="#0d1117")
resume_bar.pack(fill=tk.X, pady=(4,2))

file_badge = tk.Frame(left, bg="#0d1117")

file_icon  = tk.Label(file_badge, text="📄", font=("Segoe UI", 11),
                       bg="#0d2a1a", fg="#3fb950", padx=6, pady=4)
file_icon.pack(side=tk.LEFT)
file_name_lbl = tk.Label(file_badge, text="", font=("Consolas", 9, "bold"),
                          bg="#0d2a1a", fg="#3fb950", pady=4, padx=4)
file_name_lbl.pack(side=tk.LEFT)
file_pages_lbl = tk.Label(file_badge, text="", font=("Consolas", 8),
                           bg="#0d2a1a", fg="#238636", pady=4)
file_pages_lbl.pack(side=tk.LEFT)

def clear_file():
    resume_box.delete("1.0", tk.END)
    file_badge.pack_forget()
    resume_hint.config(text="Paste your resume below, or load a PDF →")

tk.Button(file_badge, text="✕", font=("Consolas", 9, "bold"),
          bg="#0d2a1a", fg="#f85149", activebackground="#3d1f1f",
          relief=tk.FLAT, padx=6, pady=2, cursor="hand2",
          command=clear_file).pack(side=tk.RIGHT, padx=4)

import os

def load_pdf():
    path = filedialog.askopenfilename(filetypes=[("PDF","*.pdf"),("Text","*.txt")])
    if not path: return
    pages = None
    if path.endswith(".pdf"):
        if not PDF_OK:
            messagebox.showwarning("Missing library",
                "Install PyPDF2:\n  pip install PyPDF2")
            return
        text = extract_pdf_text(path)
        try:
            with open(path, "rb") as f:
                pages = len(PyPDF2.PdfReader(f).pages)
        except Exception:
            pass
    else:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()

    resume_box.delete("1.0", tk.END)
    resume_box.insert("1.0", text)

    fname = os.path.basename(path)
    fname_short = fname if len(fname) <= 32 else fname[:29] + "…"
    file_name_lbl.config(text=fname_short)
    file_pages_lbl.config(text=f"  •  {pages} page{'s' if pages!=1 else ''}" if pages else "")
    file_badge.pack(fill=tk.X, pady=(0,4), before=resume_box)
    resume_hint.config(text="✔ File loaded — text extracted below")

tk.Button(resume_bar, text="📄 Load PDF / TXT", font=("Consolas", 9),
          bg="#21262d", fg="#58a6ff", activebackground="#30363d",
          relief=tk.FLAT, padx=10, pady=4, cursor="hand2",
          command=load_pdf).pack(side=tk.LEFT)

resume_box = scrolledtext.ScrolledText(left, height=12, font=("Consolas", 9),
                                        bg="#161b22", fg="#c9d1d9",
                                        insertbackground="white",
                                        relief=tk.FLAT, bd=0, padx=8, pady=6)
resume_box.pack(fill=tk.BOTH, expand=True)

section_label(left, "▸ Job Description")

jd_box = scrolledtext.ScrolledText(left, height=8, font=("Consolas", 9),
                                    bg="#161b22", fg="#c9d1d9",
                                    insertbackground="white",
                                    relief=tk.FLAT, bd=0, padx=8, pady=6)
jd_box.pack(fill=tk.BOTH, expand=True)

analyze_btn = tk.Button(left, text="⚡  ANALYZE RESUME",
                         font=("Consolas", 12, "bold"),
                         bg="#238636", fg="white",
                         activebackground="#2ea043",
                         relief=tk.FLAT, pady=10, cursor="hand2")
analyze_btn.pack(fill=tk.X, pady=(12,4))

status_lbl = tk.Label(left, text="", font=("Consolas", 9),
                       fg="#8b949e", bg="#0d1117")
status_lbl.pack()

right_outer = tk.Frame(pane, bg="#0d1117")
pane.add(right_outer, minsize=400)

right_canvas = tk.Canvas(right_outer, bg="#0d1117", highlightthickness=0)
right_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(right_outer, orient=tk.VERTICAL,
                          command=right_canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

right_canvas.configure(yscrollcommand=scrollbar.set)

right = tk.Frame(right_canvas, bg="#0d1117", padx=16, pady=12)
right_canvas.create_window((0,0), window=right, anchor="nw")

def on_resize(e):
    right_canvas.configure(scrollregion=right_canvas.bbox("all"))

right.bind("<Configure>", on_resize)

right_canvas.bind("<MouseWheel>",
    lambda e: right_canvas.yview_scroll(-1*(e.delta//120), "units"))

placeholder = tk.Label(right, text="Results will appear here\nafter analysis.",
                         font=("Consolas", 13), fg="#21262d", bg="#0d1117",
                         justify="center")
placeholder.pack(expand=True, pady=80)

def render_results(d):
    for w in right.winfo_children():
        w.destroy()

    score = d.get("ats_score", 0)
    color = score_color(score)

    top_row = tk.Frame(right, bg="#0d1117")
    top_row.pack(fill=tk.X, pady=(0,10))

    circ = tk.Canvas(top_row, bg="#0d1117", highlightthickness=0)
    circ.pack(side=tk.LEFT, padx=(0,16))
    draw_circle_score(circ, score, color)

    verdict_frame = tk.Frame(top_row, bg="#0d1117")
    verdict_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    tk.Label(verdict_frame, text="ATS Score", font=("Consolas", 10),
             fg="#4a5568", bg="#0d1117").pack(anchor="w")

    tk.Label(verdict_frame, text=d.get("verdict",""), font=("Segoe UI", 11),
             fg="#c9d1d9", bg="#0d1117", wraplength=260, justify="left"
             ).pack(anchor="w", pady=(4,0))

    tk.Label(right, text="Section Breakdown", font=("Consolas", 11, "bold"),
             fg="#58a6ff", bg="#0d1117").pack(anchor="w", pady=(12,4))

    bar_frame = tk.Frame(right, bg="#0d1117")
    bar_frame.pack(fill=tk.X)

    for sec, sc in d.get("section_scores", {}).items():
        draw_bar(bar_frame, sec, sc, score_color(sc))

    tk.Label(right, text="Matched Keywords", font=("Consolas", 11, "bold"),
             fg="#58a6ff", bg="#0d1117").pack(anchor="w", pady=(14,2))
    pill_list(right, d.get("matched_keywords", []), "#0d3321", "#3fb950")

    tk.Label(right, text="Missing Keywords", font=("Consolas", 11, "bold"),
             fg="#58a6ff", bg="#0d1117").pack(anchor="w", pady=(8,2))
    pill_list(right, d.get("missing_keywords", []), "#3d1f1f", "#f85149")

    tk.Label(right, text="✦ Strengths", font=("Consolas", 11, "bold"),
             fg="#3fb950", bg="#0d1117").pack(anchor="w", pady=(14,4))
    bullet_list(right, d.get("strengths", []), "✓", "#3fb950")

    tk.Label(right, text="⚑ Improvements", font=("Consolas", 11, "bold"),
             fg="#f0883e", bg="#0d1117").pack(anchor="w", pady=(12,4))
    bullet_list(right, d.get("improvements", []), "→", "#f0883e")

    tk.Label(right, text="⚡ Quick Fixes", font=("Consolas", 11, "bold"),
             fg="#d2a8ff", bg="#0d1117").pack(anchor="w", pady=(12,4))
    bullet_list(right, d.get("quick_fixes", []), "•", "#d2a8ff")

    right_canvas.configure(scrollregion=right_canvas.bbox("all"))

def run_analysis():
    resume = resume_box.get("1.0", tk.END).strip()
    jd     = jd_box.get("1.0", tk.END).strip()

    if not resume:
        messagebox.showwarning("Missing", "Please paste or load your resume.")
        return
    if not jd:
        messagebox.showwarning("Missing", "Please paste the job description.")
        return

    analyze_btn.config(state=tk.DISABLED, text="Analyzing…")
    status_lbl.config(text="⏳ Sending to AI model…")

    def _worker():
        result = call_api(resume, jd)

        def _done():
            analyze_btn.config(state=tk.NORMAL, text="⚡  ANALYZE RESUME")
            if "error" in result:
                status_lbl.config(text=f"Error: {result['error']}", fg="#f85149")
            else:
                status_lbl.config(text="✔ Analysis complete", fg="#3fb950")
                render_results(result)

        root.after(0, _done)

    threading.Thread(target=_worker, daemon=True).start()

analyze_btn.config(command=run_analysis)

root.mainloop()
