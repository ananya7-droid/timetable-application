import pandas as pd

def get_class_timetable(timetable_dict, class_id):
    return timetable_dict.get(class_id, pd.DataFrame())

def get_teacher_timetable(timetable_dict, faculty_id, free_periods=False):
    result = {}
    for class_id, df in timetable_dict.items():
        # define mask of cells where that faculty teaches
        def has_fac(cell):
            if pd.isna(cell) or cell == "":
                return False
            parts = str(cell).split(':')
            if len(parts) >= 2 and parts[1].strip() == faculty_id:
                return True
            return False

        mask = df.applymap(has_fac)

        if free_periods:
            free_df = df.where(~mask)
            free_df2 = free_df.dropna(how='all', axis=0).dropna(how='all', axis=1)
            if not free_df2.empty:
                result[class_id] = free_df2
        else:
            teach_df = df.where(mask)
            teach_df2 = teach_df.dropna(how='all', axis=0).dropna(how='all', axis=1)
            if not teach_df2.empty:
                result[class_id] = teach_df2

    if not result:
        return pd.DataFrame()
    if len(result) == 1:
        # return just the DataFrame for that class
        return next(iter(result.values()))
    return result

def export_timetable(timetable_dict, filename):
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        for class_id, df in timetable_dict.items():
            df.to_excel(writer, sheet_name=class_id)
