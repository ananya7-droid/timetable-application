import pandas as pd

def generate_timetable(classes_df, subjects_df, faculty_df, labs_df):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    periods = [f"Period {i}" for i in range(1, 7)]  # 6 periods

    timetable = {}

    for class_id in classes_df['class_id']:
        df = pd.DataFrame(index=periods, columns=days)

        # Subjects for this class
        class_subjects = subjects_df[subjects_df['class_id'] == class_id]['subject_id'].tolist()
        subj_count = len(class_subjects)

        # Map subject to faculty (first faculty teaching that subject)
        subject_faculty_map = {}
        for _, row in faculty_df.iterrows():
            for subj in row['subject_ids_list']:
                if subj not in subject_faculty_map:
                    subject_faculty_map[subj] = row['faculty_id']

        for i, period in enumerate(periods):
            for j, day in enumerate(days):
                subject_id = class_subjects[(i + j) % subj_count]
                faculty_id = subject_faculty_map.get(subject_id, "")
                df.at[period, day] = f"{subject_id}|{faculty_id}"

        timetable[class_id] = df

    return timetable
