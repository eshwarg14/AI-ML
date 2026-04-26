# 🍅 AI Tomato Leaf Disease Classifier

An AI-powered image classification system that detects whether a tomato leaf is **Healthy or Diseased** using Deep Learning. Built with TensorFlow, MobileNetV2, and Tkinter GUI, this project helps in early detection of crop diseases.

---

## Preview

![Demo](https://github.com/eshwarg14/AI-ML/raw/7a9a3ed688595454f8e440d9dc6823cab0b20e2c/Images/DL1.png)
![Demo](https://github.com/eshwarg14/AI-ML/raw/7a9a3ed688595454f8e440d9dc6823cab0b20e2c/Images/HL1.png)

---

## ✨ Features

- 🍅 Detects healthy vs diseased leaves  
- 🤖 Deep Learning model (MobileNetV2)  
- 🖼️ Image upload & preview  
- 📊 Confidence score output  
- 🖥️ Simple GUI using Tkinter  
- ⚡ Fast prediction  

---

## 🧠 What is Image Classification?

Image classification is a Computer Vision task where:

- Input → Image  
- Output → Label (e.g., Healthy / Diseased)  

---

## 🤖 Deep Learning Model

### 📱 MobileNetV2 (Transfer Learning)

- Pre-trained on ImageNet  
- Lightweight & fast  
- Ideal for low-end systems  

👉 Why used?
- High accuracy  
- Less training time  
- Efficient performance  

---

## 🧠 Technologies Used

```
tensorflow
keras
opencv (optional)
numpy
pillow
tkinter
```

📦 Install dependencies:

```bash
pip install tensorflow pillow numpy
```

---

## ▶️ How to Run

```bash
python main.py
```

---

## 📁 Project Structure

```
├── main.py                 # GUI application
├── leaf_classifier.h5      # Trained model
├── train.py                # Training script
├── train/                  # Dataset (healthy / diseased folders)
│   ├── healthy.zip
│   └── diseased.zip              
└── README.md
```

---

## 📊 Dataset

- 📁 Folder: `train/`  
---

## 🛠️ Step-by-Step Working

### 1️⃣ Data Loading
- Images loaded using ImageDataGenerator  
- Augmentation applied:
  - Rotation  
  - Zoom  
  - Flip  

---

### 2️⃣ Model Building

- Base model: MobileNetV2  
- Top layers:
  - GlobalAveragePooling  
  - Dense layer  
  - Dropout  

---

### 3️⃣ Training

- Optimizer: Adam  
- Loss: Categorical Crossentropy  
- Epochs: 5  

---

### 4️⃣ Model Saving

```python
model.save("leaf_classifier.h5")
```

---

### 5️⃣ Prediction (GUI)

- User uploads image  
- Image resized → 224x224  
- Model predicts class  
- Output:
  - Healthy ✅  
  - Diseased ⚠️  
- Confidence displayed  

---

## 🎯 Output Example

```
Prediction: Healthy
Confidence: 96.45%
```

---

## ⚠️ Important Notes

- 🐍 Python 3.8+ required  
- 🖼️ Input image should be clear  
- 📊 Accuracy depends on dataset quality  

---

## 🔧 Important Fix

Your current model path is:

```
E:...
```

👉 Replace with:

```python
MODEL_PATH = "leaf_classifier.h5"
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

- Multi-disease classification 🌿  
- Real-time camera detection 📷  
- Mobile app integration 📱  
- Cloud-based prediction ☁️  
