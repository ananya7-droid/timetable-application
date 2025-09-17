import pandas as pd

def get_teacher_timetable(timetable_df, faculty_id, free_periods=False):
    """
    Returns a dict of class-wise timetables filtered for the given faculty_id.
    If free_periods=True, returns periods where faculty is free.
    """
    result = {}
    for class_id, df in timetable_df.items():
        # Filter cells where faculty_id appears in the cell text
        def cell_contains_faculty(cell):
            if pd.isna(cell):
                return False
            return faculty_id in cell

        teacher_cells = df.applymap(cell_contains_faculty)

        if free_periods:
            # Free periods = cells where faculty_id NOT present
            free_df = df.where(~teacher_cells)
            if not free_df.empty:
                result[class_id] = free_df.dropna(how='all', axis=0).dropna(how='all', axis=1)
        else:
            # Timetable cells for this faculty only
            teach_df = df.where(teacher_cells)
            if not teach_df.empty:
                result[class_id] = teach_df.dropna(how='all', axis=0).dropna(how='all', axis=1)

    if len(result) == 1:
        # Return single DataFrame if only one class found
        return next(iter(result.values()))
    return result


def get_class_timetable(timetable_df, class_id):
    """
    Returns timetable DataFrame for the given class_id from timetable dict.
    """
    return timetable_df.get(class_id, pd.DataFrame())


def export_timetable(timetable_df, filename):
    """
    Export the timetable dict to an Excel file, each class in a separate sheet.
    """
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        for class_id, df in timetable_df.items():
            df.to_excel(writer, sheet_name=class_id)
    print(f"Timetable exported to {filename}")
