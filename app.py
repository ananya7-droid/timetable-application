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

# Preprocess faculty_df to parse lists
def parse_list_column(df, col_name):
    return df[col_name].apply(lambda x: [i.strip() for i in x.split(',')] if pd.notna(x) else [])

faculty_df['subject_ids_list'] = parse_list_column(faculty_df, 'subject_ids')
faculty_df['lab_incharge_list'] = parse_list_column(faculty_df, 'lab_incharge')

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

        # Create mapping dictionaries
        subject_map = pd.Series(subjects_df['subject_name'].values, index=subjects_df['subject_id']).to_dict()
        faculty_map = pd.Series(faculty_df['faculty_name'].values, index=faculty_df['faculty_id']).to_dict()
        lab_map = pd.Series(labs_df['lab_name'].values, index=labs_df['lab_id']).to_dict()

        # Replace IDs with names in timetable DataFrame (assuming timetable_df is dict of class: DataFrame)
        def replace_ids_with_names(df):
            def convert_cell(cell):
                # cell expected format might be subject_id or faculty_id or lab_id or combined strings
                # You might want to adjust this depending on your timetable format
                if pd.isna(cell) or cell == "":
                    return ""
                # If cell contains multiple IDs separated by commas or spaces, split and convert each
                parts = [p.strip() for p in str(cell).split(',')]
                converted = []
                for p in parts:
                    if p in subject_map:
                        converted.append(subject_map[p])
                    elif p in faculty_map:
                        converted.append(faculty_map[p])
                    elif p in lab_map:
                        converted.append(lab_map[p])
                    else:
                        converted.append(p)
                return ", ".join(converted)
            return df.applymap(convert_cell)

        # Replace IDs in timetable_df
        for class_id in timetable_df:
            timetable_df[class_id] = replace_ids_with_names(timetable_df[class_id])

        if role == "admin":
            st.subheader("📚 Class-wise Timetable")
            for c in classes_df['class_id']:
                st.markdown(f"### Class: `{c}`")
                st.table(get_class_timetable(timetable_df, c))

            st.subheader("👩‍🏫 Teacher-wise Timetable")
            for idx, row in faculty_df.iterrows():
                faculty_name = row['faculty_name']
                st.markdown(f"### Faculty: {faculty_name}")
                teacher_tt = get_teacher_timetable(timetable_df, row['faculty_id'])
                if isinstance(teacher_tt, dict):
                    for class_name, df in teacher_tt.items():
                        st.markdown(f"**Class: {class_name}**")
                        st.table(df)
                else:
                    st.table(teacher_tt)

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

            # Show subjects taught by this faculty
            subjects_taught = []
            faculty_row = faculty_df[faculty_df['faculty_id'] == faculty_id]
            if not faculty_row.empty:
                subjects_taught = faculty_row.iloc[0]['subject_ids_list']
            subject_names = [subject_map.get(sid, sid) for sid in subjects_taught]
            st.subheader("📝 Subjects You Teach")
            st.write(", ".join(subject_names))

            # Show labs managed by this faculty
            labs_managed = []
            if not faculty_row.empty:
                labs_managed = faculty_row.iloc[0]['lab_incharge_list']
            lab_names = [lab_map.get(lab_id, lab_id) for lab_id in labs_managed]
            st.subheader("🧪 Labs You Manage")
            st.write(", ".join(lab_names))

    else:
        st.sidebar.error("❌ Invalid credentials")
