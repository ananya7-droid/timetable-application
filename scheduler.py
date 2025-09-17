import pandas as pd
import numpy as np

def generate_timetable(classes_df, subjects_df, faculty_df, labs_df):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    periods = [str(i) for i in range(1, 7)]  # x-axis

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

        # Allocate non-repeating period for each subject
        df = pd.DataFrame('', index=days, columns=periods)
        subs_cycle = np.array(subs).copy()
        np.random.shuffle(subs_cycle)
        for ip, period in enumerate(periods):
            for iday, day in enumerate(days):
                # Ensure no subject on same period in week
                sid = subs_cycle[(iday + ip) % len(subs_cycle)]
                fid = subject_faculty.get(sid, "")
                df.at[day, period] = f"{sid}:{fid}"
        
        # Assign labs in one or more available free slots
        for lab_id in labs:
            # Find a slot that doesn't already have a lab
            set_slot = False
            for period in periods:
                for day in days:
                    if df.at[day, period] == "" or 'Lab' in df.at[day, period]:
                        lab_name = subjects_df[subjects_df['subject_id'] == lab_id]['subject_name'].values[0]
                        fid = lab_faculty.get(lab_name, "")
                        df.at[day, period] = f"{lab_id}:{fid}"
                        set_slot = True
                        break
                if set_slot: break

        timetable[class_id] = df

    return timetable
