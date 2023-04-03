import pandas as pd
data = pd.read_csv("courses.csv")

def get_grade_difference(class_name):
    # creating a dataset containing classes corresponding to class name passed through that are within the past 5 years (for more relevance)
    filtered_data = data[(data['Course Title'] == class_name) & (data['Year'] >= 2018)]

    # getting all the sections for the class
    sections = filtered_data['YearTerm'].unique()

    # making a way to store the differences for each class
    grade_diffs = {
        'A+': [], 'A': [], 'A-': [],
        'B+': [], 'B': [], 'B-': [],
        'C+': [], 'C': [], 'C-': [],
        'D+': [], 'D': [], 'D-': [],
        'F': []
    }

    # looping through all pairs of sections to get the grade difference per letter grade
    for i in range(len(sections)):
        for j in range(i+1, len(sections)):
            # average grade per letter
            avg_i = filtered_data[filtered_data['YearTerm'] == sections[i]].mean()
            avg_j = filtered_data[filtered_data['YearTerm'] == sections[j]].mean()

            # calculating difference in grades oer letter grade and storing in grade_diffs
            for grade in grade_diffs:
                grade_diff = abs(avg_i[grade] - avg_j[grade])
                grade_diffs[grade].append(grade_diff)

    return grade_diffs