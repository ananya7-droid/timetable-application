from ortools.sat.python import cp_model
import pandas as pd

def generate_timetable(faculty_df, subject_df, lab_df, class_df, semester_id):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    time_slots = [
        ("12:25 PM", "1:15 PM"),
        ("1:15 PM", "2:05 PM"),
        ("2:05 PM", "2:55 PM"),
        ("3:10 PM", "4:00 PM"),
        ("4:00 PM", "4:50 PM"),
        ("4:50 PM", "5:40 PM"),
    ]
    total_periods = len(time_slots)

    semester_subjects = subject_df[subject_df["class_id"] == semester_id].copy()
    semester_labs = lab_df[lab_df["class_id"] == semester_id].copy()

    faculty_map = faculty_df.set_index("faculty_id")[["subject_id", "lab_id"]].to_dict(orient="index")

    subject_faculty = {}
    for _, subj in semester_subjects.iterrows():
        sid = str(subj["subject_id"])
        for fid, assgn in faculty_map.items():
            if sid in assgn.get("subject_id", []):
                subject_faculty[sid] = fid
                break

    lab_faculty = {}
    for _, lab in semester_labs.iterrows():
        lid = str(lab["lab_id"])
        for fid, assgn in faculty_map.items():
            if lid in assgn.get("lab_id", []):
                lab_faculty[lid] = fid
                break

    model = cp_model.CpModel()

    subj_list = list(subject_faculty.keys())
    lab_list = list(lab_faculty.keys())

    subj_index = {s: i for i, s in enumerate(subj_list)}
    lab_index = {l: i for i, l in enumerate(lab_list)}

    num_days = len(days)
    num_periods = total_periods

    subj_vars = {}
    lab_vars = {}

    for s, s_i in subj_index.items():
        for d in range(num_days):
            for p in range(num_periods):
                subj_vars[(s_i, d, p)] = model.NewBoolVar(f"subj{s}_d{d}_p{p}")

    for l, l_i in lab_index.items():
        for d in range(num_days):
            for p in range(num_periods - 1):
                lab_vars[(l_i, d, p)] = model.NewBoolVar(f"lab{l}_d{d}_p{p}")

    # Each lab assigned exactly once per week
    for l, l_i in lab_index.items():
        model.Add(sum(lab_vars[(l_i, d, p)] for d in range(num_days) for p in range(num_periods - 1)) == 1)

    # Faculty clash avoidance
    for d in range(num_days):
        for p in range(num_periods):
            for fid in faculty_map.keys():
                assigned_vars = []
                for s, s_i in subj_index.items():
                    if subject_faculty[subj_list[s_i]] == fid:
                        assigned_vars.append(subj_vars[(s_i, d, p)])
                for l, l_i in lab_index.items():
                    if lab_faculty[lab_list[l_i]] == fid:
                        if p < num_periods - 1:
                            assigned_vars.append(lab_vars.get((l_i, d, p), model.NewConstant(0)))
                        if p > 0:
                            assigned_vars.append(lab_vars.get((l_i, d, p - 1), model.NewConstant(0)))
                if assigned_vars:
                    model.Add(sum(assigned_vars) <= 1)

    # Max 2 occurrences per subject per day
    for s, s_i in subj_index.items():
        for d in range(num_days):
            model.Add(sum(subj_vars[(s_i, d, p)] for p in range(num_periods)) <= 2)

    # Subjects assigned exactly 4 times per week
    for s, s_i in subj_index.items():
        model.Add(sum(subj_vars[(s_i, d, p)] for d in range(num_days) for p in range(num_periods)) == 4)

    # No consecutive periods for subject per day
    for s, s_i in subj_index.items():
        for d in range(num_days):
            for p in range(num_periods - 1):
                model.AddBoolOr([subj_vars[(s_i, d, p)].Not(), subj_vars[(s_i, d, p + 1)].Not()])

    # Subjects appear at most once in periods 4,5,6 combined per day (key constraint)
    for s, s_i in subj_index.items():
        for d in range(num_days):
            model.Add(sum(subj_vars[(s_i, d, p)] for p in range(3, 6)) <= 1)

    # Every slot must be assigned exactly one subject or lab (full fill)
    for d in range(num_days):
        for p in range(num_periods):
            slot_vars = []
            for s, s_i in subj_index.items():
                slot_vars.append(subj_vars[(s_i, d, p)])
            for l, l_i in lab_index.items():
                if p < num_periods - 1:
                    slot_vars.append(lab_vars.get((l_i, d, p), model.NewConstant(0)))
                if p > 0:
                    slot_vars.append(lab_vars.get((l_i, d, p - 1), model.NewConstant(0)))
            model.Add(sum(slot_vars) == 1)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        result = []
        for s, s_i in subj_index.items():
            for d in range(num_days):
                for p in range(num_periods):
                    if solver.BooleanValue(subj_vars[(s_i, d, p)]):
                        result.append({
                            "FacultyID": subject_faculty[subj_list[s_i]],
                            "SubjectID": subj_list[s_i],
                            "ClassID": semester_id,
                            "Day": days[d],
                            "Period": p + 1,
                            "Type": "theory"
                        })
        for l, l_i in lab_index.items():
            for d in range(num_days):
                for p in range(num_periods - 1):
                    if solver.BooleanValue(lab_vars[(l_i, d, p)]):
                        result.append({
                            "FacultyID": lab_faculty[lab_list[l_i]],
                            "SubjectID": lab_list[l_i],
                            "ClassID": semester_id,
                            "Day": days[d],
                            "Period": p + 1,
                            "Type": "lab"
                        })
        return pd.DataFrame(result)
    else:
        print("No feasible solution found!")
        return pd.DataFrame()
