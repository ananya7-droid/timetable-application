Automatic College Timetable Generator:
This project is an automated timetable generator for college courses, built using Python and Streamlit. It creates clash-free timetables for theory and lab sessions, scheduling faculty and subjects efficiently using constraint programming.

Features:
- User authentication (admin role required to generate timetable)

- Upload and parse input data via CSV files (faculty, subjects, labs, classes, users)

- Generate timetables automatically with OR-Tools CP-SAT solver

- Display timetables in a clean tabular format by day and period

- Export generated timetables to Excel files

Requirements:
- Python 3.7+

- Packages listed in requirements.txt

Installation:
- Clone the repository

- Create and activate a virtual environment (recommended)

Install dependencies:

bash
pip install -r requirements.txt

Usage:
Run the Streamlit app:

- bash
streamlit run app.py
Login as admin

- Click "Generate Timetable" for the chosen semester/class

- View the timetable and export to Excel if needed

Data Format:
Place input CSV files in the data/ folder:

faculty.csv
subjects.csv
labs.csv
classes.csv
users.csv

Acknowledgements:
This project uses Google OR-Tools for constraint-based scheduling.