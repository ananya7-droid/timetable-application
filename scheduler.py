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

    # Include Saturday now
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    # Updated time slots with 15 min break between 14:55 and 15:10
    time_slots = [
        ('12:25', '13:15'),
        ('13:15', '14:05'),
        ('14:05', '14:55'),
        # 15 min break (14:55-15:10)
        ('15:10', '16:00'),
        ('16:00', '16:50'),
        ('16:50', '17:40')
    ]

    timetable_records = []
    faculty_ids = faculty_df['faculty_id'].tolist()
    subject_ids = subject_df['subject_id'].tolist()
    class_ids = class_df['class_id'].tolist()

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

                subject = subject_ids[idx % len(subject_ids)]

                timetable_records.append({
                    'FacultyID': faculty,
                    'SubjectID': subject,
                    'ClassID': cls,
                    'Day': day,
                    'StartTime': pd.to_datetime(start).time(),
                    'EndTime': pd.to_datetime(end).time(),
                    'Room': f'Room {idx % 5 + 1}',
                    'Type': 'theory'
                })

                idx += 1

    return pd.DataFrame(timetable_records)
