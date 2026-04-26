import tkinter as tk
from tkinter import Toplevel, filedialog, messagebox
from PIL import Image, ImageTk
import tensorflow as tf
from keras.preprocessing import image
import numpy as np

MODEL_PATH = r"leaf_classifier.h5"
model = tf.keras.models.load_model(MODEL_PATH)

class_names = ['diseased', 'healthy']

def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img) / 255.0
    return np.expand_dims(img_array, axis=0)

class TomatoClassifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tomato Crop Classifier: Healthy vs Diseased")
        self.root.geometry("500x650")
        self.root.configure(bg="#f9f9f9")
        self.root.resizable(False, False)
        title_label = tk.Label(root, text="Tomato Crop Classifier:\nHealthy vs Diseased",
                               font=("Helvetica", 18, "bold"), bg="#4CAF50", fg="white",
                               padx=10, pady=10)
        title_label.pack(fill=tk.X)

        self.upload_btn = tk.Button(root, text="Upload Image", font=("Helvetica", 14), bg="#008CBA", fg="white",
                                   activebackground="#005f73", padx=10, pady=5,
                                   command=self.open_upload_window)
        self.upload_btn.pack(pady=20)

        self.canvas = tk.Canvas(root, width=400, height=400, bg="white", bd=2, relief="solid")
        self.canvas.pack()

        self.pred_label = tk.Label(root, text="", font=("Helvetica", 16, "bold"),
                                   bg="#f9f9f9", fg="#333")
        self.pred_label.pack(pady=20)

        self.loaded_image = None

    def open_upload_window(self):
        self.upload_window = Toplevel(self.root)
        self.upload_window.title("Upload Image")
        self.upload_window.geometry("400x100")
        self.upload_window.resizable(False, False)
        self.upload_window.configure(bg="#f0f0f0")

        info_label = tk.Label(self.upload_window, text="Select an image file to classify:",
                              font=("Helvetica", 12), bg="#f0f0f0")
        info_label.pack(pady=10)

        select_btn = tk.Button(self.upload_window, text="Select Image",
                               font=("Helvetica", 12), command=self.upload_image)
        select_btn.pack()

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if not file_path:
            return

        self.upload_window.destroy()

        try:
            pil_img = Image.open(file_path).resize((400, 400), Image.Resampling.LANCZOS)
            self.loaded_image = ImageTk.PhotoImage(pil_img)
            self.canvas.delete("all")
            self.canvas.create_image(200, 200, image=self.loaded_image)

            preds = self.predict_image(file_path)
            self.show_prediction(preds)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to process image:\n{e}")

    def predict_image(self, img_path):
        processed_img = preprocess_image(img_path)
        preds = model.predict(processed_img)[0]
        return preds

    def show_prediction(self, preds):
        class_idx = np.argmax(preds)
        class_name = class_names[class_idx]
        confidence = preds[class_idx] * 100

        result_text = f"Prediction: {class_name.capitalize()}\nConfidence: {confidence:.2f}%"
        self.pred_label.config(text=result_text)

        if class_name == "healthy":
            self.pred_label.config(fg="#2E7D32")
        else:
            self.pred_label.config(fg="#C62828")

if __name__ == "__main__":
    root = tk.Tk()
    app = TomatoClassifierApp(root)
    root.mainloop()
