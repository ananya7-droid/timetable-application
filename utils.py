import pandas as pd

def get_teacher_timetable(timetable_dict, faculty_id, free_periods=False):
    """
    Returns dict: class_id -> timetable DataFrame (days as rows, periods as columns)
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
            # Transpose for display: periods as columns, days as rows
            result[class_id] = filtered.T

    return result

def get_class_timetable(timetable_dict, class_id):
    return timetable_dict.get(class_id, pd.DataFrame())

def export_timetable(timetable_dict, filename):
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        for class_id, df in timetable_dict.items():
            df.to_excel(writer, sheet_name=class_id)
