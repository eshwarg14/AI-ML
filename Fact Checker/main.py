import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests, threading

class FakeNewsDetector:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔍 Fake News Detector")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f2f5")

        self.api_key = ""
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        
        self.model = "openrouter/free"

        self.setup_ui()

    def setup_ui(self):
        self.header = tk.Frame(self.root, bg="#2c3e50", height=60)
        self.header.pack(fill=tk.X)
        tk.Label(self.header, text="AI FACT CHECKER", font=("Arial", 16, "bold"), fg="white", bg="#2c3e50").pack(pady=15)
        
        main = tk.Frame(self.root, bg="#f0f2f5")
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.input_text = scrolledtext.ScrolledText(main, height=8, font=("Segoe UI", 11))
        self.input_text.pack(fill=tk.X, pady=10)

        btn_frame = tk.Frame(main, bg="#f0f2f5")
        btn_frame.pack(fill=tk.X)

        self.check_btn = ttk.Button(btn_frame, text="Analyze", command=self.start)
        self.check_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="Key", command=self.set_key).pack(side=tk.LEFT, padx=5)
        self.progress = ttk.Progressbar(btn_frame, mode="indeterminate", length=150)
        self.progress.pack(side=tk.RIGHT)

        self.output_text = scrolledtext.ScrolledText(main, height=15, font=("Consolas", 10))
        self.output_text.pack(fill=tk.BOTH, expand=True, pady=10)

        self.status = tk.Label(self.root, text="Ready", bg="#2c3e50", fg="white", anchor="w", padx=10)
        self.status.pack(fill=tk.X, side=tk.BOTTOM)

    def set_key(self):
        pass

    def start(self):
        text = self.input_text.get("1.0", tk.END).strip()
        if not text or not self.api_key.startswith("sk-or-"):
            return messagebox.showwarning("Setup", "Enter text and ensure API key is set.")
        
        self.output_text.delete("1.0", tk.END)
        self.progress.start(10)
        self.check_btn.config(state="disabled")
        threading.Thread(target=self.call_api, args=(text,), daemon=True).start()

    def call_api(self, text):
        try:
            self.root.after(0, lambda: self.status.config(text="Analyzing..."))
            
            response = requests.post(
                self.url,
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": f"Fact check this: {text[:800]}"}],
                    "temperature": 0.1
                },
                timeout=20
            )

            if response.status_code == 200:
                data = response.json()
                result = data["choices"][0]["message"]["content"]
            else:
                result = f"Error {response.status_code}: {response.text}"

        except Exception as e:
            result = f"Request Failed: {str(e)}"

        self.root.after(0, self.finish, result)

    def finish(self, result):
        self.progress.stop()
        self.check_btn.config(state="normal")
        self.status.config(text="Done")
        self.output_text.insert(tk.END, result)

if __name__ == "__main__":
    FakeNewsDetector().root.mainloop()
