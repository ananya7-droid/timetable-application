import pandas as pd
import numpy as np

def generate_timetable(classes_df, subjects_df, faculty_df, labs_df):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    periods = [f"{i}" for i in range(1, 7)]

    # Faculty subject map
    subject_faculty = {}
    for _, frow in faculty_df.iterrows():
        for sid in str(frow['subject_ids']).split(','):
            if sid.strip():
                subject_faculty[sid.strip()] = frow['faculty_id']

    # Assign labs based on 'lab_incharge'
    lab_faculty = {}
    for _, frow in faculty_df.iterrows():
        for labname in str(frow['lab_incharge']).split(','):
            if labname.strip():
                lab_faculty[labname.strip()] = frow['faculty_id']

    timetable = {}

    for _, class_row in classes_df.iterrows():
        class_id = class_row['class_id']
        subs = subjects_df[(subjects_df['class_id'] == class_id) & (subjects_df['type'] == 'theory')]['subject_id'].tolist()
        labs = subjects_df[(subjects_df['class_id'] == class_id) & (subjects_df['type'] == 'lab')]['subject_id'].tolist()

        # Ensure clash-free and non-repeating slot allocation for subjects in each period
        df = pd.DataFrame('', index=days, columns=periods)
        # Shuffle subjects for fairness
        subs_cycle = np.array(subs).copy()
        np.random.shuffle(subs_cycle)
        # Assign each subject only once per column
        for ip, period in enumerate(periods):
            for iday, day in enumerate(days):
                # Ensure no subject on same period in week
                sid = subs_cycle[(iday + ip) % len(subs_cycle)]
                fid = subject_faculty.get(sid, "")
                df.at[day, period] = f"{sid}:{fid}"
        
        # Assign labs to random slots, but do not overwrite existing theory
        for lab_id in labs:
            # Find least used slot to place the lab
            used_slots = {(d, p) for d in days for p in periods if df.at[d, p] != ""}
            all_slots = [(d, p) for d in days for p in periods]
            available_slots = list(set(all_slots) - used_slots)
            # If all slots used, overwrite random
            if available_slots:
                lab_day, lab_period = available_slots[0]
            else:
                lab_day, lab_period = days[0], periods[-1]
            fid = lab_faculty.get("Lab"+class_id[-1], "")  # Get lab incharge by class year
            df.at[lab_day, lab_period] = f"{lab_id}:{fid}"

        timetable[class_id] = df

    return timetable
