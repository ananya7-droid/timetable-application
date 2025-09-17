def get_teacher_timetable(timetable_df, faculty_id, free_periods=False):
    result = {}
    for class_id, df in timetable_df.items():
        # Filter timetable cells for this faculty_id (match faculty name)
        # Because timetable cells are like "SubjectName\nFacultyName"
        mask = df.applymap(lambda x: False if pd.isna(x) else faculty_id not in x and faculty_id not in x)
        filtered = df.where(df.applymap(lambda cell: faculty_id in str(cell) if pd.notna(cell) else False))

        if free_periods:
            # Show only free periods (cells where teacher not present)
            free_df = df.where(df.applymap(lambda cell: faculty_id not in str(cell) if pd.notna(cell) else True))
            if not free_df.empty:
                result[class_id] = free_df
        else:
            # Normal timetable
            if not filtered.empty:
                result[class_id] = filtered.dropna(how='all')

    if len(result) == 1:
        return list(result.values())[0]
    return result

def get_class_timetable(timetable_df, class_id):
    return timetable_df.get(class_id, pd.DataFrame())
