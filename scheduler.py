import pandas as pd
import random

def generate_timetable(classes_df, subjects_df, faculty_df, labs_df):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    periods = [f"Period {i}" for i in range(1,7)]

    # Map subject -> faculty
    subject_faculty = {}
    for _, row in faculty_df.iterrows():
        for sid in str(row['subject_ids']).split(','):
            sid = sid.strip()
            if sid:
                subject_faculty[sid] = row['faculty_id']

    timetable = {}
    faculty_schedule = {fid: {day:set() for day in days} for fid in faculty_df['faculty_id']}

    for _, class_row in classes_df.iterrows():
        class_id = class_row['class_id']
        class_name = class_row['class_name']
        df = pd.DataFrame(index=periods, columns=days)

        subs = subjects_df[subjects_df['class_id']==class_name]['subject_id'].tolist()
        labs = labs_df[labs_df['class_id']==class_name]['lab_id'].tolist()
        all_slots = subs + labs

        for day in days:
            for period in periods:
                random.shuffle(all_slots)
                assigned = False
                for slot in all_slots:
                    fid = subject_faculty.get(slot)
                    if fid:
                        if period not in faculty_schedule[fid][day]:
                            df.at[period, day] = f"{slot}:{fid}"
                            faculty_schedule[fid][day].add(period)
                            assigned = True
                            break
                    else:
                        df.at[period, day] = slot
                        assigned = True
                        break
                if not assigned:
                    df.at[period, day] = ""
        timetable[class_id] = df
    return timetable
