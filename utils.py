import pandas as pd

def get_class_timetable(timetable_dict, class_id):
    return timetable_dict.get(class_id, pd.DataFrame())

def get_teacher_timetable(timetable_dict, faculty_id, free_periods=False):
    results = {}
    for class_id, df in timetable_dict.items():
        def cell_has_faculty(cell):
            if pd.isna(cell) or cell == "":
                return False
            parts = cell.split('|')
            return len(parts) == 2 and parts[1] == faculty_id

        if free_periods:
            mask = df.applymap(lambda x: not cell_has_faculty(x))
        else:
            mask = df.applymap(cell_has_faculty)

        filtered_df = df.where(mask, other="")

        if filtered_df.replace("", pd.NA).dropna(how='all').shape[0] > 0:
            results[class_id] = filtered_df

    if not results:
        return pd.DataFrame()
    if len(results) == 1:
        return list(results.values())[0]
    return results

def export_timetable(timetable_dict, filepath):
    with pd.ExcelWriter(filepath) as writer:
        for class_id, df in timetable_dict.items():
            df.to_excel(writer, sheet_name=class_id)
