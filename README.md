# 📅 Timetable Generator

A Streamlit-based **automated timetable generator** for Data Analytics classes (1st, 2nd, and 3rd year).  
It schedules faculty, subjects, and classrooms while avoiding conflicts.

---

## 🚀 Features
- Automatic timetable generation
- Conflict prevention (faculty, class, subject)
- Support for 3 year groups (DA 1, 2, 3)
- Interactive dashboard (Streamlit)
- Export data in CSV/Excel/PDF

---

## 🛠️ Tech Stack
- **Python**
- **Streamlit** (frontend + dashboards)
- **Pandas** (data handling)
- **CSV/Excel** (data input/output)

---

# 📂 Project Structure

timetable-generator/ │── app.py              # Main Streamlit frontend │── scheduler.py        # Timetable scheduling logic │── utils.py            # Helper functions (conflict checks, etc.) │── requirements.txt    # Dependencies │── data/ │    ├── classes.csv │    ├── faculty.csv │    └── subjects.csv │── README.md

---

# ⚡ Installation
Clone this repo and install requirements:
```bash
pip install -r requirements.txt

streamlit run app.py



---

👉 Do you want me to now also give you **ready-to-paste code for `app.py`, `scheduler.py`, and `utils.py`** so you can add them on GitHub the same way?
