import pandas as pd

def generate_timetable(faculty_df, subject_df, lab_df, class_df):
    """
    Timetable generation logic respecting constraints:
    - Teacher availability (mocked here with no clashes)
    - Max consecutive classes (e.g. 3 max)
    - No double booking, avoid clashes
    
    Returns a timetable DataFrame with columns:
    ['FacultyID', 'SubjectID', 'ClassID', 'Day', 'StartTime', 'EndTime', 'Room', 'Type']
    """

    # For demonstration, create a simple evenly distributed timetable mock data
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    time_slots = [('09:00', '10:00'), ('10:15', '11:15'), ('11:30', '12:30'), ('13:30', '14:30'), ('14:45', '15:45')]

    timetable_records = []
    faculty_ids = faculty_df['faculty_id'].tolist()
    subject_ids = subject_df['subject_id'].tolist()
    class_ids = class_df['class_id'].tolist()

    # Simple round-robin assignment avoiding consecutive >3 (mock example)
    max_consec = 3

    idx = 0
    for cls in class_ids:
        for day in days:
            consec_cnt = 0
            last_faculty = None
            for start, end in time_slots:
                if idx >= len(faculty_ids):
                    idx = 0
                faculty = faculty_ids[idx]

                # If last faculty same, increment consec count else reset
                if last_faculty == faculty:
                    if consec_cnt >= max_consec:
                        idx += 1
                        faculty = faculty_ids[idx % len(faculty_ids)]
                        consec_cnt = 1
                    else:
                        consec_cnt += 1
                else:
                    consec_cnt = 1

                last_faculty = faculty

                # Assign subject randomly (or linked via faculty-subject relation)
                subject = subject_ids[idx % len(subject_ids)]

                timetable_records.append({
                    'FacultyID': faculty,
                    'SubjectID': subject,
                    'ClassID': cls,
                    'Day': day,
                    'StartTime': pd.to_datetime(start).time(),
                    'EndTime': pd.to_datetime(end).time(),
                    'Room': f'Room {idx%5 + 1}',
                    'Type': 'theory'
                })

                idx += 1

    return pd.DataFrame(timetable_records)
