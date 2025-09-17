import pandas as pd

def generate_timetable(classes_df, subjects_df, faculty_df, labs_df):
    # Days and periods
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    periods = [f"Period {i}" for i in range(1, 7)]  # 6 periods

    # Map subject → faculty_id (pick first or whatever logic)
    # And also map subject_id → subject_name
    subject_faculty = {}
    for _, frow in faculty_df.iterrows():
        sids = str(frow['subject_ids']).split(',')
        for sid in sids:
            sid = sid.strip()
            # avoid overwriting if multiple faculty teach same subject, optional
            if sid not in subject_faculty:
                subject_faculty[sid] = frow['faculty_id']

    timetable = {}
    for _, crow in classes_df.iterrows():
        class_id = crow['class_id']
        # get subjects for this class
        subs = subjects_df[subjects_df['class_id'] == class_id]['subject_id'].tolist()
        if not subs:
            # handle case with no subjects
            df = pd.DataFrame("", index=periods, columns=days)
        else:
            df = pd.DataFrame(index=periods, columns=days)
            for i, period in enumerate(periods):
                for j, day in enumerate(days):
                    # cycle through subjects
                    sid = subs[(i + j) % len(subs)]
                    fid = subject_faculty.get(sid, "")
                    df.at[period, day] = f"{sid}:{fid}"
        timetable[class_id] = df

    return timetable
