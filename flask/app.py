from django.shortcuts import render
from flask import Flask, jsonify, request, render_template, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("test.html", data = "Hello World!")

class Student:
    def __init__(self, name, age, gpa):
        self.name = name
        self.age = age
        self.gpa = gpa

@app.route("/otherpage")
def otherpage():
    s1 = Student("Marcus", 13, 2.6)
    s2 = Student("HJ", 20, 3.9)
    s3 = Student("Michael", 18, 2.0)
    students = [s1, s2, s3]
    return render_template("test2.html", data = students)