import streamlit as st
from utils import load_data, authenticate_user, export_timetable_excel
from scheduler import get_timetable

st.set_page_config(page_title="Simple Timetable Viewer", layout="wide")

faculty_df, subject_df, lab_df, class_df, users_df, timetable_df = load_data()

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

    st.title("Provided Timetable Viewer")

    if st.button("View Timetable"):
        timetable_df_display = get_timetable(timetable_df)
        st.session_state.timetable = timetable_df_display

    timetable_df_display = st.session_state.get("timetable", timetable_df)

    st.write("Timetable")
    st.dataframe(timetable_df_display)

    if st.button("Export Timetable Excel"):
        export_timetable_excel(timetable_df_display, "exported_timetable.xlsx")
        st.success("Exported timetable Excel successfully.")
