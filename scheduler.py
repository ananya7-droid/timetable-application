import pandas as pd

def generate_timetable(classes_df, subjects_df, faculty_df, labs_df):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    periods = [f"Period {i}" for i in range(1, 7)]

    # Build subject -> faculty mapping, strip spaces
    subject_faculty = {}
    for _, row in faculty_df.iterrows():
        subject_ids_str = str(row['subject_ids']).strip()
        if subject_ids_str and subject_ids_str.lower() != 'nan':
            for sid in subject_ids_str.split(','):
                sid = sid.strip()
                if sid:
                    subject_faculty[sid] = str(row['faculty_id']).strip()

    timetable = {}

    for _, row in classes_df.iterrows():
        class_id = row['class_id']
        subjects = subjects_df[subjects_df['class_id'] == class_id]['subject_id'].tolist()

        df = pd.DataFrame(index=periods, columns=days)

        if not subjects:
            for day in days:
                for period in periods:
                    df.at[period, day] = ""
        else:
            for i, period in enumerate(periods):
                for j, day in enumerate(days):
                    sid = subjects[(i + j) % len(subjects)]
                    fid = subject_faculty.get(sid, "")
                    df.at[period, day] = f"{sid}:{fid}"

        timetable[str(class_id)] = df

    return timetable
