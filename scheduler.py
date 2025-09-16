import pandas as pd
import random

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
PERIODS = [1,2,3,4,5,6]

def generate_timetable(classes_df, subjects_df, faculty_df, labs_df):
    """
    Returns a dict: {class_id: DataFrame of timetable}
    """
    timetable = {}  # {class_name: DataFrame}
    
    for idx, row in classes_df.iterrows():
        class_id = row['class_id']
        df = pd.DataFrame(index=PERIODS, columns=DAYS)
        subjects = subjects_df['subject_id'].tolist()
        random.shuffle(subjects)
        
        # Assign labs first (2 consecutive periods)
        labs = subjects_df[subjects_df['type'] == 'lab']['subject_id'].tolist()
        lab_idx = 0
        for day in DAYS:
            if lab_idx < len(labs):
                df.at[1, day] = labs[lab_idx]
                df.at[2, day] = labs[lab_idx]
                lab_idx += 1
        
        # Assign theory subjects avoiding same period on multiple days
        theory = subjects_df[subjects_df['type']=='theory']['subject_id'].tolist()
        for period in PERIODS:
            for day in DAYS:
                if pd.isna(df.at[period, day]):
                    if theory:
                        sub = theory.pop(0)
                        df.at[period, day] = sub
                        theory.append(sub)  # rotate subjects
        
        timetable[class_id] = df

    return timetable
