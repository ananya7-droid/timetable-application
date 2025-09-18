import pandas as pd

USERS = {
    "admin": {"password": "admin123", "role": "admin", "faculty_id": "admin"},
    "santha_kumari": {"password": "santha123", "role": "teacher", "faculty_id": "F1"},
    "neeraja": {"password": "neeraja123", "role": "teacher", "faculty_id": "F2"},
    "venkateswar_rao": {"password": "venkat123", "role": "teacher", "faculty_id": "F3"},
    "pandu_ranga_rao": {"password": "pandu123", "role": "teacher", "faculty_id": "F4"},
    "kiran": {"password": "kiran123", "role": "teacher", "faculty_id": "F5"},
    "sirisha": {"password": "sirisha123", "role": "teacher", "faculty_id": "F6"},
    "naga_sasanka": {"password": "naga123", "role": "teacher", "faculty_id": "F7"},
    "lakshmi": {"password": "lakshmi123", "role": "teacher", "faculty_id": "F8"},
    "naga_lakshmi": {"password": "nagalakshmi123", "role": "teacher", "faculty_id": "F9"},
    "munni_narendra": {"password": "munni123", "role": "teacher", "faculty_id": "F10"},
    "ravi_babu": {"password": "ravi123", "role": "teacher", "faculty_id": "F11"},
    "rakesh": {"password": "rakesh123", "role": "teacher", "faculty_id": "F12"},
    "kusuma_rohini": {"password": "kusuma123", "role": "teacher", "faculty_id": "F13"},
    "ravi_shankar": {"password": "ravishankar123", "role": "teacher", "faculty_id": "F14"},
    "sowmya": {"password": "sowmya123", "role": "teacher", "faculty_id": "F15"},
    "samhita_reddy": {"password": "samhita123", "role": "teacher", "faculty_id": "F16"},
    "sreeja": {"password": "sreeja123", "role": "teacher", "faculty_id": "F17"},
    "balaji": {"password": "balaji123", "role": "teacher", "faculty_id": "F18"},
    "venkatesh": {"password": "venkatesh123", "role": "teacher", "faculty_id": "F19"},
    "rajya_lakshmi": {"password": "rajya123", "role": "teacher", "faculty_id": "F20"},
    "swetha": {"password": "swetha123", "role": "teacher", "faculty_id": "F21"},
    "siva_naga_raju": {"password": "siva123", "role": "teacher", "faculty_id": "F22"},
    "kavya_sree": {"password": "kavya123", "role": "teacher", "faculty_id": "F23"},
    "sreenivasa_rao": {"password": "sreenivasa123", "role": "teacher", "faculty_id": "F24"},
    "raheem": {"password": "raheem123", "role": "teacher", "faculty_id": "F25"},
}

def load_data():
    # For demo, minimal dataframes with required columns only:
    faculty_df = pd.DataFrame([{"faculty_id": f"F{i+1}"} for i in range(25)])
    subject_df = pd.DataFrame([{"subject_id": i} for i in range(101, 106)])
    lab_df = pd.DataFrame()
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
    user = USERS.get(user_id)
    if user and user['password'] == password:
        return {"user_id": user_id, "role": user['role'], "faculty_id": user['faculty_id']}
    return None

def export_timetable_csv(df, filename):
    df.to_csv(filename, index=False)

def export_timetable_excel(df, filename):
    df.to_excel(filename, index=False, engine='openpyxl')

def get_teacher_timetable_week(timetable_df, faculty_id):
    if timetable_df.empty:
        return pd.DataFrame()
    # Here we assume 'FacultyID' and filter
    return timetable_df[timetable_df['FacultyID'] == faculty_id]

def get_admin_timetable_semester(timetable_df, class_id):
    if timetable_df.empty:
        return pd.DataFrame()
    # Filter by ClassID == class_id
    return timetable_df[timetable_df['ClassID'] == class_id]
