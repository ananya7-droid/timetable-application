import pandas as pd

def get_class_timetable(timetable_dict, class_id):
    return timetable_dict.get(class_id, pd.DataFrame())

def get_teacher_timetable(timetable_dict, faculty_id, free_periods=False):
    """
    Returns either a dict of class DataFrames or one DataFrame
    showing where this faculty_id has scheduled classes, or free periods.
    """

    result = {}
    for class_id, df in timetable_dict.items():
        # create boolean mask of where cell contains faculty_id
        def has_fac(cell):
            if pd.isna(cell) or cell == "":
                return False
            # expecting format "subject_id:faculty_id"
            parts = str(cell).split(':')
            if len(parts) >= 2 and parts[1].strip() == faculty_id:
                return True
            return False

        mask = df.applymap(has_fac)

        if free_periods:
            # free = where mask is False
            free_df = df.where(~mask)
            # drop rows and columns that are completely empty
            free_df2 = free_df.dropna(how='all', axis=0).dropna(how='all', axis=1)
            if not free_df2.empty:
                result[class_id] = free_df2
        else:
            teach_df = df.where(mask)
            teach_df2 = teach_df.dropna(how='all', axis=0).dropna(how='all', axis=1)
            if not teach_df2.empty:
                result[class_id] = teach_df2

    if len(result) == 0:
        return pd.DataFrame()
    if len(result) == 1:
        return next(iter(result.values()))
    return result

def export_timetable(timetable_dict, filename):
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        for class_id, df in timetable_dict.items():
            df.to_excel(writer, sheet_name=class_id)
