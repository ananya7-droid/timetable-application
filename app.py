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
    elif isinstance(cell, str) and cell in subject_map:
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

        # Debug: display first class raw
        # st.write("Raw timetable sample:", timetable.get(classes_df['class_id'].iloc[0]).head())

        # Format & transpose
        for cls in list(timetable.keys()):
            df_raw = timetable[cls]
            df_fmt = replace_ids(df_raw)
            timetable[cls] = df_fmt.T

        if role == "admin":
            st.subheader("Class Timetables")
            for cls in classes_df['class_id']:
                st.markdown(f"### Class: {cls}")
                st.table(timetable.get(cls, pd.DataFrame()))

            st.subheader("Teacher Timetables")
            for _, row in faculty_df.iterrows():
                fid = row['faculty_id']
                fname = row['faculty_name']
                st.markdown(f"### {fname} (ID: {fid})")
                tt = get_teacher_timetable(timetable, fid)
                if isinstance(tt, dict):
                    for cname, df in tt.items():
                        st.markdown(f"**Class {cname}**")
                        st.table(df)
                else:
                    st.table(tt)

            if st.button("Export"):
                export_timetable(timetable, "outputs/timetable.xlsx")
                st.success("Exported.")

        elif role == "teacher":
            st.subheader("Your Timetable")
            tt = get_teacher_timetable(timetable, faculty_id_logged)
            if isinstance(tt, dict):
                for cname, df in tt.items():
                    st.markdown(f"**Class {cname}**")
                    st.table(df)
            else:
                st.table(tt)

            st.subheader("Free Periods")
            free = get_teacher_timetable(timetable, faculty_id_logged, free_periods=True)
            if isinstance(free, dict):
                for cname, df in free.items():
                    st.markdown(f"**Class {cname}**")
                    st.table(df)
                else:
                    st.table(free)
