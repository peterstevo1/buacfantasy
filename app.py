from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Team model
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    runner1 = db.Column(db.String(100))
    runner2 = db.Column(db.String(100))
    runner3 = db.Column(db.String(100))
    runner4 = db.Column(db.String(100))
    runner5 = db.Column(db.String(100))

# Create tables automatically on startup (only if they don't exist)
@app.before_first_request
def create_tables():
    db.create_all()

# Homepage
@app.route('/')
def index():
    return render_template('index.html')

# Submit team
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

# View submitted teams
@app.route('/teams')
def view_teams():
    teams = Team.query.all()
    return render_template('teams.html', teams=teams)

if __name__ == '__main__':
    app.run(debug=True)
