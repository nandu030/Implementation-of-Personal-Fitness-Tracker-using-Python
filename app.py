import csv
import os

def load_data(file_path):
    """Loads data from a CSV file."""
    if not os.path.exists(file_path):
        return []
    with open(file_path, mode='r', newline='') as file:
        return list(csv.DictReader(file))

def save_data(file_path, headers, records):
    """Saves records into a CSV file."""
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(records)

def add_exercise_record(user_id, gender, age, height, weight, time_spent, pulse, temperature):
    """Adds a new exercise record."""
    file = 'exercise_log.csv'
    fields = ['User_ID', 'Gender', 'Age', 'Height', 'Weight', 'Time_Spent', 'Pulse', 'Temperature']
    records = load_data(file)
    
    records.append({
        'User_ID': user_id,
        'Gender': gender,
        'Age': age,
        'Height': height,
        'Weight': weight,
        'Time_Spent': time_spent,
        'Pulse': pulse,
        'Temperature': temperature
    })
    
    save_data(file, fields, records)
    print("Exercise entry added successfully!")

def estimate_calories(time_spent, pulse, weight):
    """Calculates estimated calories burned."""
    return round((pulse * 0.7 + weight * 0.2 + time_spent * 0.15) * time_spent / 5, 2)

def log_calories(user_id, calories):
    """Stores calorie data."""
    file = 'calorie_tracker.csv'
    fields = ['User_ID', 'Calories_Burned']
    records = load_data(file)
    
    records.append({'User_ID': user_id, 'Calories_Burned': calories})
    save_data(file, fields, records)
    print("Calorie log updated!")

def display_user_records(user_id):
    """Retrieves and shows user exercise history."""
    file = 'exercise_log.csv'
    records = load_data(file)
    user_records = [record for record in records if record['User_ID'] == user_id]
    if not user_records:
        print("No records found for this user.")
    else:
        for record in user_records:
            print(record)

def main():
    user_id = input("Enter your User ID: ")
    gender = input("Enter Gender: ")
    age = int(input("Enter Age: "))
    height = int(input("Enter Height in cm: "))
    weight = int(input("Enter Weight in kg: "))
    time_spent = int(input("Enter Exercise Duration (min): "))
    pulse = int(input("Enter Average Heart Rate: "))
    temperature = float(input("Enter Body Temperature (°C): "))
    
    add_exercise_record(user_id, gender, age, height, weight, time_spent, pulse, temperature)
    calories = estimate_calories(time_spent, pulse, weight)
    log_calories(user_id, calories)
    print(f"Calories Burned: {calories} kcal")
    
    view_records = input("Do you want to see your past records? (yes/no): ").strip().lower()
    if view_records == 'yes':
        display_user_records(user_id)

if __name__ == "__main__":
    main()
