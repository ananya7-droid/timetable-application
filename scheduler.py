import pandas as pd

def generate_timetable(classes_df, subjects_df, faculty_df, labs_df):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    periods = [f"Period {i}" for i in range(1, 7)]

    # Map subject_id → faculty_id (from faculty_df subject_ids)
    subject_faculty = {}
    for _, frow in faculty_df.iterrows():
        subj_ids = str(frow['subject_ids']).split(',')
        for sid in subj_ids:
            sid = sid.strip()
            if sid:
                subject_faculty[sid] = frow['faculty_id']

    timetable = {}

    for _, class_row in classes_df.iterrows():
        class_id = class_row['class_id']  # keep as original type (int)
        subs = subjects_df[subjects_df['class_id'] == class_id]['subject_id'].tolist()
        
        df = pd.DataFrame(index=periods, columns=days)

        if not subs:
            # If no subjects, fill the timetable with empty strings
            for day in days:
                for period in periods:
                    df.at[period, day] = ""
        else:
            # Assign subjects to periods in a round-robin fashion
            for i, period in enumerate(periods):
                for j, day in enumerate(days):
                    sid = subs[(i + j) % len(subs)]
                    fid = subject_faculty.get(sid, "")
                    df.at[period, day] = f"{sid}:{fid}"

        timetable[str(class_id)] = df  # convert to string as dict key for consistency

    return timetable
