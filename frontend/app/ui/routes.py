from ui import app
from ui.utils import *
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
    cnx = connect_db()

    # Get user information
    cnx.execute('PREPARE get_info FROM ' +
                '\'SELECT * FROM USER_INFO WHERE rit_username = ?\';')
    cnx.execute('SET @a = \'{}\';'.format(user))
    result = [row for row in cnx.execute('EXECUTE get_info USING @a;')][0]

    # Get profile picture URL
    cnx.execute('PREPARE get_pic FROM ' +
                '\'SELECT * FROM PROFILE_PICTURE WHERE picture_id = ?\';')
    cnx.execute('SET @a = \'{}\';'.format(result[5]))
    picture_url = [r for r in cnx.execute('EXECUTE get_pic USING @a;')][0][1]

    # Render page
    return render_template('profile.html', scripts=True, username=result[0],
                           fname=result[1], lname=result[2], pic=picture_url)


@app.route('/logout')
def logout():
    return render_template('logout.html')
