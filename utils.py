import pandas as pd

def load_data():
    # Load all CSV files as-is
    faculty_df = pd.read_csv("data/faculty.csv")
    subject_df = pd.read_csv("data/subjects.csv")
    lab_df = pd.read_csv("data/labs.csv")
    class_df = pd.read_csv("data/classes.csv")
    users_df = pd.read_csv("data/users.csv")
    timetable_df = pd.read_csv("data/timetable.csv")  # Your provided timetable
    return faculty_df, subject_df, lab_df, class_df, users_df, timetable_df

def authenticate_user(user_id, password, users_df):
    user = users_df[(users_df['user_id'] == user_id) & (users_df['password'] == password)]
    if not user.empty:
        return user.iloc[0].to_dict()
    return None

def export_timetable_excel(df, filename):
    df.to_excel(filename, index=False, engine='openpyxl')
