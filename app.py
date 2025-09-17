import streamlit as st
import pandas as pd
from scheduler import generate_timetable
from utils import get_teacher_timetable, export_timetable

# Load CSVs
faculty_df = pd.read_csv("data/faculty.csv")
subjects_df = pd.read_csv("data/subjects.csv")
labs_df = pd.read_csv("data/labs.csv")
classes_df = pd.read_csv("data/classes.csv")
users_df = pd.read_csv("data/users.csv")

st.title("Timetable App")

# Maps for display
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

# --- Login ---
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if st.sidebar.button("Login"):
    user = users_df[(users_df['user_id']==username) & (users_df['password']==password)]
    if user.empty:
        st.sidebar.error("Invalid credentials")
    else:
        role = user.iloc[0]['role']
        faculty_id_logged = user.iloc[0].get('faculty_id', "")
        st.sidebar.success(f"Logged in as {role}")

        # Generate timetable
        timetable = generate_timetable(classes_df, subjects_df, faculty_df, labs_df)

        # Format timetable: periods = columns, days = rows
        for cls in list(timetable.keys()):
            df_raw = timetable[cls]
            df_fmt = replace_ids(df_raw)
            timetable[cls] = df_fmt.T

        # ---------------- Admin View ----------------
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
                if not tt:
                    st.write("No assigned periods")
                else:
                    # Loop through all classes for this teacher
                    for cname, df in tt.items():
                        st.markdown(f"**Class {cname}**")
                        st.table(df)

            if st.button("Export Timetable"):
                export_timetable(timetable, "outputs/timetable.xlsx")
                st.success("Exported timetable to outputs/timetable.xlsx")

        # ---------------- Teacher View ----------------
        elif role == "teacher":
            st.subheader("Your Timetable")
            tt = get_teacher_timetable(timetable, faculty_id_logged)
            if not tt:
                st.write("No assigned periods")
            else:
                for cname, df in tt.items():
                    st.markdown(f"**Class {cname}**")
                    st.table(df)

            st.subheader("Free Periods")
            free = get_teacher_timetable(timetable, faculty_id_logged, free_periods=True)
            if not free:
                st.write("No free periods")
            else:
                for cname, df in free.items():
                    st.markdown(f"**Class {cname}**")
                    st.table(df)

            if st.button("Export My Timetable"):
                export_timetable(tt, f"outputs/{username}_timetable.xlsx")
                st.success(f"Exported to outputs/{username}_timetable.xlsx")
