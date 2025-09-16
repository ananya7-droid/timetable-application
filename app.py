import streamlit as st
import pandas as pd
from scheduler import generate_timetable
from utils import get_teacher_timetable, get_class_timetable, export_timetable

# Load CSVs
faculty_df = pd.read_csv("data/faculty.csv")
subjects_df = pd.read_csv("data/subjects.csv")
labs_df = pd.read_csv("data/labs.csv")
classes_df = pd.read_csv("data/classes.csv")
users_df = pd.read_csv("data/users.csv")  # contains login info

st.title("Automated Timetable Generator")

# --- LOGIN ---
st.sidebar.title("Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
login_button = st.sidebar.button("Login")

if login_button:
    user = users_df[(users_df['user_id'] == username) & (users_df['password'] == password)]
    if not user.empty:
        role = user.iloc[0]['role']
        st.sidebar.success(f"Logged in as {role}")
        
        # Generate timetable once for the session
        timetable_df = generate_timetable(classes_df, subjects_df, faculty_df, labs_df)

        if role == "admin":
            st.subheader("Class-wise Timetable")
            for c in classes_df['class_name']:
                st.write(f"**{c}**")
                st.table(get_class_timetable(timetable_df, c))

            st.subheader("Teacher-wise Timetable")
            for f in faculty_df['faculty_name']:
                st.write(f"**{f}**")
                st.table(get_teacher_timetable(timetable_df, f))

            # Button to export timetable
            if st.button("Download Timetable as Excel"):
                export_timetable(timetable_df, "outputs/timetable.xlsx")
                st.success("Timetable exported to outputs/timetable.xlsx")
        
        elif role == "teacher":
            faculty_id = user.iloc[0]['faculty_id']
            st.subheader("Your Timetable")
            st.table(get_teacher_timetable(timetable_df, faculty_id))
            st.subheader("Free Periods Today")
            st.table(get_teacher_timetable(timetable_df, faculty_id, free_periods=True))
        
    else:
        st.sidebar.error("Invalid credentials")
