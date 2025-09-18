import streamlit as st
import pandas as pd
from utils import load_data, authenticate_user, export_timetable_excel, get_subject_name
from scheduler import generate_timetable

st.set_page_config(page_title="Simple Timetable Generator", layout="wide")

faculty_df, subject_df, lab_df, class_df, users_df = load_data()

if "login" not in st.session_state:
    st.session_state.login = False

def logout():
    st.session_state.clear()
    st.experimental_rerun()

if not st.session_state.login:
    st.title("Admin Login")
    user_id = st.text_input("User ID")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = authenticate_user(user_id, password, users_df)
        if user and user["role"] == "admin":
            st.session_state.login = True
            st.session_state.user = user
        else:
            st.error("Invalid credentials.")
else:
    st.sidebar.title("Welcome Admin")
    if st.sidebar.button("Logout"):
        logout()

    st.title("Timetable Generator")

    semester_id = 1
    semester_name = class_df[class_df["class_id"] == semester_id]["class_name"].values[0]

    if st.button(f"Generate Timetable for {semester_name}"):
        timetable_df = generate_timetable(faculty_df, subject_df, lab_df, class_df, semester_id)
        st.session_state.timetable = timetable_df
        st.success(f"Timetable generated for {semester_name}!")

    timetable_df = st.session_state.get("timetable", pd.DataFrame())

    if timetable_df.empty:
        st.info("No timetable generated yet.")
    else:
        st.dataframe(timetable_df)

        if st.button("Export Timetable Excel"):
            export_timetable_excel(timetable_df, f"timetable_{semester_name.replace(' ', '_')}.xlsx")
            st.success("Exported timetable Excel successfully.")
