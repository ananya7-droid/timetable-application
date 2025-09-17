import pandas as pd

def get_teacher_timetable(timetable_dict, faculty_id, free_periods=False):
    """
    Returns a dict: class_id -> timetable DataFrame (days as rows, periods as columns)
    """
    result = {}
    for class_id, df in timetable_dict.items():
        def has_fac(cell):
            if pd.isna(cell) or cell=="":
                return False
            if ":" in cell:
                parts = cell.split(":")
                if len(parts)>=2 and parts[1].strip() == faculty_id:
                    return True
            return False

        mask = df.applymap(has_fac)

        if free_periods:
            filtered = df.where(~mask)
        else:
            filtered = df.where(mask)

        filtered = filtered.dropna(how='all', axis=0).dropna(how='all', axis=1)

        if not filtered.empty:
            # Transpose so periods are columns, days are rows
            result[class_id] = filtered.T

    return result
