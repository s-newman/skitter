from ui import app
from flask import render_template

@app.route('/')
def index():
    return render_template('index.html', scripts=True, jquery=True)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
