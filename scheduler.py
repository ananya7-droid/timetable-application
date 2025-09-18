from ortools.sat.python import cp_model
import pandas as pd

def generate_timetable(faculty_df, subject_df, lab_df, class_df, semester_id):
    # Prepare data for CP-SAT
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    periods = 6
    total_slots = len(days) * periods

    reduced_subjects = set([105,106,206,207,208,306,307])  # 2/week subjects

    # Filter semester relevant subjects and labs
    semester_subjects = subject_df[subject_df['class_id'] == semester_id].copy()
    semester_labs = lab_df[lab_df['class_id'] == semester_id].copy()

    faculty_map = faculty_df.set_index('faculty_id')[['subject_id', 'lab_id']].to_dict(orient='index')

    # Map subjects/labs to faculty
    subject_faculty = {}
    for i, subj in semester_subjects.iterrows():
        sid = str(subj['subject_id'])
        for fid, assgn in faculty_map.items():
            if sid in assgn.get('subject_id', []):
                subject_faculty[sid] = fid
                break

    lab_faculty = {}
    for i, lab in semester_labs.iterrows():
        lid = str(lab['lab_id'])
        for fid, assgn in faculty_map.items():
            if lid in assgn.get('lab_id', []):
                lab_faculty[lid] = fid
                break

    model = cp_model.CpModel()

    # Variables: subject_id x slot -> bool if subject occupies slot
    # For labs, slots represent start period since labs take 2 periods

    # Create mappings to integer indices for easier modeling
    subj_list = list(subject_faculty.keys())
    lab_list = list(lab_faculty.keys())

    subj_index = {s: i for i, s in enumerate(subj_list)}
    lab_index = {l: i for i, l in enumerate(lab_list)}

    # Slots: day * period index
    num_days = len(days)
    num_periods = periods

    # Variables
    subj_vars = {}  # (subject_idx, day, period) : bool var
    lab_vars = {}   # (lab_idx, day, period) : bool var (period here is start period for 2 consecutive)

    # Create vars for subjects (theory)
    for s, s_i in subj_index.items():
        for d in range(num_days):
            for p in range(num_periods):
                subj_vars[(s_i,d,p)] = model.NewBoolVar(f'subj{s}_d{d}_p{p}')

    # Create vars for labs (need to ensure period < num_periods-1)
    for l, l_i in lab_index.items():
        for d in range(num_days):
            for p in range(num_periods-1):  # labs occupy p and p+1
                lab_vars[(l_i,d,p)] = model.NewBoolVar(f'lab{l}_d{d}_p{p}')

    # Constraints

    # 1. Each lab assigned exactly once per week (one start slot)
    for l, l_i in lab_index.items():
        model.Add(sum(lab_vars[(l_i,d,p)] for d in range(num_days) for p in range(num_periods-1)) == 1)

    # 2. Labs occupy 2 consecutive periods (implicit in slot definition)

    # 3. Theory subjects assigned 4 times/week or 2 if in reduced set
    for s, s_i in subj_index.items():
        subj_id_int = int(subj_list[s_i]) if subj_list[s_i].isdigit() else -1
        required = 2 if subj_id_int in reduced_subjects else 4
        model.Add(sum(subj_vars[(s_i,d,p)] for d in range(num_days) for p in range(num_periods)) == required)

    # 4. No subject assigned more than once per day
    for s, s_i in subj_index.items():
        for d in range(num_days):
            model.Add(sum(subj_vars[(s_i,d,p)] for p in range(num_periods)) <= 1)

    # 5. No subject assigned in consecutive periods on same day
    for s, s_i in subj_index.items():
        for d in range(num_days):
            for p in range(num_periods - 1):
                model.AddBoolOr([subj_vars[(s_i,d,p)].Not(), subj_vars[(s_i,d,p+1)].Not()])

    # 6. Faculty clash avoidance: a faculty can't be assigned two subjects/labs at the same slot
    # Prepare a mapping slot -> list of faculty vars assigned at that slot

    for d in range(num_days):
        for p in range(num_periods):
            faculty_slots = {}
            # theory subjects
            for s, s_i in subj_index.items():
                fac = subject_faculty[subj_list[s_i]]
                if (fac, d, p) not in faculty_slots:
                    faculty_slots[(fac, d, p)] = []
                faculty_slots[(fac,d,p)].append(subj_vars[(s_i,d,p)])

            # labs: labs occupy p and p+1
            # For labs, also consider p-1 period to check clashes properly
            for l, l_i in lab_index.items():
                fac = lab_faculty[lab_list[l_i]]
                # If p is start period or second period of lab slot
                if p < num_periods -1 and (fac, d, p) not in faculty_slots:
                    faculty_slots[(fac, d, p)] = []
                if p < num_periods -1:
                    if lab_vars.get((l_i, d, p), None) is not None:
                        faculty_slots[(fac,d,p)].append(lab_vars[(l_i,d,p)])
                if p > 0:
                    # If p is second period of lab at p-1
                    if lab_vars.get((l_i,d,p-1), None) is not None:
                        faculty_slots[(fac,d,p)].append(lab_vars[(l_i,d,p-1)])

            # Add constraint: sum of assigned classes in slot for faculty ≤ 1
            for fac in set(f for (f,_,_) in faculty_slots.keys()):
                vars_list = []
                for (f2,d2,p2), vars_assigned in faculty_slots.items():
                    if f2 == fac and d2 == d and p2 == p:
                        vars_list.extend(vars_assigned)
                if vars_list:
                    model.Add(sum(vars_list) <= 1)

    # 7. Each slot has at most one subject or lab assigned (hard capacity)
    for d in range(num_days):
        for p in range(num_periods):
            vars_in_slot = []
            for s, s_i in subj_index.items():
                vars_in_slot.append(subj_vars[(s_i,d,p)])
            for l, l_i in lab_index.items():
                # lab covers two periods, so only consider start period lab_vars
                if p < num_periods - 1:
                    vars_in_slot.append(lab_vars.get((l_i,d,p), model.NewConstant(0)))
                # else period is second for lab, no var needed here
                if p > 0:
                    # if p is the second period, include lab starting at p-1
                    vars_in_slot.append(lab_vars.get((l_i,d,p-1), model.NewConstant(0)))
            model.Add(sum(vars_in_slot) <= 1)

    # Objective: Can be simply feasibility; optionally minimize gaps or preferences

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        result = []
        for s, s_i in subj_index.items():
            for d in range(num_days):
                for p in range(num_periods):
                    if solver.BooleanValue(subj_vars[(s_i,d,p)]):
                        result.append({
                            "FacultyID": subject_faculty[subj_list[s_i]],
                            "SubjectID": subj_list[s_i],
                            "ClassID": semester_id,
                            "Day": days[d],
                            "Period": p+1,
                            "StartTime": pd.to_datetime(time_slots[p][0]).time(),
                            "EndTime": pd.to_datetime(time_slots[p][1]).time(),
                            "Room": "Room 1",
                            "Type": subject_df[subject_df['subject_id'] == subj_list[s_i]]['type'].values[0],
                        })

        for l, l_i in lab_index.items():
            for d in range(num_days):
                for p in range(num_periods -1):
                    if solver.BooleanValue(lab_vars[(l_i,d,p)]):
                        result.append({
                            "FacultyID": lab_faculty[lab_list[l_i]],
                            "SubjectID": lab_list[l_i],
                            "ClassID": semester_id,
                            "Day": days[d],
                            "Period": p+1,
                            "StartTime": pd.to_datetime(time_slots[p][0]).time(),
                            "EndTime": pd.to_datetime(time_slots[p+1][1]).time(),
                            "Room": "Lab 1",
                            "Type": "lab",
                        })

        return pd.DataFrame(result)
    else:
        print("No feasible solution found!")
        return pd.DataFrame()
