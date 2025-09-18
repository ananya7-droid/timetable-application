import streamlit as st
import pandas as pd
from utils import load_data, authenticate_user, export_timetable_excel, get_subject_name
from scheduler import generate_timetable

st.set_page_config(page_title="3rd BSc Data Analytics Timetable", layout="wide")

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

    st.title("Timetable Generator for 3rd BSc Data Analytics 5th Semester")

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
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        period_times = [
            ("1", "12:25 - 13:15"),
            ("2", "13:15 - 14:05"),
            ("3", "14:05 - 14:55"),
            ("Break", "14:55 - 15:10"),
            ("4", "15:10 - 16:00"),
            ("5", "16:00 - 16:50"),
            ("6", "16:50 - 17:40"),
        ]

        columns = [f"{num}\n{time}" for num, time in period_times if num != "Break"]
        grid_df = pd.DataFrame(index=days, columns=columns)

        for day in days:
            day_data = timetable_df[timetable_df["Day"] == day]
            for period_num, _ in period_times:
                if period_num == "Break":
                    continue
                period = int(period_num)
                slot_data = day_data[day_data["Period"] == period]
                if not slot_data.empty:
                    subj_names = []
                    for _, row in slot_data.iterrows():
                        subj_names.append(
                            get_subject_name(subject_df, row["SubjectID"]) +
                            (" (Lab)" if row["Type"] == "lab" else "")
                        )
                    grid_df.at[day, f"{period_num}\n{period_times[period - 1][1]}"] = ", ".join(subj_names)
                else:
                    grid_df.at[day, f"{period_num}\n{period_times[period - 1][1]}"] = ""

        st.subheader(f"Timetable for {semester_name}")
        st.table(grid_df)

        if st.button("Export Timetable Excel"):
            export_timetable_excel(timetable_df, f"timetable_{semester_name.replace(' ', '_')}.xlsx")
            st.success("Exported timetable Excel successfully.")
