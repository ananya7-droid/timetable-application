# Format & transpose for display: PERIODS on X-axis, DAYS on Y-axis
for cls in list(timetable.keys()):
    df_raw = timetable[cls]
    df_fmt = replace_ids(df_raw)
    timetable[cls] = df_fmt.T  # <-- transpose here for display

if role == "admin":
    st.subheader("Class Timetables")
    for cls in classes_df['class_id']:
        st.markdown(f"### Class: {cls}")
        st.table(timetable.get(cls, pd.DataFrame()))

    st.subheader("Teacher Timetables")
    for _, row in faculty_df.iterrows():
        fid = row['faculty_id']
        fname = row['faculty_name']
        st.markdown(f"### {fname} (ID: {fid})")
        tt = get_teacher_timetable(timetable, fid)
        if not tt:
            st.write("No assigned periods")
        else:
            for cname, df in tt.items():
                st.markdown(f"**Class {cname}**")
                st.table(df)
