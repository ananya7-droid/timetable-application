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
    reduced_subjects = set([105,106,206,207,208,306,307])  # subjects with 2 periods/week

    # Filter subjects and labs for semester
    semester_subjects = subject_df[subject_df['class_id'] == semester_id]
    semester_labs = lab_df[lab_df['class_id'] == semester_id]

    faculty_map = faculty_df.set_index('faculty_id')[['subject_id', 'lab_id']].to_dict(orient='index')

    subjects_for_semester = []
    labs_for_semester = []

    for subj_row in semester_subjects.itertuples():
        subj_id = str(subj_row.subject_id)
        for fac_id, assign in faculty_map.items():
            if subj_id in assign.get('subject_id', []):
                subjects_for_semester.append((subj_id, fac_id, subj_row.type))
                break

    for lab_row in semester_labs.itertuples():
        lab_id = str(lab_row.lab_id)
        for fac_id, assign in faculty_map.items():
            if lab_id in assign.get('lab_id', []):
                labs_for_semester.append((lab_id, fac_id, 'lab'))
                break

    timetable_records = []
    booked_slots = {}

    slots = [(d, p) for d in days for p in period_nums]
    slot_index = 0

    # Assign labs (1 per week, 2 periods)
    for lab_id, fac_id, _ in labs_for_semester:
        assigned = False
        for d in days:
            for p in range(1, total_periods):
                if (fac_id, d, p) not in booked_slots and (fac_id, d, p+1) not in booked_slots:
                    timetable_records.append({
                        "FacultyID": fac_id,
                        "SubjectID": lab_id,
                        "ClassID": semester_id,
                        "Day": d,
                        "Period": p,
                        "StartTime": pd.to_datetime(time_slots[p-1][0]).time(),
                        "EndTime": pd.to_datetime(time_slots[p][1]).time(),
                        "Room": "Lab 1",
                        "Type": "lab"
                    })
                    booked_slots[(fac_id, d, p)] = True
                    booked_slots[(fac_id, d, p+1)] = True
                    assigned = True
                    break
            if assigned:
                break
        if not assigned:
            print(f"Could not assign lab {lab_id}")

    # Theory subjects: 4/week normally, 2/week for a subset
    subject_instances = []
    for subj_id, fac_id, typ in [s for s in subjects_for_semester if s[2] != 'lab']:
        subj_id_int = int(subj_id) if subj_id.isdigit() else -1
        n_periods = 2 if subj_id_int in reduced_subjects else 4
        for _ in range(n_periods):
            subject_instances.append((subj_id, fac_id, typ))

    # Assign theory subjects into available slots
    for subj_id, fac_id, typ in subject_instances:
        while slot_index < len(slots):
            d, p = slots[slot_index]
            slot_index += 1
            if (fac_id, d, p) not in booked_slots:
                timetable_records.append({
                    "FacultyID": fac_id,
                    "SubjectID": subj_id,
                    "ClassID": semester_id,
                    "Day": d,
                    "Period": p,
                    "StartTime": pd.to_datetime(time_slots[p-1][0]).time(),
                    "EndTime": pd.to_datetime(time_slots[p-1][1]).time(),
                    "Room": "Room 1",
                    "Type": typ
                })
                booked_slots[(fac_id, d, p)] = True
                break

    return pd.DataFrame(timetable_records)
