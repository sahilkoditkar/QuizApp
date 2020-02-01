
from flask import Flask, render_template, request, redirect, url_for, session
import json, random

app = Flask(__name__)
app.secret_key = "igniteMCQ"

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/authenticate', methods = ['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']

    with open('users.json') as file:
        users = json.load(file)
    for user in users:
        if username == user['username'] and password == user['password']:
            session['username'] = username
            return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    with open('users.json') as file:
        users = json.load(file)
    for user in users:
        if session['username'] == user['username']:
            return render_template('dashboard.html', User = user)
    return redirect(url_for('login'))

@app.route('/test/<event>')
def test(event):
    with open('{}.json'.format(event)) as file:
        mcqs = json.load(file)
    random.shuffle(mcqs)
    for mcq in mcqs:
        random.shuffle(mcq['options'])
    return render_template('test.html', Event = event, MCQs = mcqs)

@app.route('/submit/<event>', methods=['POST'])
def submitTest(event):
    correct = 0
    with open('{}.json'.format(event)) as file:
        mcqs = json.load(file)
    for mcq in mcqs:
        if mcq['options'][0] == request.form[mcq['question']]:
            correct+=1
    return '<h1>Correct Answers: <u>'+str(correct)+'</u></h1>'

if __name__ == '__main__':
	app.run(debug=True)
