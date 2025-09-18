import pandas as pd

def get_class_timetable(timetable_dict, class_id):
    return timetable_dict.get(class_id, pd.DataFrame())

def get_teacher_day_timetable(timetable_dict, faculty_id, day):
    result = []
    for class_id, df in timetable_dict.items():
        if day in df.columns:
            for period in df.index:
                cell = df.at[period, day]
                if pd.isna(cell) or cell == "":
                    result.append({
                        "Period": period,
                        "Class": class_id,
                        "Subject": "",
                        "Status": "Free"
                    })
                elif isinstance(cell, str) and ":" in cell:
                    sid, fid = cell.split(":")
                    if fid.strip() == faculty_id:
                        result.append({
                            "Period": period,
                            "Class": class_id,
                            "Subject": sid.strip(),
                            "Status": "Scheduled"
                        })
    df_result = pd.DataFrame(result)
    return df_result.sort_values(by="Period") if not df_result.empty else pd.DataFrame()

def export_timetable(timetable_dict, filename):
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        for class_id, df in timetable_dict.items():
            df.to_excel(writer, sheet_name=str(class_id))
