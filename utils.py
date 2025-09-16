import pandas as pd

def get_teacher_timetable(timetable, faculty_id, free_periods=False):
    # Simplified: returns timetable for a faculty
    # In real case, map faculty_id to subjects assigned
    result = {}
    for class_name, df in timetable.items():
        result[class_name] = df
    if free_periods:
        # Return periods with no assigned subject (simplified)
        return {c: df.isna() for c, df in timetable.items()}
    return result

def get_class_timetable(timetable, class_name):
    return timetable[class_name]

def export_timetable(timetable, path):
    with pd.ExcelWriter(path) as writer:
        for class_name, df in timetable.items():
            df.to_excel(writer, sheet_name=class_name)
