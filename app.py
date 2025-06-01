# Import necessary libraries
from flask import Flask, request, jsonify
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
import requests
import warnings
warnings.filterwarnings('ignore' )

# Flask App
app = Flask(__name__)

# Illness diagnosis logic (rules-based)
def diagnose(symptom):
    symptom = symptom.lower()

    diagnosis_data = {
        "fever": ("Flu", "General Physician", "Paracetamol"),
        "cough": ("Common Cold", "Pulmonologist", "Cough Syrup"),
        "headache": ("Migraine", "Neurologist", "Ibuprofen"),
        "sore throat": ("Throat Infection", "ENT Specialist", "Lozenges"),
        "chest pain": ("Heart Issue", "Cardiologist", "Aspirin"),
        "stomach pain": ("Gastritis", "Gastroenterologist", "Antacid"),
        "rash": ("Allergy", "Dermatologist", "Antihistamine"),
    }

    for key in diagnosis_data:
        if key in symptom:
            return diagnosis_data[key]

    return ("Unknown", "General Physician", "Consult Doctor")

# Database setup
def init_db():
    conn = sqlite3.connect("health.db")
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS patient (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            symptom TEXT,
            illness TEXT,
            doctor TEXT,
            medicine TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Insert data
@app.route('/add', methods=['POST'])
def add_patient():
    data = request.get_json()
    illness, doctor, medicine = diagnose(data['symptom'])

    conn = sqlite3.connect("health.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO patient (name, age, symptom, illness, doctor, medicine) VALUES (?, ?, ?, ?, ?, ?)",
                (data['name'], data['age'], data['symptom'], illness, doctor, medicine))
    conn.commit()
    conn.close()

    return jsonify({
        "status": "Patient added",
        "illness": illness,
        "doctor": doctor,
        "medicine": medicine
    }), 201

# Fetch data
@app.route('/patients', methods=['GET'])
def get_patients():
    conn = sqlite3.connect("health.db")
    df = pd.read_sql_query("SELECT * FROM patient", conn)
    conn.close()
    return df.to_json(orient="records")

# Simple visualization
def plot_symptoms():
    conn = sqlite3.connect("health.db")
    df = pd.read_sql_query("SELECT symptom FROM patient", conn)
    symptom_counts = df['symptom'].value_counts()
    symptom_counts.plot(kind='bar', color='skyblue')
    plt.title("Symptoms Frequency")
    plt.xlabel("Symptom")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig("symptoms_chart.png")
    plt.close()

# Tkinter GUI
def launch_gui():
    def submit():
        name = entry_name.get()
        age = int(entry_age.get())
        symptom = entry_symptom.get()

        try:
            response = requests.post("http://127.0.0.1:5000/add", json={
                "name": name,
                "age": age,
                "symptom": symptom
            })

            if response.status_code == 201:
                result = response.json()
                message = (
                    f"Illness: {result['illness']}\n"
                    f"Recommended Doctor: {result['doctor']}\n"
                    f"Suggested Medicine: {result['medicine']}"
                )
                messagebox.showinfo("Prediction Result", message)
            else:
                messagebox.showerror("Error", "Failed to add patient")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    root = tk.Tk()
    root.title("YourHealth Assistant")

    tk.Label(root, text="Name").grid(row=0)
    tk.Label(root, text="Age").grid(row=1)
    tk.Label(root, text="Symptom").grid(row=2)

    entry_name = tk.Entry(root)
    entry_age = tk.Entry(root)
    entry_symptom = tk.Entry(root)

    entry_name.grid(row=0, column=1)
    entry_age.grid(row=1, column=1)
    entry_symptom.grid(row=2, column=1)

    tk.Button(root, text='Submit', command=submit).grid(row=3, column=0, columnspan=2, pady=5)
    tk.Button(root, text='Visualize', command=plot_symptoms).grid(row=4, column=0, columnspan=2, pady=5)

    root.mainloop()

# Initialize DB
init_db()

# Flask app runner
if __name__ == '__main__':
    from threading import Thread
    # Run Flask in thread
    Thread(target=lambda: app.run(debug=False)).start()
    # Run GUI
    launch_gui()