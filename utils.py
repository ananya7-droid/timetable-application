import pandas as pd

def get_teacher_timetable(timetable_dict, faculty_id, free_periods=False):
    """
    Returns a dict mapping class_id -> DataFrame for that teacher.
    Always returns a dict, even if only one class.
    DataFrame is transposed: days = rows, periods = columns.
    """
    result = {}

    for class_id, df in timetable_dict.items():
        def has_fac(cell):
            if pd.isna(cell) or cell=="":
                return False
            if ":" in cell:
                sid, fid = cell.split(":")
                return fid.strip() == faculty_id
            return False

        mask = df.applymap(has_fac)

        if free_periods:
            filtered = df.where(~mask)
        else:
            filtered = df.where(mask)

        # drop empty rows/columns
        filtered = filtered.dropna(how='all', axis=0).dropna(how='all', axis=1)

        if not filtered.empty:
            result[class_id] = filtered.T  # transpose for display

    return result  # always dict


def export_timetable(timetable_dict, filename):
    """
    Exports the timetable dict to an Excel file, each class in a separate sheet.
    """
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        for class_id, df in timetable_dict.items():
            df.to_excel(writer, sheet_name=class_id)
