import streamlit as st
import pandas as pd
from scheduler import generate_timetable
from utils import get_teacher_timetable, export_timetable

# Load CSV files
faculty_df = pd.read_csv("data/faculty.csv")
subjects_df = pd.read_csv("data/subjects.csv")
labs_df = pd.read_csv("data/labs.csv")
classes_df = pd.read_csv("data/classes.csv")
users_df = pd.read_csv("data/users.csv")

st.title("Timetable App")

# Mapping for names
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

# Login sidebar
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if st.sidebar.button("Login"):
    user = users_df[(users_df['user_id'] == username) & (users_df['password'] == password)]
    if user.empty:
        st.sidebar.error("Invalid credentials")
    else:
        role = user.iloc[0]['role']
        faculty_id_logged = str(user.iloc[0].get('faculty_id', "")).strip()
        st.sidebar.success(f"Logged in as {role}")

        timetable = generate_timetable(classes_df, subjects_df, faculty_df, labs_df)

        # Format and transpose timetable for display
        for cls in list(timetable.keys()):
            df_raw = timetable[cls]
            df_fmt = replace_ids(df_raw)
            timetable[cls] = df_fmt.T

        if role == "admin":
            st.subheader("Class Timetables")
            for cls in classes_df['class_id']:
                st.markdown(f"### Class: {cls}")
                st.table(timetable.get(str(cls), pd.DataFrame()))

            st.subheader("Teacher Timetables")
            for _, row in faculty_df.iterrows():
                fid = str(row['faculty_id']).strip()
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
            st.subheader("Your Weekly Timetable Across Classes")
            tt = get_teacher_timetable(timetable, faculty_id_logged)
            free = get_teacher_timetable(timetable, faculty_id_logged, free_periods=True)

            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
            periods = [f"Period {i}" for i in range(1, 7)]
            combined_df = pd.DataFrame("", index=periods, columns=days)

            if isinstance(tt, dict):
                for class_id, df in tt.items():
                    for day in days:
                        for period in periods:
                            if day in df.columns and period in df.index:
                                cell = df.at[period, day]
                                if cell and pd.notna(cell) and cell != "":
                                    combined_df.at[period, day] += f"{class_id}: {cell}\n"
            else:
                df = tt
                for day in days:
                    for period in periods:
                        if day in df.columns and period in df.index:
                            cell = df.at[period, day]
                            if cell and pd.notna(cell) and cell != "":
                                combined_df.at[period, day] = cell

            if isinstance(free, dict):
                for class_id, df in free.items():
                    for day in days:
                        for period in periods:
                            if day in df.columns and period in df.index:
                                cell = df.at[period, day]
                                if cell == "" or pd.isna(cell):
                                    if combined_df.at[period, day] == "":
                                        combined_df.at[period, day] = "Free"
            else:
                df = free
                for day in days:
                    for period in periods:
                        if day in df.columns and period in df.index:
                            cell = df.at[period, day]
                            if cell == "" or pd.isna(cell):
                                if combined_df.at[period, day] == "":
                                    combined_df.at[period, day] = "Free"

            st.table(combined_df)
