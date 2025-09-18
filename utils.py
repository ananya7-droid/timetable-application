import pandas as pd

def get_class_timetable(timetable_dict, class_id):
    return timetable_dict.get(class_id, pd.DataFrame())

def get_teacher_timetable(timetable_dict, faculty_id, free_periods=False):
    result = {}
    for class_id, df in timetable_dict.items():
        # Define function to check if faculty_id is in the cell
        def has_fac(cell):
            if pd.isna(cell) or cell == "":
                return False
            if isinstance(cell, str) and ":" in cell:
                parts = cell.split(":")
                # parted[1] should be faculty_id
                if len(parts) >= 2 and parts[1].strip() == faculty_id:
                    return True
            return False

        mask = df.applymap(has_fac)

        if free_periods:
            filtered = df.where(~mask)
        else:
            filtered = df.where(mask)

        # Remove rows wholly empty and columns wholly empty
        filtered = filtered.dropna(how='all', axis=0).dropna(how='all', axis=1)

        if not filtered.empty:
            result[class_id] = filtered

    if not result:
        return pd.DataFrame()
    if len(result) == 1:
        return next(iter(result.values()))
    return result

def export_timetable(timetable_dict, filename):
    import pandas as pd
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        for class_id, df in timetable_dict.items():
            df.to_excel(writer, sheet_name=class_id)

