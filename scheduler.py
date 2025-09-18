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
    period_nums = list(range(1, total_periods + 1))

    # Filter subjects and labs only for the semester
    semester_subjects = subject_df[subject_df['class_id'] == semester_id]
    semester_labs = lab_df[lab_df['class_id'] == semester_id]

    # Build faculty map with assigned subject and lab IDs
    faculty_map = faculty_df.set_index('faculty_id')[['subject_id', 'lab_id']].to_dict(orient='index')

    subjects_for_semester = []
    labs_for_semester = []

    # Map subjects for semester with faculty
    for subj_row in semester_subjects.itertuples():
        subj_id = str(subj_row.subject_id)
        for fac_id, assign in faculty_map.items():
            if subj_id in assign.get('subject_id', []):
                subjects_for_semester.append((subj_id, fac_id, subj_row.type))
                break

    # Map labs similarly
    for lab_row in semester_labs.itertuples():
        lab_id = str(lab_row.lab_id)
        for fac_id, assign in faculty_map.items():
            if lab_id in assign.get('lab_id', []):
                labs_for_semester.append((lab_id, fac_id, 'lab'))
                break

    timetable_records = []
    booked_slots = {}

    day_index = 0
    period_index = 0

    # Assign theory subjects - one period
    for subj_id, fac_id, typ in [s for s in subjects_for_semester if s[2] != 'lab']:
        assigned = False
        for _ in range(len(days) * total_periods):
            day = days[day_index]
            period = period_nums[period_index]

            if not booked_slots.get((fac_id, day, period), False):
                timetable_records.append({
                    "FacultyID": fac_id,
                    "SubjectID": subj_id,
                    "ClassID": semester_id,
                    "Day": day,
                    "Period": period,
                    "StartTime": pd.to_datetime(time_slots[period-1][0]).time(),
                    "EndTime": pd.to_datetime(time_slots[period-1][1]).time(),
                    "Room": "Room 1",
                    "Type": typ
                })
                booked_slots[(fac_id, day, period)] = True
                assigned = True
                period_index += 1
                if period_index >= total_periods:
                    period_index = 0
                    day_index = (day_index + 1) % len(days)
                break

            period_index += 1
            if period_index >= total_periods:
                period_index = 0
                day_index = (day_index + 1) % len(days)

        if not assigned:
            print(f"Warning: could not assign subject {subj_id}")

    # Assign labs - two consecutive periods
    day_index = 0
    period_index = 0

    for lab_id, fac_id, _typ in labs_for_semester:
        assigned = False
        for _ in range(len(days) * (total_periods - 1)):
            day = days[day_index]
            period = period_nums[period_index]

            if period < total_periods:
                if (not booked_slots.get((fac_id, day, period), False) and
                    not booked_slots.get((fac_id, day, period + 1), False)):
                    timetable_records.append({
                        "FacultyID": fac_id,
                        "SubjectID": lab_id,
                        "ClassID": semester_id,
                        "Day": day,
                        "Period": period,
                        "StartTime": pd.to_datetime(time_slots[period-1][0]).time(),
                        "EndTime": pd.to_datetime(time_slots[period][1]).time(),
                        "Room": "Lab 1",
                        "Type": "lab"
                    })
                    booked_slots[(fac_id, day, period)] = True
                    booked_slots[(fac_id, day, period + 1)] = True
                    assigned = True
                    period_index += 2
                    if period_index >= total_periods:
                        period_index = 0
                        day_index = (day_index + 1) % len(days)
                    break

            period_index += 1
            if period_index >= total_periods:
                period_index = 0
                day_index = (day_index + 1) % len(days)

        if not assigned:
            print(f"Warning: could not assign lab {lab_id}")

    return pd.DataFrame(timetable_records)
