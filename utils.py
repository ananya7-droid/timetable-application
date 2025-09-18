import pandas as pd

def get_class_timetable(timetable_dict, class_id):
    return timetable_dict.get(str(class_id), pd.DataFrame())

def get_teacher_timetable(timetable_dict, faculty_id, free_periods=False):
    faculty_id = str(faculty_id).strip()
    result = {}

    for class_id, df in timetable_dict.items():
        def has_fac(cell):
            if pd.isna(cell) or cell == "":
                return False
            if isinstance(cell, str) and ":" in cell:
                parts = cell.split(":")
                if len(parts) >= 2:
                    fac_part = parts[1].strip()
                    if fac_part == faculty_id:
                        return True
            return False

        mask = df.applymap(has_fac)
        if free_periods:
            filtered = df.where(~mask)
        else:
            filtered = df.where(mask)
        
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
