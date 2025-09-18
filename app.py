import streamlit as st
import pandas as pd
from scheduler import generate_timetable
from utils import get_teacher_timetable

# Load CSVs
faculty_df = pd.read_csv("data/faculty.csv")
subjects_df = pd.read_csv("data/subjects.csv")
labs_df = pd.read_csv("data/labs.csv")
classes_df = pd.read_csv("data/classes.csv")
users_df = pd.read_csv("data/users.csv")

st.title("Timetable App")

# Mappings
subject_map = pd.Series(subjects_df['subject_name'].values, index=subjects_df['subject_id']).to_dict()
faculty_map = pd.Series(faculty_df['faculty_name'].values, index=faculty_df['faculty_id']).to_dict()

def format_cell(cell):
    if pd.isna(cell) or cell == "":
        return ""
    if ":" in cell:
        sid, fid = [x.strip() for x in cell.split(":")]
        sub_name = subject_map.get(sid, sid)
        fac_name = faculty_map.get(fid, fid)
        return f"{sub_name} ({fac_name})"
    elif isinstance(cell, str) and cell in subject_map:
        return subject_map[cell]
    else:
        return cell

def replace_ids(df):
    return df.applymap(format_cell)

# Login
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if st.sidebar.button("Login"):
    user = users_df[(users_df['user_id'] == username) & (users_df['password'] == password)]
    if user.empty:
        st.sidebar.error("Invalid credentials")
    else:
        role = user.iloc[0]['role']
        faculty_id_logged = str(user.iloc[0].get('faculty_id', '')).strip()
        st.sidebar.success
