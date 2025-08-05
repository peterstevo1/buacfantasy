from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"

# Load existing data or create new file
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        team = [request.form.get(f'runner{i}') for i in range(1, 6)]

        with open(DATA_FILE, 'r') as f:
            data = json.load(f)

        data.append({
            'name': name,
            'team': team
        })

        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)

        return redirect('/')
    return render_template('submit.html')
