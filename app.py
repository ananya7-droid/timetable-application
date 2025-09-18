import streamlit as st
import pandas as pd
import io
from scheduler import generate_timetable
from .utils import get_teacher_day_timetable

# Load default base CSVs (developer mode)
faculty_df = pd.read_csv("data/faculty.csv")
subjects_df = pd.read_csv("data/subjects.csv")
labs_df = pd.read_csv("data/labs.csv")
classes_df = pd.read_csv("data/classes.csv")
users_df = pd.read_csv("data/users.csv")

st.title("Timetable App")

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

uploaded_file = st.sidebar.file_uploader(
    "Upload classes/subjects (CSV) [Teacher mode]",
    type=["csv"]
)
teacher_uploaded_df = None
if uploaded_file is not None:
    teacher_uploaded_df = pd.read_csv(uploaded_file)
    st.sidebar.success("Teacher csv loaded!")

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
if st.sidebar.button("Login"):
    user = users_df[(users_df['user_id'] == username) & (users_df['password'] == password)]
    if user.empty:
        st.sidebar.error("Invalid credentials")
    else:
        role = user.iloc[0]['role']
        faculty_id_logged = user.iloc[0].get('faculty_id', "")

        # --- If teacher uploaded CSV, use ONLY that for timetable ---
        if role == "teacher" and teacher_uploaded_df is not None:
            # Generate timetable directly from uploaded teacher file
            st.success("Generating timetable from your uploaded file!")
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
            periods = [f"Period {i}" for i in range(1, 7)]

            subjects = teacher_uploaded_df['subject_name'].tolist()
            timetable_df = pd.DataFrame(index=periods, columns=days)
            for i, period in enumerate(periods):
                for j, day in enumerate(days):
                    subject = subjects[(i + j) % len(subjects)]
                    timetable_df.at[period, day] = subject

            st.subheader("Your Weekly Timetable")
            st.table(timetable_df)

            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                timetable_df.to_excel(writer, sheet_name="Timetable")
            output.seek(0)
            st.download_button(
                label="Download Timetable (Excel)",
                data=output,
                file_name="your_timetable.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        # --- Otherwise, fall back to developer dataset mode ---
        else:
            timetable = generate_timetable(classes_df, subjects_df, faculty_df, labs_df)
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
                    for day in timetable[classes_df['class_id'].iloc[0]].columns:
                        st.markdown(f"**Day: {day}**")
                        df = get_teacher_day_timetable(timetable, fid, day)
                        st.table(df)
                def get_timetable_excel_file(timetable_dict):
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                        for class_id, df in timetable_dict.items():
                            df.to_excel(writer, sheet_name=str(class_id))
                    output.seek(0)
                    return output

                excel_file = get_timetable_excel_file(timetable)
                st.download_button(
                    label="Download Timetable (Excel)",
                    data=excel_file,
                    file_name="timetable.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            elif role == "teacher":
                st.subheader("Your Daily Timetable (Developer Data)")
                selected_day = st.selectbox("Day", ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'])
                teacher_day_df = get_teacher_day_timetable(timetable, faculty_id_logged, selected_day)
                st.table(teacher_day_df)
