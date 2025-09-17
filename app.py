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

st.title("Timetable App")

# Maps
subject_map = pd.Series(subjects_df['subject_name'].values, index=subjects_df['subject_id']).to_dict()
subject_type_map = pd.Series(subjects_df['type'].values, index=subjects_df['subject_id']).to_dict()
faculty_map = pd.Series(faculty_df['faculty_name'].values, index=faculty_df['faculty_id']).to_dict()

def format_cell(cell):
    if pd.isna(cell) or cell == "":
        return ""
    if ":" in cell:
        sid, fid = cell.split(":")
        sid = sid.strip()
        fid = fid.strip()
        sub_name = subject_map.get(sid, sid)
        fac_name = faculty_map.get(fid, fid)
        return f"{sub_name} ({fac_name})"
    elif cell in subject_map:
        return subject_map[cell]
    else:
        return cell

def replace_ids(df):
    return df.applymap(format_cell)

# Login
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
if st.sidebar.button("Login"):
    user = users_df[(users_df['user_id'] == username) & (users_df['password'] == password)]
    if user.empty:
        st.sidebar.error("Invalid credentials")
    else:
        role = user.iloc[0]['role']
        faculty_id_logged = user.iloc[0].get('faculty_id', "")
        st.sidebar.success(f"Logged in as {role}")

        timetable = generate_timetable(classes_df, subjects_df, faculty_df, labs_df)

        timetable_fmt = {
            cls: replace_ids(df) for cls, df in timetable.items()
        }

        if role == "admin":
            st.subheader("Class Timetables")
            for cls in classes_df['class_id']:
                st.markdown(f"### Class: {cls}")
                st.table(timetable_fmt.get(cls, pd.DataFrame()))
            st.subheader("Teacher Timetables")
            for fid in faculty_df['faculty_id']:
                fname = faculty_map[fid]
                st.markdown(f"### {fname} (ID: {fid})")
                tt = get_teacher_timetable(timetable, fid, subject_map=subject_type_map)
                if isinstance(tt, dict):
                    for cname, df in tt.items():
                        st.markdown(f"**Class {cname}**")
                        st.table(df)
                else:
                    st.table(tt)
            st.subheader("Teacher Free Periods")
            for fid in faculty_df['faculty_id']:
                fname = faculty_map[fid]
                st.markdown(f"### {fname} (ID: {fid}) Free Periods")
                free_tt = get_teacher_timetable(timetable, fid, free_periods=True, subject_map=subject_type_map)
                if isinstance(free_tt, dict):
                    for cname, df in free_tt.items():
                        st.markdown(f"**Class {cname}**")
                        st.table(df)
                else:
                    st.table(free_tt)
            if st.button("Export All"):
                export_timetable(timetable_fmt, "outputs/timetable.xlsx")
                st.success("Exported timetable to outputs/timetable.xlsx.")

        elif role == "teacher":
            st.subheader("Your Timetable")
            tt = get_teacher_timetable(timetable, faculty_id_logged, subject_map=subject_type_map)
            if isinstance(tt, dict):
                for cname, df in tt.items():
                    st.markdown(f"**Class {cname}**")
                    st.table(df)
            else:
                st.table(tt)
            st.subheader("Free Periods")
            free_tt = get_teacher_timetable(timetable, faculty_id_logged, free_periods=True, subject_map=subject_type_map)
            if isinstance(free_tt, dict):
                for cname, df in free_tt.items():
                    st.markdown(f"**Class {cname}**")
                    st.table(df)
            else:
                st.table(free_tt)
            if st.button("Download Your Timetable"):
                fname = f"outputs/{faculty_id_logged}_timetable.xlsx"
                export_timetable({faculty_id_logged: tt}, fname)
                st.success(f"Exported timetable to {fname}.")
