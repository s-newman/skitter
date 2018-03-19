from ui import app
from flask import render_template

# Routes for webpages
@app.route('/')
def index():
    return render_template('index.html', scripts=True)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', scripts=True)

@app.route('/new-account')
def new_account():
    return render_template('new-account.html', scripts=True)

@app.route('/settings')
def settings():
    return render_template('settings.html', scripts=True, jquery=True)