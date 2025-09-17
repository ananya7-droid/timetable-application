import pandas as pd
import random

def generate_timetable(classes_df, subjects_df, faculty_df, labs_df):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    periods = [f"Period {i}" for i in range(1, 7)]

    # Map subject -> faculty
    subject_faculty = {}
    for _, row in faculty_df.iterrows():
        for sid in str(row['subject_ids']).split(','):
            sid = sid.strip()
            if sid:
                subject_faculty[sid] = row['faculty_id']

    timetable = {}
    for _, class_row in classes_df.iterrows():
        class_id = class_row['class_id']
        class_name = class_row['class_name']

        # Theory subjects for this class
        subs = subjects_df[(subjects_df['class_id'] == class_name) & (subjects_df['type']=='theory')]['subject_id'].tolist()
        labs = labs_df[labs_df['class_id']==class_name]['lab_id'].tolist()
        all_slots = subs + labs

        df = pd.DataFrame(index=periods, columns=days)

        used_subjects = {day: set() for day in days}

        for period in periods:
            for day in days:
                # pick a subject/lab not already in this period on other days
                available = [s for s in all_slots if s not in used_subjects[day]]
                if not available:
                    cell = ""
                else:
                    cell = random.choice(available)
                    used_subjects[day].add(cell)
                fid = subject_faculty.get(cell, "")
                df.at[period, day] = f"{cell}:{fid}" if fid else cell

        timetable[class_id] = df

    return timetable
