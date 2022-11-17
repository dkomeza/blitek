import json

from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_bs4 import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField
from wtforms.validators import DataRequired
from math import sqrt

import statistics

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'ghj5678(*^678&*(hjk&*JKL'
date = datetime.now()


class LoginForm(FlaskForm):
    """formularz logowania"""
    userLogin = StringField('Nazwa użytkownika:', validators=[DataRequired()])
    userPass = PasswordField('Hasło:', validators=[DataRequired()])
    submit = SubmitField('Zaloguj')

users = {1: {
    'userLogin': 'dkomeza',
    'userPass': 'haslo',
    'fname': 'Dawid',
    'lname': 'Komęza'
}}

def countAverage(subjectValue, termValue):
    """funkcja obliczająca średnie"""
    with open('data/grades.json', encoding='utf-8') as gradesFile:
        grades = json.load(gradesFile)
        gradesFile.close()
    sum = 0
    len = 0
    if subjectValue == "" and termValue == "":
        for subject, terms in grades.items():
            for term, categories in terms.items():
                for category, grades in categories.items():
                    if category == 'answer' or category == 'quiz' or category == 'test':
                        for grade in grades:
                            sum += grade
                            len += 1
    else:
        for subject, terms in grades.items():
            if subject == subjectValue:
                for term, categories in terms.items():
                    if term == termValue:
                        for category, grades in categories.items():
                            if category == 'answer' or category == 'quiz' or category == 'test':
                                for grade in grades:
                                    sum += grade
                                    len += 1
    return round(sum/len, 2)

@app.route('/')
def index():
    return render_template('index.html', title='Strona główna', userLogin=session.get('userLogin'), date=date)

@app.route('/logIn', methods=['POST', 'GET'])
def logIn():
    login = LoginForm()
    if login.validate_on_submit():
        userLogin = login.userLogin.data
        userPass = login.userPass.data
        if userLogin == users[1]['userLogin'] and userPass == users[1]['userPass']:
            session['userLogin'] = userLogin
            return redirect('dashboard')
    return render_template('login.html', title='Logowanie', login=login, userLogin=session.get('userLogin'), date=date)

@app.route('/logOut')
def logOut():
    session.pop('userLogin')
    return redirect('logIn')

@app.route('/dashboard')
def dashboard():
    with open('data/grades.json', encoding='utf-8') as gradesFile:
        grades = json.load(gradesFile)
        gradesFile.close()
    sorting = []
    for subject in grades:
        allGrades = []
        for term in grades[subject]:
            for grade in grades[subject][term]:
                if grade == "answer" or grade == "quiz" or grade == "test":
                    for singleGrade in grades[subject][term][grade]:
                        allGrades.append(singleGrade)
        sorting.append([subject, round(statistics.mean(allGrades) * 100) / 100])
    high = sorted(sorting, key=lambda x: x[1], reverse=True)
    low = sorted(sorting, key=lambda x: x[1], reverse=False)
    bestGrades = [high[0], high[1]]
    badGrades = []
    for subject in low:
        if subject[1] > 2:
            break
        badGrades.append(subject)
    print(badGrades)
    return render_template('dashboard.html', title='Dashboard', userLogin=session.get('userLogin'), date=date, grades=grades, countAverage=countAverage, badGrades=badGrades, bestGrades=bestGrades)

@app.errorhandler(404)
def pageNotFound(error):
    return render_template('404.html', date=date), 404

@app.errorhandler(500)
def internalServerError(error):
    return render_template('500.html', date=date), 500

if __name__ == '__main__':
    app.run(debug=True, port=3000, host= "127.0.0.1")