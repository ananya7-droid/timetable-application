import pandas as pd
import random

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]
SLOTS = ["9-10", "10-11", "11-12", "1-2", "2-3", "3-4"]

def generate_timetable(subjects_df, faculty_df, classes_df, days=DAYS, slots=SLOTS):
    schedule = []
    for _, class_row in classes_df.iterrows():
        class_id = class_row['class_id']
        subjects = subjects_df[subjects_df['year'] == class_row['year']]
        for _, subj in subjects.iterrows():
            day = random.choice(days)
            slot = random.choice(slots)
            schedule.append({
                "class_id": class_id,
                "year": class_row['year'],
                "day": day,
                "slot": slot,
                "subject": subj['subject_name'],
                "faculty": subj['faculty_id']
            })
    return pd.DataFrame(schedule)
