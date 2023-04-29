from django.shortcuts import render
from flask import Flask, render_template, request, jsonify
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
from io import BytesIO
import base64
import seaborn as sns

df = pd.read_csv("courses.csv")
grade = df
grade["GPA"] = (grade['A+']*4 + grade['A']*4 + grade['A-']*3.67 + grade['B+']*3.33 + grade['B']*3 + grade['B-']*2.67 + grade['C+']*2.33 + grade['C']*2 + grade['C-']*1.67 + grade['D+']*1.33 + grade['D']*1 +  grade['D-']*0.67 + grade['F']*0)/(grade['A+'] + grade['A'] + grade['A-'] + grade['B+'] + grade['B'] + grade['B-'] + grade['C+'] + grade['C'] + grade['C-'] + grade['D+'] + grade['D'] +  grade['D-'] + grade['F']) 
grade_course = grade.groupby([grade["Subject"], grade["Course Title"]])['GPA'].mean().reset_index()
grade_time = grade.groupby([grade["Year"], grade["Term"], grade["Subject"], grade["Course Title"]])['GPA'].mean().reset_index()
grade_professor = grade.groupby([grade["Year"], grade["Term"], grade["Subject"], grade["Course Title"], grade['Primary Instructor']])['GPA'].mean().reset_index()



app = Flask(__name__)

# Helper Functions

def get_major(subject):
  return df[df['Subject'] == subject][['Course Title']].drop_duplicates(keep='first').reset_index()


def get_gpa(course_title, year, term):
  return grade_time[(grade_time['Course Title'] == course_title) & (grade_time['Year'] == year) & (grade_time['Term'] == term)][['GPA']].reset_index()

def get_class_by_major_time(major, year, term):
  return df[(df['Subject'] == major) & (df['Year'] == year) & (df['Term'] == term)][['Course Title']].reset_index()

def GetAllSubject():
    subjects = df['Subject'].unique()
    return subjects

def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i,y[i],y[i], ha = 'center')
 
def get_plot_by_subject(subject):
        img = BytesIO()
        # x-coordinates of left sides of bars 
        left = ['A+','A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F']
        
        # heights of bars
        temp = df[(df['Subject'] == subject)]
        height = [temp['A+'].sum(), temp['A'].sum(), temp['A-'].sum(), temp['B+'].sum(), temp['B'].sum(), temp['B-'].sum(), temp['C+'].sum(), temp['C'].sum(), temp['C-'].sum(), temp['D+'].sum(), temp['D'].sum(), temp['D-'].sum(), temp['F'].sum()]

        # plotting a bar chart
        plt.bar(left, height,
                width = 0.8, color = ['red', 'green'])
        
        # add label 
        addlabels(left, height)

        # naming the x-axis
        plt.xlabel(subject)
        # naming the y-axis
        plt.ylabel('Count')
        # plot title
        plt.title('Grade')
        
        plt.savefig(img, format = 'png')
        plt.close()
        img.seek(0)
        return base64.b64encode(img.getvalue()).decode('utf8')

def get_plot_by_course(subject, course_number):
        img = BytesIO()
        # x-coordinates of left sides of bars 
        left = ['A+','A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F']
        
        # heights of bars
        temp = df[(df['Subject'] == subject) & (df['Number'] == int(course_number))]
        height = [temp['A+'].sum(), temp['A'].sum(), temp['A-'].sum(), temp['B+'].sum(), temp['B'].sum(), temp['B-'].sum(), temp['C+'].sum(), temp['C'].sum(), temp['C-'].sum(), temp['D+'].sum(), temp['D'].sum(), temp['D-'].sum(), temp['F'].sum()]

        # plotting a bar chart
        plt.bar(left, height,
                width = 0.8, color = ['red', 'green'])
        
        # add label 
        addlabels(left, height)
        # naming the x-axis
        plt.xlabel( temp['Course Title'].unique()[0])
        # naming the y-axis
        plt.ylabel('Count')
        # plot title
        plt.title('Grade')
        
        plt.savefig(img, format = 'png')
        plt.close()
        img.seek(0)
        return base64.b64encode(img.getvalue()).decode('utf8')

def get_heatmap(subject, number, year, term):
    img = BytesIO()

    temp = grade[(grade["Subject"] == subject) & (grade["Number"] == int(number)) & (grade["Year"] == int(year)) & (grade["Term"] == term)]
    
    data = temp[["Primary Instructor", "A+",'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F']]
    print(data)

    sns.heatmap(data=data[["A+",'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F']], square=True,cmap="RdBu_r", annot=True, fmt="d", linewidths=0.3)  
    plt.plot()
    plt.xlabel("Grade")
    plt.ylabel("Primary Instructors")
    plt.title("Heatmap for " + temp['Course Title'].unique()[0]) 
    plt.savefig(img, format = 'png')
    plt.close()
    
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode('utf8')

# Routing Functions

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/plotgrade")
def plotgrade():
    return render_template("plotgrades.html", subjects = GetAllSubject(), graph = False, invalid = False, image_url = '')

@app.route("/plotgradebycourse")
def plotcoursegrade():
    return render_template("plotcoursegrades.html", subjects = GetAllSubject(), graph = False, invalid = False, image_url = "")

@app.route("/heatmap")
def heatmap():
    return render_template("heatmap.html", subjects = GetAllSubject(), graph = False, invalid = False, image_url = "")

# Plots new graph
@app.route('/plotgrade', methods = ["POST"])
def plotgradebysubject():
    subject = request.form.to_dict()['course']
    if (subject not in GetAllSubject()):
        return render_template("plotgrades.html", subjects = GetAllSubject(), graph = False, invalid = True, image_url = '')
    img_url = get_plot_by_subject(subject)
    return render_template("plotgrades.html", subjects = GetAllSubject(), graph = True, invalid = False, image_url = img_url)

@app.route('/plotgradebycourse', methods = ["POST"])
def plotgradebycourse():
    subject = request.form.to_dict()['course']
    number = request.form.to_dict()['number']
    num_list = df[df['Subject'] == subject]['Number'].unique()
    if (subject not in GetAllSubject()):
        return render_template("plotcoursegrades.html", subjects = GetAllSubject(), graph = False, invalid = True, image_url = '')
    if (int(number) not in num_list):
        return render_template("plotcoursegrades.html", subjects = GetAllSubject(), graph = False, invalid = True, image_url = '')
    img_url = get_plot_by_course(subject, number)
    return render_template("plotcoursegrades.html", subjects = GetAllSubject(), graph = True, invalid = False, image_url = img_url)

@app.route('/heatmap', methods = ["POST"])
def heatmap_plot():
    subject = request.form.to_dict()['course']
    number = request.form.to_dict()['course number']
    year = request.form.to_dict()['year']
    season = request.form.to_dict()['season']
    num_list = df[df['Subject'] == subject]['Number'].unique()
    if (subject not in GetAllSubject()):
        return render_template("heatmap.html", subjects = GetAllSubject(), graph = False, invalid = True, image_url = '')
    if (int(number) not in num_list):
        return render_template("heatmap.html", subjects = GetAllSubject(), graph = False, invalid = True, image_url = '')
    if (not (season == "Spring" or season == "Fall")):
        return render_template("heatmap.html", subjects = GetAllSubject(), graph = False, invalid = True, image_url = '')
    if (int(year) < 2010 or int(year) > 2022):
        return render_template("heatmap.html", subjects = GetAllSubject(), graph = False, invalid = True, image_url = '')
    img_url = get_heatmap(subject, number, year, season)
    return render_template("heatmap.html", subjects = GetAllSubject(), graph = True, invalid = False, image_url = img_url)