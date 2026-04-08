import tkinter as tk
from tkinter import ttk, scrolledtext
import requests, threading

API_KEY = ""
URL     = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT = """You are a helpful school assistant bot.
Answer clearly, simply, and politely.
Explain concepts like a teacher.
Keep answers short and easy to understand.
"""

def ask_ai(user_input):
    try:
        r = requests.post(URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost",
                "X-Title": "SchoolBot"
            },
            json={
                "model": "openrouter/free",
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user",   "content": user_input}
                ]
            },
            timeout=30
        )
        data = r.json()
        if "choices" in data:
            return data["choices"][0]["message"]["content"].strip()
        elif "error" in data:
            return f"API Error: {data['error']['message']}"
        else:
            return f"Unexpected: {data}"
    except Exception as e:
        return f"Error: {e}"

def add(sender, msg, tag):
    chat.config(state=tk.NORMAL)
    chat.insert(tk.END, f"{sender}:\n", tag+"_s")
    chat.insert(tk.END, f"{msg}\n\n", tag)
    chat.config(state=tk.DISABLED)
    chat.see(tk.END)

def handle_ai(prompt):
    root.after(0, lambda: add("🤖 School Bot", "Thinking...", "bot"))
    reply = ask_ai(prompt)
    root.after(0, lambda: add("🤖 School Bot", reply, "bot"))

def send(event=None):
    text = entry.get().strip()
    if not text: return
    entry.delete(0, tk.END)
    add("🧑 You", text, "user")
    threading.Thread(target=handle_ai, args=(text,), daemon=True).start()

root = tk.Tk()
root.title("🎓 School Assistant Bot")
root.geometry("900x600")

chat = scrolledtext.ScrolledText(root, font=("Segoe UI", 12), state=tk.DISABLED)
chat.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
chat.tag_config("user_s", foreground="#0056A6", font=("Segoe UI", 10, "bold"))
chat.tag_config("user",   foreground="#003366")
chat.tag_config("bot_s",  foreground="#1a7431", font=("Segoe UI", 10, "bold"))
chat.tag_config("bot",    foreground="#0f5132")

frame = tk.Frame(root)
frame.pack(fill=tk.X, padx=10, pady=5)
entry = ttk.Entry(frame, font=("Segoe UI", 12))
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,5))
entry.bind("<Return>", send)
ttk.Button(frame, text="Send", command=send).pack(side=tk.RIGHT)
entry.focus()
root.mainloop()
