import pandas as pd

def get_class_timetable(timetable_dict, class_id):
    return timetable_dict.get(class_id, pd.DataFrame())

def get_teacher_timetable(timetable_dict, faculty_id, free_periods=False, subject_map=None, subject_name_map=None):
    result = {}
    for class_id, df in timetable_dict.items():
        filtered_df = pd.DataFrame("", index=df.index, columns=df.columns)
        for day in df.index:
            for period in df.columns:
                cell = df.at[day, period]
                if pd.isna(cell) or cell == "":
                    if free_periods:
                        filtered_df.at[day, period] = "Free"
                elif isinstance(cell, str) and ":" in cell:
                    sid, fid = cell.split(":")
                    if fid == faculty_id:
                        name = subject_name_map.get(sid, sid) if subject_name_map else sid
                        filtered_df.at[day, period] = name
                    elif free_periods:
                        filtered_df.at[day, period] = "Free"
        if (filtered_df != "").any().any():
            result[class_id] = filtered_df
    if not result:
        return pd.DataFrame()
    if len(result) == 1:
        return next(iter(result.values()))
    return result

def export_timetable(timetable_dict, filename):
    with pd.ExcelWriter(filename, engine="xlsxwriter") as writer:
        for key, df in timetable_dict.items():
            df.to_excel(writer, sheet_name=str(key))
