from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os
import sys

app = Flask(__name__)

# Set up database
database_url = os.environ.get("DATABASE_URL", "sqlite:///local.db")

if not database_url:
    print("❌ ERROR: DATABASE_URL is not set!", file=sys.stderr)
    raise RuntimeError("DATABASE_URL must be set")

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define model
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    runner1 = db.Column(db.String(100))
    runner2 = db.Column(db.String(100))
    runner3 = db.Column(db.String(100))
    runner4 = db.Column(db.String(100))
    runner5 = db.Column(db.String(100))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        team = Team(
            name=request.form['name'],
            runner1=request.form.get('runner1'),
            runner2=request.form.get('runner2'),
            runner3=request.form.get('runner3'),
            runner4=request.form.get('runner4'),
            runner5=request.form.get('runner5'),
        )
        db.session.add(team)
        db.session.commit()
        return redirect('/')
    return render_template('submit.html')

@app.route('/teams')
def view_teams():
    teams = Team.query.all()
    return render_template('teams.html', teams=teams)

if __name__ == '__main__':
    app.run(debug=True)
