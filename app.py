import streamlit as st
import pandas as pd
import plotly.express as px
from utils import (
    load_data, authenticate_user, export_timetable_csv, export_timetable_excel,
    get_teacher_timetable_week, get_admin_timetable_semester
)
from scheduler import generate_timetable

st.set_page_config(page_title="BSc Data Analytics Timetable System", layout="wide")

# Load base data
faculty_df, subject_df, lab_df, class_df, _ = load_data()

# Initialize session state for login and timetable
if 'login' not in st.session_state:
    st.session_state.login = False

if 'timetable' not in st.session_state:
    st.session_state.timetable = pd.DataFrame()  # Empty initially

if not st.session_state.login:
    st.title("Login")
    user_id = st.text_input("User ID")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = authenticate_user(user_id, password)
        if user:
            st.session_state.login = True
            st.session_state.user = user
        else:
            st.error("Invalid credentials")
else:
    user = st.session_state.user
    st.sidebar.title(f"Welcome {user['user_id']} ({user['role']})")
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.experimental_rerun()

    if user['role'] == 'admin':
        st.title("Admin Dashboard - Semester Timetables")
        semester_selected = st.sidebar.selectbox("Select Semester (Class)", class_df['class_name'].unique())
        semester_id = class_df[class_df['class_name'] == semester_selected]['class_id'].values[0]

        if st.session_state.timetable.empty:
            st.info("No timetable generated yet. Please generate timetable.")
        else:
            timetable = get_admin_timetable_semester(st.session_state.timetable, semester_id)
            st.dataframe(timetable)

        if st.button("Generate Timetable"):
            generated_df = generate_timetable(faculty_df, subject_df, lab_df, class_df)
            st.session_state.timetable = generated_df
            st.success("Timetable generated successfully!")
            st.dataframe(generated_df)

        # Export buttons
        if not st.session_state.timetable.empty:
            if st.button("Export CSV"):
                export_timetable_csv(timetable, f"timetable_semester_{semester_id}.csv")
                st.success("CSV exported successfully")
            if st.button("Export Excel"):
                export_timetable_excel(timetable, f"timetable_semester_{semester_id}.xlsx")
                st.success("Excel exported successfully")

    elif user['role'] == 'teacher':
        st.title("Teacher Dashboard - Weekly Timetable")
        teacher_id = user['faculty_id']
        if st.session_state.timetable.empty:
            st.info("No timetable available. Contact admin.")
        else:
            timetable = get_teacher_timetable_week(st.session_state.timetable, teacher_id)
            if timetable.empty:
                st.info("No classes scheduled for this week.")
            else:
                days = timetable['Day'].unique()
                selected_day = st.selectbox("Select Day", days)
                filtered = timetable[timetable['Day'] == selected_day]
                fig = px.timeline(
                    filtered,
                    x_start="StartTime",
                    x_end="EndTime",
                    y="Day",
                    color="SubjectID",
                    hover_data=["ClassID", "Room"]
                )
                fig.update_yaxes(autorange="reversed")
                st.plotly_chart(fig, use_container_width=True)
                st.dataframe(filtered)

            # Export options
            if st.button("Export My Timetable CSV"):
                export_timetable_csv(timetable, f"teacher_timetable_{teacher_id}.csv")
                st.success("CSV exported successfully")
            if st.button("Export My Timetable Excel"):
                export_timetable_excel(timetable, f"teacher_timetable_{teacher_id}.xlsx")
                st.success("Excel exported successfully")

    else:
        st.error("Unauthorized role")
