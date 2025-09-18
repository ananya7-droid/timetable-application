import pandas as pd

def generate_timetable(faculty_df, subject_df, lab_df, class_df, semester_id):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    time_slots = [
        ("12:25", "13:15"),
        ("13:15", "14:05"),
        ("14:05", "14:55"),
        ("15:10", "16:00"),
        ("16:00", "16:50"),
        ("16:50", "17:40"),
    ]
    total_periods = len(time_slots)
    period_num = list(range(1, total_periods + 1))

    # Build map of subject to faculty and subject type (lab/theory)
    # Using comprehensive subject list below to match utils.py
    subject_type_map = subject_df.set_index('subject_id')['type'].to_dict()

    # Faculty assigned round-robin to subjects just for demo purposes
    sub_fac_map = {}
    for i, row in subject_df.iterrows():
        faculty_index = i % len(faculty_df)
        faculty = faculty_df.iloc[faculty_index]['faculty_id']
        sub_fac_map[row['subject_id']] = {
            "faculty_id": faculty,
            "type": row['type']
        }

    timetable_records = []
    assignment_tracker = dict()  # (faculty, day, period) => True

    for subject_id, assign_info in sub_fac_map.items():
        faculty_id = assign_info['faculty_id']
        subject_type = assign_info['type']
        assigned = False

        for day in days:
            if assigned:
                break
            if subject_type == 'lab':
                for p in range(1, total_periods):
                    if (faculty_id, day, p) not in assignment_tracker and (faculty_id, day, p+1) not in assignment_tracker:
                        timetable_records.append({
                            "FacultyID": faculty_id,
                            "SubjectID": subject_id,
                            "ClassID": semester_id,
                            "Day": day,
                            "Period": p,
                            "StartTime": pd.to_datetime(time_slots[p-1][0]).time(),
                            "EndTime": pd.to_datetime(time_slots[p][1]).time(),
                            "Room": "Lab 1",
                            "Type": "lab"
                        })
                        assignment_tracker[(faculty_id, day, p)] = True
                        assignment_tracker[(faculty_id, day, p+1)] = True
                        assigned = True
                        break
            else:
                for p in period_num:
                    if (faculty_id, day, p) not in assignment_tracker:
                        timetable_records.append({
                            "FacultyID": faculty_id,
                            "SubjectID": subject_id,
                            "ClassID": semester_id,
                            "Day": day,
                            "Period": p,
                            "StartTime": pd.to_datetime(time_slots[p-1][0]).time(),
                            "EndTime": pd.to_datetime(time_slots[p-1][1]).time(),
                            "Room": "Room 1",
                            "Type": "theory"
                        })
                        assignment_tracker[(faculty_id, day, p)] = True
                        assigned = True
                        break

    return pd.DataFrame(timetable_records)
