import pandas as pd

data = pd.read_csv("courses.csv")

# conversion factors for letter grades
letter_grade_points = {
    'A+': 4.0, 'A': 4.0, 'A-': 3.7,
    'B+': 3.3, 'B': 3.0, 'B-': 2.7,
    'C+': 2.3, 'C': 2.0, 'C-': 1.7,
    'D+': 1.3, 'D': 1.0, 'D-': 0.7,
    'F': 0.0
}

def get_section_gpa(section):
    # getting the data for section passed
    section_data = data[data['YearTerm'] == section]

    # calculating total GPA per section
    total_points = 0
    total_credits = 0
    for index, row in section_data.iterrows():
        for grade, value in letter_grade_points.items():
            if row[grade] > 0:
                total_points += value * row[grade]
                total_credits += row[grade]

    if total_credits > 0:
        return total_points / total_credits
    else:
        return None

def get_gpa_difference(section1, section2):
    section1_gpa = get_section_gpa(section1)
    section2_gpa = get_section_gpa(section2)

    # calculating difference in gpa and figuring out which class has the higher one
    if section1_gpa is not None and section2_gpa is not None:
        gpa_difference = abs(section1_gpa - section2_gpa)
        if section1_gpa > section2_gpa:
            higher_gpa_prof = data[data['YearTerm'] == section1]['Primary Instructor'].iloc[0]
        elif section2_gpa > section1_gpa:
            higher_gpa_prof = data[data['YearTerm'] == section2]['Primary Instructor'].iloc[0]
        else:
            higher_gpa_prof = "Both professors' sections are good choices."
            # returns associated prof
        return gpa_difference, higher_gpa_prof
    else:
        return None