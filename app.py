import streamlit as st
import pandas as pd
from scheduler import generate_timetable
from utils import get_teacher_timetable, get_class_timetable, export_timetable

# Load data
faculty_df = pd.read_csv("data/faculty.csv")
subjects_df = pd.read_csv("data/subjects.csv")
labs_df = pd.read_csv("data/labs.csv")
classes_df = pd.read_csv("data/classes.csv")
users_df = pd.read_csv("data/users.csv")

st.title("Automated Timetable Generator")

# Create maps
subject_map = pd.Series(subjects_df['subject_name'].values, index=subjects_df['subject_id']).to_dict()
faculty_map = pd.Series(faculty_df['faculty_name'].values, index=faculty_df['faculty_id']).to_dict()
# If labs needed: lab_name map
lab_map = {}
if 'lab_id' in labs_df.columns and 'lab_name' in labs_df.columns:
    lab_map = pd.Series(labs_df['lab_name'].values, index=labs_df['lab_id']).to_dict()

# Formatting function
def format_cell(cell_value):
    if pd.isna(cell_value) or cell_value == "":
        return ""
    if isinstance(cell_value, str) and ":" in cell_value:
        sub_id, fac_id = cell_value.split(":")
        sub_id = sub_id.strip()
        fac_id = fac_id.strip()
        sub_name = subject_map.get(sub_id, sub_id)
        fac_name = faculty_map.get(fac_id, fac_id)
        return f"{sub_name} ({fac_name})"
    elif isinstance(cell_value, str) and cell_value in subject_map:
        return subject_map[cell_value]
    else:
        return cell_value

def replace_ids_with_names(df):
    return df.applymap(format_cell)

# Sidebar login
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
login = st.sidebar.button("Login")

if login:
    user = users_df[(users_df['user_id'] == username) & (users_df['password'] == password)]
    if user.empty:
        st.sidebar.error("Invalid credentials")
    else:
        role = user.iloc[0]['role']
        faculty_id_logged = user.iloc[0].get('faculty_id', None)
        st.sidebar.success(f"Logged in as " + role)

        # Generate
        timetable = generate_timetable(classes_df, subjects_df, faculty_df, labs_df)

        # Convert all class timetables
        for cls in timetable:
            df = timetable[cls]
            df2 = replace_ids_with_names(df)
            timetable[cls] = df2.T  # transpose so days are columns

        if role == "admin":
            st.subheader("Class-wise Timetables")
            for cls in classes_df['class_id']:
                st.markdown(f"### Class {cls}")
                st.table(timetable.get(cls, pd.DataFrame()))

            st.subheader("Teacher-wise Timetables")
            for _, frow in faculty_df.iterrows():
                fid = frow['faculty_id']
                fname = frow['faculty_name']
                st.markdown(f"### {fname}")
                teacher_tt = get_teacher_timetable(timetable, fid)
                if isinstance(teacher_tt, dict):
                    for cls_name, df in teacher_tt.items():
                        st.markdown(f"**Class {cls_name}**")
                        st.table(df)
                else:
                    st.table(teacher_tt)

            if st.button("Export Timetable to Excel"):
                export_timetable(timetable, "outputs/timetable.xlsx")
                st.success("Exported timetable.xlsx")

        elif role == "teacher":
            st.subheader("Your Timetable")
            teacher_tt = get_teacher_timetable(timetable, faculty_id_logged)
            if isinstance(teacher_tt, dict):
                for cls_name, df in teacher_tt.items():
                    st.markdown(f"**Class {cls_name}**")
                    st.table(df)
            else:
                st.table(teacher_tt)

            st.subheader("Free Periods Today")
            free_tt = get_teacher_timetable(timetable, faculty_id_logged, free_periods=True)
            if isinstance(free_tt, dict):
                for cls_name, df in free_tt.items():
                    st.markdown(f"**Class {cls_name}**")
                    st.table(df)
            else:
                st.table(free_tt)
