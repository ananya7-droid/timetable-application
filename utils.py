import pandas as pd

def get_teacher_timetable(timetable_dict, faculty_id, free_periods=False):
    faculty_id = str(faculty_id).strip()
    result = {}

    for class_id, df in timetable_dict.items():
        def has_fac(cell):
            if pd.isna(cell) or cell == "":
                return False
            if isinstance(cell, str) and ":" in cell:
                parts = cell.split(":", 1)
                if len(parts) == 2 and parts[1].strip() == faculty_id:
                    return True
            return False

        mask = df.applymap(has_fac)
        filtered = df.where(~mask if free_periods else mask)

        filtered = filtered.dropna(how='all', axis=0).dropna(how='all', axis=1)

        if not filtered.empty:
            result[class_id] = filtered

    if not result:
        return pd.DataFrame()
    if len(result) == 1:
        return next(iter(result.values()))
    return result
