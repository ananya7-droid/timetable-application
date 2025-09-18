import pandas as pd

def generate_timetable(classes_df, subjects_df, faculty_df, labs_df):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    periods = [f'Period {i}' for i in range(1, 7)]

    # Map subject_id → faculty_id (strip and convert to strings)
    subject_faculty = {}
    for _, frow in faculty_df.iterrows():
        subj_str = str(frow['subject_ids']).strip()
        if subj_str and subj_str.lower() != 'nan':
            subj_ids = subj_str.split(',')
            for sid in subj_ids:
                sid = sid.strip()
                if sid:
                    subject_faculty[sid] = str(frow['faculty_id']).strip()

    timetable = {}

    for _, class_row in classes_df.iterrows():
        class_id = class_row['class_id']  # keep original (int)
        subs = subjects_df[subjects_df['class_id'] == class_id]['subject_id'].tolist()

        df = pd.DataFrame(index=periods, columns=days)
        if not subs:
            for day in days:
                for period in periods:
                    df.at[period, day] = ""
        else:
            for i, period in enumerate(periods):
                for j, day in enumerate(days):
                    sid = subs[(i + j) % len(subs)]
                    fid = subject_faculty.get(sid, "").strip()
                    df.at[period, day] = f"{sid}:{fid}"

        timetable[str(class_id)] = df  # convert to string as dict keys

    return timetable
