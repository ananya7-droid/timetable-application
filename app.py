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

        # Mapping dicts
        subject_map = pd.Series(subjects_df['subject_name'].values, index=subjects_df['subject_id']).to_dict()
        faculty_map = pd.Series(faculty_df['faculty_name'].values, index=faculty_df['faculty_id']).to_dict()

        # Function to format cell as "SubjectName (FacultyName)"
        def format_cell(value):
            if isinstance(value, str) and ':' in value:
                sub_id, fac_id = value.split(':')
                sub_name = subject_map.get(sub_id, sub_id)
                fac_name = faculty_map.get(fac_id, fac_id)
                return f"{sub_name} ({fac_name})"
            elif isinstance(value, str) and value in subject_map:
                # Sometimes just subject id without faculty id
                return subject_map.get(value, value)
            else:
                return value

        def replace_ids_with_names(df):
            return df.applymap(format_cell)

        # For all classes, convert IDs to names & transpose (days X-axis)
        for class_id in timetable_df:
            timetable_df[class_id] = replace_ids_with_names(timetable_df[class_id])
            timetable_df[class_id] = timetable_df[class_id].T

        if role == "admin":
            st.subheader("📚 Class-wise Timetable")
            for c in classes_df['class_id']:
                st.markdown(f"### Class: `{c}`")
                # Get class timetable from the processed timetable_df
                st.table(timetable_df[c])

            st.subheader("👩‍🏫 Teacher-wise Timetable")
            for f_id, f_name in faculty_map.items():
                st.markdown(f"### Faculty: `{f_name}`")
                teacher_tt = get_teacher_timetable(timetable_df, f_id)  # Pass faculty ID here!
                if isinstance(teacher_tt, dict):
                    for class_name, df in teacher_tt.items():
                        formatted_df = replace_ids_with_names(df).T
                        st.markdown(f"**Class: {class_name}**")
                        st.table(formatted_df)
                else:
                    formatted_df = replace_ids_with_names(teacher_tt).T
                    st.table(formatted_df)

            # Export button
            if st.button("📥 Download Timetable as Excel"):
                export_timetable(timetable_df, "outputs/timetable.xlsx")
                st.success("✅ Timetable exported to `outputs/timetable.xlsx`")

        elif role == "teacher":
            faculty_id = user.iloc[0]['faculty_id']
            st.subheader("📆 Your Timetable")
            teacher_tt = get_teacher_timetable(timetable_df, faculty_id)
            if isinstance(teacher_tt, dict):
                for class_name, df in teacher_tt.items():
                    formatted_df = replace_ids_with_names(df).T
                    st.markdown(f"**Class: {class_name}**")
                    st.table(formatted_df)
            else:
                formatted_df = replace_ids_with_names(teacher_tt).T
                st.table(formatted_df)

            st.subheader("🕒 Free Periods Today")
            free_tt = get_teacher_timetable(timetable_df, faculty_id, free_periods=True)
            if isinstance(free_tt, dict):
                for class_name, df in free_tt.items():
                    formatted_df = replace_ids_with_names(df).T
                    st.markdown(f"**Class: {class_name}**")
                    st.table(formatted_df)
            else:
                formatted_df = replace_ids_with_names(free_tt).T
                st.table(formatted_df)

    else:
        st.sidebar.error("❌ Invalid credentials")
