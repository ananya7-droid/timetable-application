import pandas as pd

def get_class_timetable(timetable_dict, class_id):
    return timetable_dict.get(class_id, pd.DataFrame())

def get_teacher_timetable(timetable_dict, faculty_id, free_periods=False, subject_map=None):
    result = {}
    for class_id, df in timetable_dict.items():
        filtered_df = pd.DataFrame('', index=df.index, columns=df.columns)
        for day in df.index:
            for period in df.columns:
                cell = df.at[day, period]
                if pd.isna(cell) or cell == "":
                    if free_periods:
                        filtered_df.at[day, period] = "Free"
                elif isinstance(cell, str) and ":" in cell:
                    sid, fid = cell.split(":")
                    if fid == faculty_id:
                        sub_type = 'theory'
                        if subject_map:
                            sub_type = subject_map.get(sid, 'theory')
                        filtered_df.at[day, period] = "Lab" if sub_type == 'lab' else "Theory"
                    elif free_periods:
                        filtered_df.at[day, period] = "Free"
        # Only add DataFrame if there are non-empty cells
        if (filtered_df != "").any().any():
            result[class_id] = filtered_df
    if not result:
        return pd.DataFrame()
    if len(result) == 1:
        return next(iter(result.values()))
    return result

def export_timetable(timetable_dict, filename):
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        for class_id, df in timetable_dict.items():
            df.to_excel(writer, sheet_name=class_id)
