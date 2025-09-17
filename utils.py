import pandas as pd

def get_class_timetable(timetable_dict, class_id):
    """
    Return the timetable DataFrame for the given class_id.
    """
    return timetable_dict.get(class_id, pd.DataFrame())

def get_teacher_timetable(timetable_dict, faculty_id, free_periods=False):
    """
    Return timetable(s) where the faculty teaches.
    If free_periods=True, return free slots instead.
    Returns a dict of {class_id: DataFrame} or empty DataFrame if none found.
    """
    results = {}
    for class_id, df in timetable_dict.items():
        # Create boolean mask where faculty_id matches in any cell
        def cell_has_faculty(cell):
            if pd.isna(cell) or cell == "":
                return False
            # Cell format: "subject_id|faculty_id"
            parts = cell.split('|')
            if len(parts) == 2 and parts[1] == faculty_id:
                return True
            return False

        if free_periods:
            # Free if cell is NaN or empty or faculty_id not in cell
            mask = df.applymap(lambda x: not cell_has_faculty(x))
        else:
            mask = df.applymap(cell_has_faculty)

        filtered_df = df.where(mask, other="")  # Show only matching cells or empty

        if filtered_df.replace("", pd.NA).dropna(how='all').shape[0] > 0:
            results[class_id] = filtered_df

    if len(results) == 0:
        return pd.DataFrame()  # no timetable found
    if len(results) == 1:
        # Return single DataFrame instead of dict
        return list(results.values())[0]
    return results

def export_timetable(timetable_dict, filepath):
    """
    Export the timetable dictionary to Excel with each class as a sheet.
    """
    with pd.ExcelWriter(filepath) as writer:
        for class_id, df in timetable_dict.items():
            df.to_excel(writer, sheet_name=class_id)
