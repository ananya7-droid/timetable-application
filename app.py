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

        # Create mapping dictionaries for IDs to names
        subject_map = pd.Series(subjects_df['subject_name'].values, index=subjects_df['subject_id']).to_dict()
        faculty_map = pd.Series(faculty_df['faculty_name'].values, index=faculty_df['faculty_id']).to_dict()

        # Function to replace IDs with names in timetable cells
        def replace_ids_with_names(df):
            def replace_cell(cell):
                # Split by newline if multiple IDs per cell
                parts = str(cell).split('\n')
                replaced_parts = [subject_map.get(p, faculty_map.get(p, p)) for p in parts]
                return '\n'.join(replaced_parts)
            return df.applymap(replace_cell)
 
        # Replace IDs in all class timetables in the dictionary
        for class_id in timetable_df:
            timetable_df[class_id] = replace_ids_with_names(timetable_df[class_id])

        if role == "admin":
            st.subheader("📚 Class-wise Timetable")
            for c in classes_df['class_id']:
                st.markdown(f"### Class: `{c}`")
                st.table(get_class_timetable(timetable_df, c))

            st.subheader("👩‍🏫 Teacher-wise Timetable")
            for f in faculty_df['faculty_name']:
                st.markdown(f"### Faculty: `{f}`")
                teacher_tt = get_teacher_timetable(timetable_df, f)
                if isinstance(teacher_tt, dict):
                    for class_name, df in teacher_tt.items():
                        st.markdown(f"**Class: {class_name}**")
                        st.table(df)
                else:
                    st.table(teacher_tt)

            # Button to export timetable
            if st.button("📥 Download Timetable as Excel"):
                export_timetable(timetable_df, "outputs/timetable.xlsx")
                st.success("✅ Timetable exported to `outputs/timetable.xlsx`")
        
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
