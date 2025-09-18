import pandas as pd

def generate_timetable(classes_df, subjects_df, faculty_df, labs_df, teacher_constraints_df=None):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    periods = [f"Period {i}" for i in range(1, 7)]

    # Map subject_id → faculty_id from faculty_df
    subject_faculty = {}
    for _, frow in faculty_df.iterrows():
        subj_ids = str(frow['subject_ids']).split(',')
        for sid in subj_ids:
            sid = sid.strip()
            if sid:
                subject_faculty[sid] = frow['faculty_id']

    def faculty_available(fid, day, period):
        if teacher_constraints_df is None:
            return True
        rows = teacher_constraints_df[
            (teacher_constraints_df['faculty_id'] == fid) &
            (teacher_constraints_df['day'] == day) &
            (teacher_constraints_df['period'] == period)
        ]
        if not rows.empty:
            return bool(rows.iloc[0].get('available', True))
        return True

    timetable = {}
    for _, class_row in classes_df.iterrows():
        class_id = class_row['class_id']
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
                    fid = subject_faculty.get(sid, "")
                    if faculty_available(fid, day, period):
                        df.at[period, day] = f"{sid}:{fid}"
                    else:
                        df.at[period, day] = ""
        timetable[class_id] = df
    return timetable
