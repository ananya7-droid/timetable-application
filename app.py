import streamlit as st
import pandas as pd
import plotly.express as px
from utils import (
    load_data, authenticate_user, export_timetable_csv, export_timetable_excel,
    get_teacher_timetable_week, get_admin_timetable_semester, save_feedback
)
from scheduler import generate_timetable

st.set_page_config(page_title="BSc Data Analytics Timetable System", layout="wide")

# Load base data
faculty_df, subject_df, lab_df, class_df, timetable_df = load_data()

# Authentication
if 'login' not in st.session_state:
    st.session_state.login = False

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
    st.sidebar.button("Logout", on_click=lambda: st.session_state.clear())
    
    # Admin Section
    if user['role'] == 'admin':
        st.title("Admin Dashboard - Semester Timetables")
        semester_selected = st.sidebar.selectbox("Select Semester (Class)", class_df['class_name'].unique())
        semester_id = class_df[class_df['class_name'] == semester_selected]['class_id'].values[0]

        timetable = get_admin_timetable_semester(timetable_df, semester_id)
        st.dataframe(timetable.style.format({"StartTime":"{:%H:%M}","EndTime":"{:%H:%M}"}))

        # Export buttons
        if st.button("Export CSV"):
            export_timetable_csv(timetable, f"timetable_semester_{semester_id}.csv")
            st.success("CSV exported successfully")
        if st.button("Export Excel"):
            export_timetable_excel(timetable, f"timetable_semester_{semester_id}.xlsx")
            st.success("Excel exported successfully")

        # Feedback form
        st.header("Feedback and Issue Reporting")
        with st.form("feedback_form"):
            feedback_subject = st.text_input("Subject")
            feedback_message = st.text_area("Message")
            submitted = st.form_submit_button("Submit Feedback")
            if submitted:
                save_feedback(user['user_id'], feedback_subject, feedback_message)
                st.success("Feedback submitted. Thank you!")
                
    # Teacher Section
    elif user['role'] == 'teacher':
        st.title("Teacher Dashboard - Weekly Timetable")
        teacher_id = user['faculty_id']
        timetable = get_teacher_timetable_week(timetable_df, teacher_id)
        if timetable.empty:
            st.info("No classes scheduled for this week.")
        else:
            # Interactive filter by day
            days = timetable['Day'].unique()
            selected_day = st.selectbox("Select Day", days)
            filtered = timetable[timetable['Day'] == selected_day]
            fig = px.timeline(filtered, x_start="StartTime", x_end="EndTime", y="Day", color="SubjectName",
                              hover_data=["ClassName", "Room"])
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

        # Feedback form
        st.header("Feedback and Issue Reporting")
        with st.form("feedback_form"):
            feedback_subject = st.text_input("Subject")
            feedback_message = st.text_area("Message")
            submitted = st.form_submit_button("Submit Feedback")
            if submitted:
                save_feedback(user['user_id'], feedback_subject, feedback_message)
                st.success("Feedback submitted. Thank you!")

    # Dynamic forms for adding/updating data (optional based on role)
    st.sidebar.header("Data Management")
    if user['role'] == 'admin':
        with st.sidebar.expander("Add/Update Faculty"):
            # Example dynamic form for adding faculty could be implemented here
            pass
        with st.sidebar.expander("Add/Update Subject/Lab"):
            pass
        
        if st.sidebar.button("Generate Timetable"):
            generated_df = generate_timetable(faculty_df, subject_df, lab_df, class_df)
            # Update timetable.csv or show preview
            st.write("Timetable generated!")
            st.dataframe(generated_df)
    else:
        st.sidebar.info("You do not have permissions for data management.")
