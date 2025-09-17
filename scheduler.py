import pandas as pd
import numpy as np

def generate_timetable(classes_df, subjects_df, faculty_df, labs_df):
    # Assuming days + periods set here
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    periods = [1, 2, 3, 4, 5, 6]

    timetable = {}

    # Create mapping for subjects and faculty names
    subject_map = pd.Series(subjects_df['subject_name'].values, index=subjects_df['subject_id']).to_dict()
    faculty_map = pd.Series(faculty_df['faculty_name'].values, index=faculty_df['faculty_id']).to_dict()
    lab_map = pd.Series(labs_df['lab_name'].values, index=labs_df['lab_id']).to_dict()

    for class_id in classes_df['class_id']:
        # Initialize empty timetable DataFrame
        df = pd.DataFrame(index=periods, columns=days)

        # For simplicity, assign subjects randomly or based on your logic here
        # This is dummy random assignment example; replace with your logic
        subjects_for_class = subjects_df[subjects_df['class_id'] == class_id]
        faculty_for_class = faculty_df  # you may filter based on subject assignments

        for day in days:
            for period in periods:
                # Pick a random subject from subjects_for_class
                sub_row = subjects_for_class.sample(1).iloc[0]
                sub_id = sub_row['subject_id']
                sub_name = subject_map.get(sub_id, sub_id)

                # Find a faculty teaching that subject
                fac_row = faculty_df[faculty_df['subject_ids'].str.contains(sub_id)]
                if not fac_row.empty:
                    fac_name = fac_row.iloc[0]['faculty_name']
                else:
                    fac_name = "TBD"

                # If subject is a lab, get lab name
                if sub_row['type'] == 'lab':
                    # Assuming labs_df matches subject_id to lab_id
                    lab_name = labs_df[labs_df['lab_id'] == sub_id]['lab_name'].values
                    lab_name = lab_name[0] if len(lab_name) > 0 else "Lab TBD"
                    df.at[period, day] = f"{sub_name} ({lab_name})\n{fac_name}"
                else:
                    df.at[period, day] = f"{sub_name}\n{fac_name}"

        timetable[class_id] = df

    return timetable
