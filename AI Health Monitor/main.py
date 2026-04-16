import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import os
import math

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        canvas = tk.Canvas(self, bg='#f8f9fa')
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg='#f8f9fa')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

class CardiovascularHealthMonitor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("❤️ AI Cardiovascular Health Monitor")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f8f9fa')
        
        self.model = None
        self.scaler = StandardScaler()
        self.dataset = None
        self.accuracy = 0
        self.feature_importance = None
        self.report_text = ""
        
        self.load_dataset()
        
        if self.dataset is not None:
            self.train_model()
        
        self.create_gui()
        
    def load_dataset(self):
        possible_paths = [r"cardio_train.csv"]
        
        for path in possible_paths:
            if os.path.exists(path):
                try:
                    self.dataset = pd.read_csv(path, sep=';')
                    
                    self.preprocess_data()
                    
                    print(f"✅ Dataset loaded successfully: {len(self.dataset)} records")
                    return
                    
                except Exception as e:
                    print(f"❌ Error loading dataset from {path}: {e}")
                    continue
        
        print("📂 Dataset not found.")
    
    def preprocess_data(self):
        self.dataset['age'] = (self.dataset['age'] / 365.25).round().astype(int)
        
        self.dataset['bmi'] = self.dataset['weight'] / ((self.dataset['height'] / 100) ** 2)
        
        self.dataset = self.dataset[
            (self.dataset['ap_hi'] >= 80) & (self.dataset['ap_hi'] <= 200) &
            (self.dataset['ap_lo'] >= 60) & (self.dataset['ap_lo'] <= 140) &
            (self.dataset['ap_hi'] >= self.dataset['ap_lo']) &
            (self.dataset['height'] >= 120) & (self.dataset['height'] <= 220) &
            (self.dataset['weight'] >= 30) & (self.dataset['weight'] <= 200)
        ]
        
        print(f"📊 Data preprocessed: {len(self.dataset)} records after cleaning")
    
    def train_model(self):
        if self.dataset is None:
            raise ValueError("No dataset available for training")
        
        feature_columns = ['age', 'gender', 'height', 'weight', 'bmi', 
                          'ap_hi', 'ap_lo', 'cholesterol', 'gluc', 
                          'smoke', 'alco', 'active']
        
        X = self.dataset[feature_columns]
        y = self.dataset['cardio']
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            min_samples_split=10,
            min_samples_leaf=5,
            random_state=42,
            class_weight='balanced'
        )
        
        self.model.fit(X_train_scaled, y_train)
        
        y_pred = self.model.predict(X_test_scaled)
        self.accuracy = accuracy_score(y_test, y_pred)
        
        self.feature_importance = dict(zip(feature_columns, self.model.feature_importances_))
        
        self.report_text = classification_report(y_test, y_pred, target_names=['No CVD', 'CVD'])
        
        print(f"🤖 Model trained with {self.accuracy:.1%} accuracy")
        print("📊 Classification Report:")
        print(self.report_text)

    def create_gui(self):
        title_frame = tk.Frame(self.root, bg='#dc3545', height=100)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, 
                              text="❤️ AI CARDIOVASCULAR HEALTH MONITOR",
                              font=('Arial', 22, 'bold'),
                              bg='#dc3545', fg='white')
        title_label.pack(expand=True)
        
        subtitle = tk.Label(title_frame, 
                           text="Predict Cardiovascular Disease Risk using Machine Learning",
                           font=('Arial', 12),
                           bg='#dc3545', fg='#fff3f3')
        subtitle.pack()
        
        main_container = tk.Frame(self.root, bg='#f8f9fa')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        left_panel = tk.Frame(main_container, bg='#f8f9fa', width=400)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        scrollable_form = ScrollableFrame(left_panel)
        scrollable_form.pack(fill=tk.BOTH, expand=True)
        
        self.create_input_form(scrollable_form.scrollable_frame)
        
        button_frame = tk.Frame(left_panel, bg='#f8f9fa')
        button_frame.pack(fill=tk.X, pady=10)
        
        self.predict_btn = tk.Button(button_frame, 
                                    text="❤️ PREDICT CVD RISK",
                                    font=('Arial', 14, 'bold'),
                                    bg='#dc3545', fg='white',
                                    command=self.predict_cardiovascular_risk,
                                    height=2)
        self.predict_btn.pack(fill=tk.X, pady=(0, 5))
        
        clear_btn = tk.Button(button_frame, 
                             text="🗑️ Clear Form",
                             font=('Arial', 10),
                             bg='#6c757d', fg='white',
                             command=self.clear_form)
        clear_btn.pack(fill=tk.X)
        
        info_frame = tk.Frame(left_panel, bg='#f8f9fa')
        info_frame.pack(fill=tk.X, pady=(10, 0))
        
        if self.dataset is not None:
            dataset_size = len(self.dataset)
            cvd_cases = sum(self.dataset['cardio'])
            info_text = f"📊 Dataset: {dataset_size:,} records\n❤️ CVD Cases: {cvd_cases:,} ({cvd_cases/dataset_size:.1%})\n🤖 Model Accuracy: {self.accuracy:.1%}"
        else:
            info_text = "❌ Dataset not loaded"
            
        tk.Label(info_frame, text=info_text, font=('Arial', 9), bg='#f8f9fa',
                justify=tk.LEFT, fg='#6c757d').pack(anchor=tk.W)
        
        middle_panel = tk.Frame(main_container, bg='#f8f9fa', width=500)
        middle_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        middle_panel.pack_propagate(False)
        
        self.create_results_panel(middle_panel)
        
        right_panel = tk.Frame(main_container, bg='#f8f9fa', width=400)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        right_panel.pack_propagate(False)
        
        scrollable_graphs = ScrollableFrame(right_panel)
        scrollable_graphs.pack(fill=tk.BOTH, expand=True)
        
        graph_frame = tk.LabelFrame(scrollable_graphs.scrollable_frame, text="📊 Real-Time Prediction Probabilities", 
                                   font=('Arial', 12, 'bold'), bg='#f8f9fa')
        graph_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.fig, self.ax = plt.subplots(figsize=(2, 2))
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.ax.bar(['No CVD', 'CVD'], [0, 0], color=['#28a745', '#dc3545'])
        self.ax.set_ylabel('Probability')
        self.ax.set_ylim(0, 1)
        self.ax.set_title("Awaiting Prediction...")
        self.fig.tight_layout()
        self.canvas.draw()
        
        ecg_frame = tk.LabelFrame(scrollable_graphs.scrollable_frame, text="💓 Real-Time ECG Simulation", 
                                 font=('Arial', 12, 'bold'), bg='#f8f9fa')
        ecg_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.ecg_canvas = tk.Canvas(ecg_frame, height=150, bg='black')
        self.ecg_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.ecg_x = 0
        self.update_ecg_graph()

    def create_input_form(self, parent):
        form_frame = tk.LabelFrame(parent, text="👤 Patient Information", 
                                  font=('Arial', 14, 'bold'), bg='#f8f9fa',
                                  relief=tk.RAISED, bd=2)
        form_frame.pack(fill=tk.X, padx=10, pady=10)
        
        obj_frame = tk.LabelFrame(form_frame, text="📋 Objective Features (Factual)", 
                                 font=('Arial', 12, 'bold'), bg='#f8f9fa')
        obj_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(obj_frame, text="Age (years):", font=('Arial', 10), bg='#f8f9fa').pack(anchor=tk.W, padx=10, pady=2)
        self.age_var = tk.StringVar(value="45")
        tk.Spinbox(obj_frame, from_=18, to=80, textvariable=self.age_var,
                  font=('Arial', 10), width=20).pack(anchor=tk.W, padx=10, pady=2)
        
        tk.Label(obj_frame, text="Gender:", font=('Arial', 10), bg='#f8f9fa').pack(anchor=tk.W, padx=10, pady=2)
        self.gender_var = tk.StringVar(value="1")
        gender_frame = tk.Frame(obj_frame, bg='#f8f9fa')
        gender_frame.pack(anchor=tk.W, padx=10, pady=2)
        tk.Radiobutton(gender_frame, text="Female", variable=self.gender_var, value="1",
                      bg='#f8f9fa').pack(side=tk.LEFT)
        tk.Radiobutton(gender_frame, text="Male", variable=self.gender_var, value="2",
                      bg='#f8f9fa').pack(side=tk.LEFT, padx=(20, 0))
        
        tk.Label(obj_frame, text="Height (cm):", font=('Arial', 10), bg='#f8f9fa').pack(anchor=tk.W, padx=10, pady=2)
        self.height_var = tk.StringVar(value="170")
        tk.Spinbox(obj_frame, from_=140, to=220, textvariable=self.height_var,
                  font=('Arial', 10), width=20).pack(anchor=tk.W, padx=10, pady=2)
        
        tk.Label(obj_frame, text="Weight (kg):", font=('Arial', 10), bg='#f8f9fa').pack(anchor=tk.W, padx=10, pady=2)
        self.weight_var = tk.StringVar(value="70")
        tk.Spinbox(obj_frame, from_=30, to=200, textvariable=self.weight_var,
                  font=('Arial', 10), width=20).pack(anchor=tk.W, padx=10, pady=2)
        
        exam_frame = tk.LabelFrame(form_frame, text="🩺 Examination Features (Medical)", 
                                  font=('Arial', 12, 'bold'), bg='#f8f9fa')
        exam_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(exam_frame, text="Systolic Blood Pressure (ap_hi):", font=('Arial', 10), bg='#f8f9fa').pack(anchor=tk.W, padx=10, pady=2)
        self.systolic_var = tk.StringVar(value="120")
        tk.Spinbox(exam_frame, from_=80, to=200, textvariable=self.systolic_var,
                  font=('Arial', 10), width=20).pack(anchor=tk.W, padx=10, pady=2)
        
        tk.Label(exam_frame, text="Diastolic Blood Pressure (ap_lo):", font=('Arial', 10), bg='#f8f9fa').pack(anchor=tk.W, padx=10, pady=2)
        self.diastolic_var = tk.StringVar(value="80")
        tk.Spinbox(exam_frame, from_=60, to=140, textvariable=self.diastolic_var,
                  font=('Arial', 10), width=20).pack(anchor=tk.W, padx=10, pady=2)
        
        tk.Label(exam_frame, text="Cholesterol Level:", font=('Arial', 10), bg='#f8f9fa').pack(anchor=tk.W, padx=10, pady=2)
        self.cholesterol_var = tk.StringVar(value="1")
        cholesterol_combo = ttk.Combobox(exam_frame, textvariable=self.cholesterol_var,
                                       values=["1 (Normal)", "2 (Above Normal)", "3 (Well Above Normal)"],
                                       font=('Arial', 10), width=25, state="readonly")
        cholesterol_combo.pack(anchor=tk.W, padx=10, pady=2)
        
        tk.Label(exam_frame, text="Glucose Level:", font=('Arial', 10), bg='#f8f9fa').pack(anchor=tk.W, padx=10, pady=2)
        self.glucose_var = tk.StringVar(value="1")
        glucose_combo = ttk.Combobox(exam_frame, textvariable=self.glucose_var,
                                   values=["1 (Normal)", "2 (Above Normal)", "3 (Well Above Normal)"],
                                   font=('Arial', 10), width=25, state="readonly")
        glucose_combo.pack(anchor=tk.W, padx=10, pady=2)
        
        subj_frame = tk.LabelFrame(form_frame, text="🗣️ Subjective Features (Patient Reported)", 
                                  font=('Arial', 12, 'bold'), bg='#f8f9fa')
        subj_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.smoke_var = tk.BooleanVar()
        tk.Checkbutton(subj_frame, text="Smoking", variable=self.smoke_var,
                      bg='#f8f9fa', font=('Arial', 10)).pack(anchor=tk.W, padx=10, pady=2)
        
        self.alcohol_var = tk.BooleanVar()
        tk.Checkbutton(subj_frame, text="Alcohol Intake", variable=self.alcohol_var,
                      bg='#f8f9fa', font=('Arial', 10)).pack(anchor=tk.W, padx=10, pady=2)
        
        self.active_var = tk.BooleanVar(value=True)
        tk.Checkbutton(subj_frame, text="Physical Activity", variable=self.active_var,
                      bg='#f8f9fa', font=('Arial', 10)).pack(anchor=tk.W, padx=10, pady=2)

    def create_results_panel(self, parent):
        results_frame = tk.LabelFrame(parent, text="📋 Cardiovascular Disease Risk Assessment", 
                                     font=('Arial', 14, 'bold'), bg='#f8f9fa')
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        self.results_text = tk.Text(results_frame, height=25, font=('Arial', 11),
                                   wrap=tk.WORD, bg='white', relief=tk.SUNKEN, bd=2)
        
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        self.results_text.pack(side="left", fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        self.results_text.tag_configure('title', font=('Arial', 14, 'bold'), foreground='#dc3545')
        self.results_text.tag_configure('low_risk', font=('Arial', 12, 'bold'), foreground='#28a745')
        self.results_text.tag_configure('high_risk', font=('Arial', 12, 'bold'), foreground='#dc3545')
        self.results_text.tag_configure('normal', foreground='#495057')
        self.results_text.tag_configure('warning', font=('Arial', 11, 'bold'), foreground='#ffc107')
        self.results_text.tag_configure('info', font=('Arial', 10, 'italic'), foreground='#6c757d')
        
        self.display_initial_message()

    def display_initial_message(self):
        self.results_text.delete(1.0, tk.END)
        
        self.results_text.insert(tk.END, "❤️ CARDIOVASCULAR DISEASE RISK PREDICTOR\n\n", 'title')
        
        if self.model is None:
            self.results_text.insert(tk.END, "❌ Model not available. Please check dataset.\n\n", 'high_risk')
            return
        
        self.results_text.insert(tk.END, "Welcome to the AI-powered cardiovascular disease risk assessment!\n\n")
        
        self.results_text.insert(tk.END, "📊 Dataset Information:\n", 'title')
        self.results_text.insert(tk.END, f"• Total Records: {len(self.dataset):,}\n")
        self.results_text.insert(tk.END, f"• CVD Cases: {sum(self.dataset['cardio']):,}\n")
        self.results_text.insert(tk.END, f"• Model Accuracy: {self.accuracy:.1%}\n\n")
        
        self.results_text.insert(tk.END, "🔬 Model Performance:\n", 'title')
        self.results_text.insert(tk.END, self.report_text + "\n")
        
        self.results_text.insert(tk.END, "📋 Dataset Features:\n", 'title')
        features_info = [
            "• Objective: Age, Height, Weight, Gender",
            "• Medical: Blood Pressure, Cholesterol, Glucose",
            "• Lifestyle: Smoking, Alcohol, Physical Activity",
        ]
        
        for info in features_info:
            self.results_text.insert(tk.END, f"{info}\n")
        
        self.results_text.insert(tk.END, "\n💡 Fill out the form and click 'Predict CVD Risk' to get your assessment!\n\n")
        
        if self.feature_importance:
            self.results_text.insert(tk.END, "🎯 Most Important Risk Factors:\n", 'title')
            sorted_features = sorted(self.feature_importance.items(), key=lambda x: x[1], reverse=True)
            for feature, importance in sorted_features[:5]:
                self.results_text.insert(tk.END, f"• {feature}: {importance:.3f}\n")

    def predict_cardiovascular_risk(self):
        if self.model is None:
            messagebox.showerror("Error", "Model not available. Please check dataset.")
            return
        
        try:
            age = float(self.age_var.get())
            gender = int(self.gender_var.get())
            height = float(self.height_var.get())
            weight = float(self.weight_var.get())
            systolic = float(self.systolic_var.get())
            diastolic = float(self.diastolic_var.get())
            cholesterol = int(self.cholesterol_var.get().split()[0])
            glucose = int(self.glucose_var.get().split()[0])
            smoke = int(self.smoke_var.get())
            alcohol = int(self.alcohol_var.get())
            active = int(self.active_var.get())
            
            bmi = weight / ((height / 100) ** 2)
            
            self.validate_inputs(age, height, weight, systolic, diastolic)
            
            features = np.array([[age, gender, height, weight, bmi, 
                                systolic, diastolic, cholesterol, glucose,
                                smoke, alcohol, active]])
            
            features_scaled = self.scaler.transform(features)
            
            prediction = self.model.predict(features_scaled)[0]
            prediction_proba = self.model.predict_proba(features_scaled)[0]
            
            self.display_prediction_results(
                age, gender, height, weight, bmi, systolic, diastolic,
                cholesterol, glucose, smoke, alcohol, active,
                prediction, prediction_proba
            )
            
            self.update_prediction_graph(prediction_proba)
            
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Prediction Error", f"Error making prediction: {str(e)}")

    def validate_inputs(self, age, height, weight, systolic, diastolic):
        if not (18 <= age <= 80):
            raise ValueError("Age must be between 18-80 years")
        if not (140 <= height <= 220):
            raise ValueError("Height must be between 140-220 cm")
        if not (30 <= weight <= 200):
            raise ValueError("Weight must be between 30-200 kg")
        if not (80 <= systolic <= 200):
            raise ValueError("Systolic BP must be between 80-200 mmHg")
        if not (60 <= diastolic <= 140):
            raise ValueError("Diastolic BP must be between 60-140 mmHg")
        if systolic <= diastolic:
            raise ValueError("Systolic BP must be higher than Diastolic BP")

    def display_prediction_results(self, age, gender, height, weight, bmi, 
                                 systolic, diastolic, cholesterol, glucose,
                                 smoke, alcohol, active, prediction, prediction_proba):
        self.results_text.delete(1.0, tk.END)
        
        self.results_text.insert(tk.END, "❤️ CARDIOVASCULAR DISEASE RISK ASSESSMENT\n", 'title')
        self.results_text.insert(tk.END, "=" * 55 + "\n\n", 'title')
        
        self.results_text.insert(tk.END, "👤 Patient Profile:\n", 'title')
        gender_text = "Female" if gender == 1 else "Male"
        self.results_text.insert(tk.END, f"Age: {age} years, Gender: {gender_text}\n")
        self.results_text.insert(tk.END, f"Height: {height} cm, Weight: {weight} kg\n")
        self.results_text.insert(tk.END, f"BMI: {bmi:.1f}")
        
        if bmi < 18.5:
            self.results_text.insert(tk.END, " (Underweight)\n\n", 'warning')
        elif bmi < 25:
            self.results_text.insert(tk.END, " (Normal)\n\n", 'low_risk')
        elif bmi < 30:
            self.results_text.insert(tk.END, " (Overweight)\n\n", 'warning')
        else:
            self.results_text.insert(tk.END, " (Obese)\n\n", 'high_risk')
        
        cvd_probability = prediction_proba[1] * 100
        no_cvd_probability = prediction_proba[0] * 100
        
        self.results_text.insert(tk.END, "🎯 CARDIOVASCULAR DISEASE PREDICTION:\n", 'title')
        
        if prediction == 0:
            self.results_text.insert(tk.END, "✅ LOW RISK - No CVD Predicted\n\n", 'low_risk')
        else:
            self.results_text.insert(tk.END, "⚠️ HIGH RISK - CVD Predicted\n\n", 'high_risk')
        
        self.results_text.insert(tk.END, f"📊 Prediction Probabilities:\n", 'title')
        self.results_text.insert(tk.END, f"• No CVD: {no_cvd_probability:.1f}%\n", 'low_risk' if no_cvd_probability > 50 else 'normal')
        self.results_text.insert(tk.END, f"• CVD Risk: {cvd_probability:.1f}%\n\n", 'high_risk' if cvd_probability > 50 else 'normal')
        
        self.results_text.insert(tk.END, "🩺 Medical Analysis:\n", 'title')
        self.results_text.insert(tk.END, f"Blood Pressure: {systolic}/{diastolic} mmHg ")
        
        if systolic >= 140 or diastolic >= 90:
            self.results_text.insert(tk.END, "(High - Stage 2 Hypertension)\n", 'high_risk')
        elif systolic >= 130 or diastolic >= 80:
            self.results_text.insert(tk.END, "(Elevated - Stage 1 Hypertension)\n", 'warning')
        else:
            self.results_text.insert(tk.END, "(Normal)\n", 'low_risk')
        
        chol_levels = ["Normal", "Above Normal", "Well Above Normal"]
        gluc_levels = ["Normal", "Above Normal", "Well Above Normal"]
        
        self.results_text.insert(tk.END, f"Cholesterol: {chol_levels[cholesterol-1]}\n")
        self.results_text.insert(tk.END, f"Glucose: {gluc_levels[glucose-1]}\n\n")
        
        self.results_text.insert(tk.END, "🗣️ Lifestyle Factors:\n", 'title')
        self.results_text.insert(tk.END, f"Smoking: {'Yes' if smoke else 'No'}\n")
        self.results_text.insert(tk.END, f"Alcohol: {'Yes' if alcohol else 'No'}\n")
        self.results_text.insert(tk.END, f"Physical Activity: {'Yes' if active else 'No'}\n\n")
        
        risk_factors = []
        if age >= 60: risk_factors.append("Advanced age")
        if bmi >= 30: risk_factors.append("Obesity")
        if systolic >= 140 or diastolic >= 90: risk_factors.append("High blood pressure")
        if cholesterol >= 3: risk_factors.append("High cholesterol")
        if glucose >= 3: risk_factors.append("High glucose")
        if smoke: risk_factors.append("Smoking")
        if not active: risk_factors.append("Physical inactivity")
        
        self.results_text.insert(tk.END, f"⚠️ Identified Risk Factors ({len(risk_factors)}):\n", 'title')
        if risk_factors:
            for factor in risk_factors:
                self.results_text.insert(tk.END, f"• {factor}\n", 'warning')
        else:
            self.results_text.insert(tk.END, "• No major risk factors identified\n", 'low_risk')
        
        self.results_text.insert(tk.END, "\n💡 Recommendations:\n", 'title')
        recommendations = []
        
        if prediction == 1:
            recommendations.append("Consult with a cardiologist for comprehensive evaluation")
            recommendations.append("Consider cardiac screening tests (ECG, stress test)")
        
        if bmi >= 25:
            recommendations.append("Maintain healthy weight through diet and exercise")
        
        if systolic >= 130 or diastolic >= 80:
            recommendations.append("Monitor blood pressure regularly")
            recommendations.append("Reduce sodium intake and manage stress")
        
        if smoke:
            recommendations.append("Quit smoking - seek professional help if needed")
        
        if not active:
            recommendations.append("Incorporate regular physical activity (150 min/week)")
        
        recommendations.append("Maintain a heart-healthy diet rich in fruits and vegetables")
        recommendations.append("Regular health check-ups and monitoring")
        
        for rec in recommendations:
            self.results_text.insert(tk.END, f"• {rec}\n")
        
        self.results_text.insert(tk.END, f"\n🤖 Model trained on {len(self.dataset):,} patient records with {self.accuracy:.1%} accuracy.", 'info')

    def update_prediction_graph(self, prediction_proba):
        self.ax.clear()
        
        bars = self.ax.bar(['No CVD', 'CVD'], 
                          [prediction_proba[0], prediction_proba[1]], 
                          color=['#28a745', '#dc3545'])
        
        for i, bar in enumerate(bars):
            height = bar.get_height()
            self.ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                        f'{prediction_proba[i]*100:.1f}%',
                        ha='center', va='bottom', fontweight='bold')
        
        self.ax.set_ylabel('Probability')
        self.ax.set_ylim(0, 1)
        self.ax.set_title("Real-Time Prediction Probabilities")
        self.ax.grid(axis='y', alpha=0.3)
        
        self.fig.tight_layout()
        self.canvas.draw()

    def update_ecg_graph(self):
        self.ecg_canvas.delete("all")
        
        width = self.ecg_canvas.winfo_width() or 400
        height = self.ecg_canvas.winfo_height() or 150
        
        points = []
        for x in range(0, width, 2):
            t = (self.ecg_x + x) * 0.02
            
            base_wave = 15 * math.sin(t * 0.8)
            
            qrs_spike = 0
            phase = t % (2 * math.pi)
            if 1.0 < phase < 1.5:
                qrs_spike = 40 * math.sin((phase - 1.0) * 4 * math.pi)
            elif 2.0 < phase < 2.8:
                qrs_spike = 20 * math.sin((phase - 2.0) * 2 * math.pi)
            
            y = height//2 + base_wave + qrs_spike
            points.extend([x, y])
        
        if len(points) > 4:
            self.ecg_canvas.create_line(points, fill='lime', width=2, smooth=True)
        
        for i in range(0, width, 40):
            self.ecg_canvas.create_line(i, 0, i, height, fill='darkgreen', width=1)
        for i in range(0, height, 20):
            self.ecg_canvas.create_line(0, i, width, i, fill='darkgreen', width=1)
        
        self.ecg_x += 2
        self.root.after(100, self.update_ecg_graph)

    def clear_form(self):
        self.age_var.set("45")
        self.gender_var.set("1")
        self.height_var.set("170")
        self.weight_var.set("70")
        self.systolic_var.set("120")
        self.diastolic_var.set("80")
        self.cholesterol_var.set("1")
        self.glucose_var.set("1")
        self.smoke_var.set(False)
        self.alcohol_var.set(False)
        self.active_var.set(True)
        
        self.display_initial_message()
        
        self.ax.clear()
        self.ax.bar(['No CVD', 'CVD'], [0, 0], color=['#28a745', '#dc3545'])
        self.ax.set_ylabel('Probability')
        self.ax.set_ylim(0, 1)
        self.ax.set_title("Awaiting Prediction...")
        self.fig.tight_layout()
        self.canvas.draw()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    print("❤️ CARDIOVASCULAR DISEASE RISK PREDICTOR")
    print("=" * 50)
    print("\nStarting application...")
    print("=" * 50)
    
    try:
        app = CardiovascularHealthMonitor()
        app.run()
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        import traceback
        traceback.print_exc()
