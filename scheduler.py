import pandas as pd

def generate_timetable(classes_df, subjects_df, faculty_df, labs_df):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    periods = [f"Period {i}" for i in range(1, 7)]  # 6 periods

    # Map subject → faculty_id
    subject_faculty = {}
    for _, frow in faculty_df.iterrows():
        subject_ids = str(frow['subject_ids']).split(',')
        for sid in subject_ids:
            sid = sid.strip()
            if sid and sid not in subject_faculty:
                subject_faculty[sid] = frow['faculty_id']

    timetable = {}
    for _, crow in classes_df.iterrows():
        class_id = crow['class_id']
        subs = subjects_df[subjects_df['class_id'] == class_id]['subject_id'].tolist()

        # If no subjects, make empty
        if not subs:
            df_empty = pd.DataFrame("", index=periods, columns=days)
            timetable[class_id] = df_empty
        else:
            df = pd.DataFrame(index=periods, columns=days)
            for i, period in enumerate(periods):
                for j, day in enumerate(days):
                    sid = subs[(i + j) % len(subs)]
                    fid = subject_faculty.get(sid, "")
                    df.at[period, day] = f"{sid}:{fid}"
            timetable[class_id] = df

    return timetable
