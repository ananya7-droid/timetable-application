import pandas as pd

def load_data():
    faculty_df = pd.read_csv("faculty.csv")
    subject_df = pd.read_csv("subjects.csv")
    lab_df = pd.read_csv("labs.csv")
    class_df = pd.read_csv("classes.csv")
    users_df = pd.read_csv("users.csv")  # For login validation if needed
    timetable_df = pd.DataFrame()  # Initially empty, generate in memory

    return faculty_df, subject_df, lab_df, class_df, users_df, timetable_df

def authenticate_user(user_id, password, users_df):
    user = users_df[(users_df['user_id'] == user_id) & (users_df['password'] == password)]
    if not user.empty:
        return True
    return False

def export_timetable_csv(df, filename):
    df.to_csv(filename, index=False)

def export_timetable_excel(df, filename):
    df.to_excel(filename, index=False, engine='openpyxl')

def get_subject_name(subject_df, subject_id):
    row = subject_df[subject_df['subject_id'] == subject_id]
    if not row.empty:
        return row.iloc[0]['subject_name']
    return str(subject_id)
