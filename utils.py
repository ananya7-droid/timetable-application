import pandas as pd

def get_teacher_timetable(timetable_dict, faculty_id, free_periods=False):
    result = {}
    for class_id, df in timetable_dict.items():
        def has_fac(cell):
            if pd.isna(cell) or cell=="":
                return False
            if ":" in cell:
                parts = cell.split(":")
                return len(parts)>=2 and parts[1].strip() == faculty_id
            return False

        mask = df.applymap(has_fac)
        filtered = df.where(~mask) if free_periods else df.where(mask)
        filtered = filtered.dropna(how='all', axis=0).dropna(how='all', axis=1)
        if not filtered.empty:
            result[class_id] = filtered.T
    return result

def export_timetable(timetable_dict, filename):
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        for class_id, df in timetable_dict.items():
            df.to_excel(writer, sheet_name=class_id)
