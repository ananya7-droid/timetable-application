import pandas as pd
import streamlit as st
import os

# Mock in-memory users for login (replace with real DB in production)
USERS = {
    "admin": {"password": "admin123", "role": "admin", "faculty_id": "admin"},
    "santha_kumari": {"password": "santha123", "role": "teacher", "faculty_id": "F1"},
    "neeraja": {"password": "neeraja123", "role": "teacher", "faculty_id": "F2"},
    # Add all teachers similarly ...
}

def load_data():
    # Load CSV or Excel files - here we simulate as empty or minimal DataFrame for example
    faculty_df = pd.DataFrame([
        {"faculty_id": f"F{i+1}"} for i in range(25)
    ])
    subject_df = pd.DataFrame([
        {"subject_id": i} for i in range(101, 106)
    ])
    lab_df = pd.DataFrame()
    class_df = pd.DataFrame([
        {"class_id": 1, "class_name": "1st BSc Data Analytics"},
        {"class_id": 2, "class_name": "2nd BSc Data Analytics"},
        {"class_id": 3, "class_name": "3rd BSc Data Analytics"}
    ])
    timetable_df = pd.DataFrame()  # initial empty timetable
    return faculty_df, subject_df, lab_df, class_df, timetable_df

def authenticate_user(user_id, password):
    user = USERS.get(user_id)
    if user and user['password'] == password:
        return {"user_id": user_id, "role": user['role'], "faculty_id": user['faculty_id']}
    return None

def export_timetable_csv(df, filename):
    df.to_csv(filename, index=False)

def export_timetable_excel(df, filename):
    df.to_excel(filename, index=False, engine='openpyxl')

def get_teacher_timetable_week(timetable_df, faculty_id):
    # Return subset of timetable for the teacher for upcoming week
    # Here returning mock empty or prepared data
    if timetable_df.empty:
        return pd.DataFrame()
    return timetable_df[timetable_df['FacultyID'] == faculty_id]

def get_admin_timetable_semester(timetable_df, class_id):
    if timetable_df.empty:
        return pd.DataFrame()
    return timetable_df[timetable_df['ClassID'] == class_id]

def save_feedback(user_id, subject, message):
    if not os.path.exists("feedback.csv"):
        with open("feedback.csv", "w") as f:
            f.write("user_id,subject,message\n")
    with open("feedback.csv", "a") as f:
        f.write(f"{user_id},{subject},{message}\n")
