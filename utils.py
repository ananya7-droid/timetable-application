def check_conflicts(df):
    conflicts = []
    grouped = df.groupby(["day", "slot"])
    for (day, slot), g in grouped:
        if g['faculty'].duplicated().any():
            conflicts.append((day, slot, "Teacher conflict"))
        if g['class_id'].duplicated().any():
            conflicts.append((day, slot, "Class conflict"))
    return conflicts
