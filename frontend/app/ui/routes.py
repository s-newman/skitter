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
    return render_template('settings.html', scripts=True)


@app.route('/profile/<user>')
def profile(user):
    return render_template('profile.html', scripts=True, user=user)


@app.route('/logout')
def logout():
    return render_template('logout.html')
