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

    # Build map: subject_id -> {"faculty_id":..., "type":...}
    subject_to_faculty = {}
    for i, row in subject_df.iterrows():
        faculty_index = i % len(faculty_df)  # round-robin faculty assign demo
        faculty_id = faculty_df.iloc[faculty_index]['faculty_id']
        subject_to_faculty[row['subject_id']] = {
            "faculty_id": faculty_id,
            "type": row['type']
        }

    timetable_records = []
    # Tracking booked slots: (day, period) for faculty
    booked_slots = {}

    # Prepare a list of all subjects ordered as [theory, then labs]
    theories = [subj for subj in subject_df['subject_id'] if subject_df[subject_df['subject_id'] == subj]['type'].values[0] == 'theory']
    labs = [subj for subj in subject_df['subject_id'] if subject_df[subject_df['subject_id'] == subj]['type'].values[0] == 'lab']

    day_index = 0
    period_index = 0

    # Assign theory subjects: 1 period each
    for subj in theories:
        faculty_id = subject_to_faculty[subj]['faculty_id']
        assigned = False

        # Try every day and period until find free slot
        for _ in range(len(days) * total_periods):
            day = days[day_index]
            period = period_nums[period_index]

            # Check if faculty free at that slot
            if not booked_slots.get((faculty_id, day, period), False):
                # Assign
                timetable_records.append({
                    "FacultyID": faculty_id,
                    "SubjectID": subj,
                    "ClassID": semester_id,
                    "Day": day,
                    "Period": period,
                    "StartTime": pd.to_datetime(time_slots[period-1][0]).time(),
                    "EndTime": pd.to_datetime(time_slots[period-1][1]).time(),
                    "Room": "Room 1",
                    "Type": "theory"
                })
                booked_slots[(faculty_id, day, period)] = True
                assigned = True
                # Move to next slot for next assignment
                period_index += 1
                if period_index >= total_periods:
                    period_index = 0
                    day_index = (day_index + 1) % len(days)
                break

            # Slot not free, move to next
            period_index += 1
            if period_index >= total_periods:
                period_index = 0
                day_index = (day_index + 1) % len(days)

        if not assigned:
            # No free slot found, could raise error or continue
            print(f"Warning: could not assign theory subject {subj}")

    # Now assign the labs requiring 2 consecutive periods
    day_index = 0
    period_index = 0

    for subj in labs:
        faculty_id = subject_to_faculty[subj]['faculty_id']
        assigned = False

        for _ in range(len(days) * (total_periods - 1)):
            day = days[day_index]
            period = period_nums[period_index]

            # Check if two consecutive periods free for faculty
            if period < total_periods:  # last period can't have 2 consecutive periods
                if (not booked_slots.get((faculty_id, day, period), False)
                        and not booked_slots.get((faculty_id, day, period + 1), False)):
                    # Assign lab in these two consecutive periods
                    timetable_records.append({
                        "FacultyID": faculty_id,
                        "SubjectID": subj,
                        "ClassID": semester_id,
                        "Day": day,
                        "Period": period,
                        "StartTime": pd.to_datetime(time_slots[period-1][0]).time(),
                        "EndTime": pd.to_datetime(time_slots[period][1]).time(),
                        "Room": "Lab 1",
                        "Type": "lab"
                    })
                    booked_slots[(faculty_id, day, period)] = True
                    booked_slots[(faculty_id, day, period + 1)] = True
                    assigned = True
                    # Move next slot forward by 2 periods to avoid overlap
                    period_index += 2
                    if period_index >= total_periods:
                        period_index = 0
                        day_index = (day_index + 1) % len(days)
                    break

            # Slot not free or no room for 2 consecutive, move next
            period_index += 1
            if period_index >= total_periods:
                period_index = 0
                day_index = (day_index + 1) % len(days)

        if not assigned:
            print(f"Warning: could not assign lab subject {subj}")

    return pd.DataFrame(timetable_records)
