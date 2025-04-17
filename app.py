import streamlit as st
import csv
import os

def load_data(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, mode='r', newline='') as file:
        return list(csv.DictReader(file))

def save_data(file_path, headers, records):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(records)

def add_exercise_record(data):
    file = 'exercise_log.csv'
    fields = list(data.keys())
    records = load_data(file)
    records.append(data)
    save_data(file, fields, records)

def estimate_calories(time_spent, pulse, weight):
    return round((pulse * 0.7 + weight * 0.2 + time_spent * 0.15) * time_spent / 5, 2)

def log_calories(user_id, calories):
    file = 'calorie_tracker.csv'
    fields = ['User_ID', 'Calories_Burned']
    records = load_data(file)
    records.append({'User_ID': user_id, 'Calories_Burned': calories})
    save_data(file, fields, records)

def display_user_records(user_id):
    records = load_data('exercise_log.csv')
    return [r for r in records if r['User_ID'] == user_id]

# --- Streamlit App ---
st.title("🏋️‍♀️ Fitness Tracker")

st.subheader("Enter Exercise Data")
user_id = st.text_input("User ID")
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
age = st.number_input("Age", min_value=10, max_value=100)
height = st.number_input("Height (cm)", min_value=100, max_value=250)
weight = st.number_input("Weight (kg)", min_value=30, max_value=200)
time_spent = st.number_input("Exercise Duration (min)", min_value=1, max_value=180)
pulse = st.number_input("Average Heart Rate", min_value=40, max_value=200)
temperature = st.number_input("Body Temperature (°C)", min_value=35.0, max_value=42.0)

if st.button("Submit"):
    record = {
        'User_ID': user_id,
        'Gender': gender,
        'Age': str(age),
        'Height': str(height),
        'Weight': str(weight),
        'Time_Spent': str(time_spent),
        'Pulse': str(pulse),
        'Temperature': str(temperature)
    }
    add_exercise_record(record)
    calories = estimate_calories(time_spent, pulse, weight)
    log_calories(user_id, calories)
    st.success(f"Calories Burned: {calories} kcal")

st.subheader("📖 View Past Records")
if st.button("Show Records"):
    history = display_user_records(user_id)
    if history:
        st.write(history)
    else:
        st.info("No records found for this user.")
