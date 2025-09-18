import pandas as pd

def load_data():
    faculty_df = pd.read_csv("data/faculty.csv")
    def parse_list(df, col):
        df[col] = df[col].fillna("").apply(lambda x: [i.strip() for i in x.split(",") if i.strip()])
        return df

    faculty_df = parse_list(faculty_df, "subject_id")
    faculty_df = parse_list(faculty_df, "lab_id")

    subject_df = pd.read_csv("data/subjects.csv")
    lab_df = pd.read_csv("data/labs.csv")
    class_df = pd.read_csv("data/classes.csv")
    users_df = pd.read_csv("data/users.csv")

    return faculty_df, subject_df, lab_df, class_df, users_df

def authenticate_user(user_id, password, users_df):
    user = users_df[(users_df['user_id'] == user_id) & (users_df['password'] == password)]
    if not user.empty:
        return user.iloc[0].to_dict()
    return None

def export_timetable_csv(df, filename):
    df.to_csv(filename, index=False)

def export_timetable_excel(df, filename):
    df.to_excel(filename, index=False, engine='openpyxl')

def get_subject_name(subject_df, subject_id):
    row = subject_df[subject_df['subject_id'] == subject_id]
    if not row.empty:
        return row.iloc[0]['subject_name']
    return str(subject_id)
