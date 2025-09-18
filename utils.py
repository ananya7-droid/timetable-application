import pandas as pd

def load_data():
    faculty_df = pd.DataFrame([
        {"faculty_id": f"F{i+1}"} for i in range(25)
    ])
    subject_df = pd.DataFrame([
        {"subject_id": 101, "subject_name": "English 1", "type": "theory"},
        {"subject_id": 102, "subject_name": "Telugu 1", "type": "theory"},
        {"subject_id": 103, "subject_name": "Essential MPC", "type": "theory"},
        {"subject_id": 104, "subject_name": "Advanced MPC", "type": "theory"},
        {"subject_id": 105, "subject_name": "Design Thinking", "type": "theory"},
        {"subject_id": 106, "subject_name": "Principles of Management", "type": "theory"},
        {"subject_id": 201, "subject_name": "English 2", "type": "theory"},
        {"subject_id": 202, "subject_name": "Telugu 2", "type": "theory"},
        {"subject_id": 203, "subject_name": "Descriptive Statistics", "type": "theory"},
        {"subject_id": 204, "subject_name": "Discrete Mathematics", "type": "theory"},
        {"subject_id": 205, "subject_name": "Python Programming", "type": "theory"},
        {"subject_id": 206, "subject_name": "Environmental Education", "type": "theory"},
        {"subject_id": 207, "subject_name": "Economics", "type": "theory"},
        {"subject_id": 208, "subject_name": "Cyber Security", "type": "theory"},
        {"subject_id": 301, "subject_name": "UID", "type": "theory"},
        {"subject_id": 302, "subject_name": "DOD", "type": "theory"},
        {"subject_id": 303, "subject_name": "Java", "type": "theory"},
        {"subject_id": 304, "subject_name": "Algebra", "type": "theory"},
        {"subject_id": 305, "subject_name": "Random Variables", "type": "theory"},
        {"subject_id": 306, "subject_name": "Quantitative Aptitude", "type": "theory"},
        {"subject_id": 307, "subject_name": "Reasoning", "type": "theory"},
        {"subject_id": 401, "subject_name": "Prompt Engineering", "type": "theory"},
        {"subject_id": 402, "subject_name": "Exploratory Data Analysis", "type": "theory"},
        {"subject_id": 403, "subject_name": "Operating Systems", "type": "theory"},
        {"subject_id": 404, "subject_name": "Sampling Distributions", "type": "theory"},
        {"subject_id": 405, "subject_name": "Statistical Inference", "type": "theory"},
        {"subject_id": 501, "subject_name": "Natural Language Processing", "type": "theory"},
        {"subject_id": 502, "subject_name": "Big Data Analysis", "type": "theory"},
        {"subject_id": 503, "subject_name": "Power BI", "type": "theory"},
        {"subject_id": 504, "subject_name": "Machine Learning", "type": "theory"},
        {"subject_id": 505, "subject_name": "Applied Statistics", "type": "theory"},
        {"subject_id": 506, "subject_name": "Operations Research", "type": "theory"},
        # Labs with string IDs
        {"subject_id": "001", "subject_name": "Python Programming Lab", "type": "lab"},
        {"subject_id": "002", "subject_name": "Descriptive Statistics Lab", "type": "lab"},
        {"subject_id": "003", "subject_name": "UID Lab", "type": "lab"},
        {"subject_id": "004", "subject_name": "DOD Lab", "type": "lab"},
        {"subject_id": "005", "subject_name": "Java Lab", "type": "lab"},
        {"subject_id": "006", "subject_name": "Random Variables Lab", "type": "lab"},
        {"subject_id": "007", "subject_name": "Prompt Engineering Lab", "type": "lab"},
        {"subject_id": "008", "subject_name": "EDA Lab", "type": "lab"},
        {"subject_id": "009", "subject_name": "OS Lab", "type": "lab"},
        {"subject_id": "010", "subject_name": "Sampling Distributions Lab", "type": "lab"},
        {"subject_id": "011", "subject_name": "Statistical Inference Lab", "type": "lab"},
        {"subject_id": "012", "subject_name": "NLP Lab", "type": "lab"},
        {"subject_id": "013", "subject_name": "BDA Lab", "type": "lab"},
        {"subject_id": "014", "subject_name": "Power BI Lab", "type": "lab"},
        {"subject_id": "015", "subject_name": "ML Lab", "type": "lab"},
        {"subject_id": "016", "subject_name": "Applied Statistics Lab", "type": "lab"},
        {"subject_id": "017", "subject_name": "Operations Research Lab", "type": "lab"},
    ])
    lab_df = pd.DataFrame([])
    class_df = pd.DataFrame([
        {"class_id": 1, "class_name": "1st Year 1st Semester"},
        {"class_id": 2, "class_name": "1st Year 2nd Semester"},
        {"class_id": 3, "class_name": "2nd Year 3rd Semester"},
        {"class_id": 4, "class_name": "2nd Year 4th Semester"},
        {"class_id": 5, "class_name": "3rd Year 5th Semester"},
    ])
    timetable_df = pd.DataFrame()
    return faculty_df, subject_df, lab_df, class_df, timetable_df

def authenticate_user(user_id, password):
    return user_id == "admin" and password == "admin123"

def export_timetable_csv(df, filename):
    df.to_csv(filename, index=False)

def export_timetable_excel(df, filename):
    df.to_excel(filename, engine='openpyxl', index=False)

def get_subject_name(subject_df, subject_id):
    row = subject_df[subject_df['subject_id'] == subject_id]
    if not row.empty:
        return row.iloc[0]['subject_name']
    return str(subject_id)
