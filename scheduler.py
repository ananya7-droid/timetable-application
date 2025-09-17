import pandas as pd
import numpy as np

def generate_timetable(classes_df, subjects_df, faculty_df, labs_df):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    periods = [str(i) for i in range(1, 7)]  # 1 to 6 (x-axis)

    # Map subject to faculty
    subject_faculty = {}
    for _, frow in faculty_df.iterrows():
        for sid in str(frow["subject_ids"]).split(","):
            if sid.strip():
                subject_faculty[sid.strip()] = frow["faculty_id"]

    # Map lab to faculty
    lab_faculty = {}
    for _, frow in faculty_df.iterrows():
        for lab_name in str(frow["lab_incharge"]).split(","):
            if lab_name.strip():
                lab_faculty[lab_name.strip()] = frow["faculty_id"]

    timetable = {}

    for _, class_row in classes_df.iterrows():
        class_id = class_row["class_id"]
        subs = subjects_df[(subjects_df["class_id"] == class_id) & (subjects_df["type"] == "theory")]["subject_id"].tolist()
        labs = subjects_df[(subjects_df["class_id"] == class_id) & (subjects_df["type"] == "lab")]["subject_id"].tolist()

        df = pd.DataFrame("", index=days, columns=periods)

        # Assign theory ensuring no subject repeats in same period slot across days
        subs_cycle = np.array(subs).copy()
        np.random.shuffle(subs_cycle)
        for i_p, period in enumerate(periods):
            for i_d, day in enumerate(days):
                sid = subs_cycle[(i_d + i_p) % len(subs_cycle)]
                fid = subject_faculty.get(sid, "")
                df.at[day, period] = f"{sid}:{fid}"

        # Assign labs to unoccupied slots
        for lab_id in labs:
            assigned = False
            for day in days:
                for period in periods:
                    if df.at[day, period] == "":
                        fid = lab_faculty.get(lab_id, "")
                        df.at[day, period] = f"{lab_id}:{fid}"
                        assigned = True
                        break
                if assigned:
                    break

        timetable[class_id] = df

    return timetable
