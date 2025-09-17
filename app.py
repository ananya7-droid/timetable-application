import streamlit as st
import pandas as pd
from scheduler import generate_timetable
from utils import get_teacher_timetable, get_class_timetable, export_timetable

# Load CSVs
faculty_df = pd.read_csv("data/faculty.csv")
subjects_df = pd.read_csv("data/subjects.csv")
labs_df = pd.read_csv("data/labs.csv")
classes_df = pd.read_csv("data/classes.csv")
users_df = pd.read_csv("data/users.csv")

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

        timetable_df = generate_timetable(classes_df, subjects_df, faculty_df, labs_df)

        if role == "admin":
            st.subheader("📚 Class-wise Timetable")
            for c in classes_df['class_id']:
                st.markdown(f"### Class: `{c}`")
                st.table(get_class_timetable(timetable_df, c))

            st.subheader("👩‍🏫 Teacher-wise Timetable")
            for _, row in faculty_df.iterrows():
                faculty_id = row['faculty_id']
                faculty_name = row['faculty_name']
                st.markdown(f"### Faculty: {faculty_name} (ID: {faculty_id})")
                teacher_tt = get_teacher_timetable(timetable_df, faculty_id)
                if isinstance(teacher_tt, dict):
                    for class_name, df in teacher_tt.items():
                        st.markdown(f"**Class: {class_name}**")
                        st.table(df)
                else:
                    st.table(teacher_tt)

        elif role == "teacher":
            faculty_id = user.iloc[0]['faculty_id']
            st.subheader("📆 Your Timetable")
            teacher_tt = get_teacher_timetable(timetable_df, faculty_id)
            if isinstance(teacher_tt, dict):
                for class_name, df in teacher_tt.items():
                    st.markdown(f"**Class: {class_name}**")
                    st.table(df)
            else:
                st.table(teacher_tt)

            st.subheader("🕒 Free Periods Today")
            free_tt = get_teacher_timetable(timetable_df, faculty_id, free_periods=True)
            if isinstance(free_tt, dict):
                for class_name, df in free_tt.items():
                    st.markdown(f"**Class: {class_name}**")
                    st.table(df)
            else:
                st.table(free_tt)

    else:
        st.sidebar.error("❌ Invalid credentials")
