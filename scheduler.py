import pandas as pd
import numpy as np

def generate_timetable(classes_df, subjects_df, faculty_df, labs_df):
    """
    Generate a dummy timetable dictionary.
    Each class timetable is a DataFrame with periods on Y axis and days on X axis.
    Each cell contains a string: "subject_id|faculty_id" or empty string.
    """

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    periods = [f"Period {i}" for i in range(1, 7)]  # 6 periods per day

    timetable = {}

    # For each class, generate a timetable DataFrame
    for class_id in classes_df['class_id']:
        df = pd.DataFrame(index=periods, columns=days)

        # For simplicity: assign subjects & faculty cyclically
        # Get subjects for this class
        class_subjects = subjects_df[subjects_df['class_id'] == class_id]['subject_id'].tolist()

        # Get faculty who teach these subjects
        faculty_subject_map = {}
        for _, row in faculty_df.iterrows():
            for subj in row['subject_ids_list']:
                faculty_subject_map[subj] = row['faculty_id']

        subj_count = len(class_subjects)
        for i, period in enumerate(periods):
            for j, day in enumerate(days):
                # Pick subject cyclically
                subject_id = class_subjects[(i + j) % subj_count]
                faculty_id = faculty_subject_map.get(subject_id, "")
                # Format cell as subject|faculty
                df.at[period, day] = f"{subject_id}|{faculty_id}"

        timetable[class_id] = df

    return timetable
