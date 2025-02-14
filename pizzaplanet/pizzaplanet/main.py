from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .auth import auth as auth_blueprint


main = Blueprint('main', __name__)

@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.userHome'))
    return render_template('home.html')

@main.route('/profileinfo')
def profileInfo():
    if current_user.is_authenticated:
        return render_template('profileinfo.html', name = current_user.name or 'Guest', des=current_user.des or '')
    else:
        return render_template('home.html')
    
@main.route('/profile')
def profile():
    if current_user.is_authenticated:
        return redirect(url_for('main.userHome'))
    
    return render_template('home.html')

@main.route('/editProfile')
@login_required
def editProfile():
    if current_user.is_authenticated:
        return render_template('editprofile.html', name = current_user.name or 'Guest', des = current_user.des, fPath = current_user.fPath)
    else:
        return render_template('home.html')

@main.route('/index')
@login_required
def userHome():
    return render_template('index.html', name = current_user.name)

@main.route('/security')
@login_required
def security():
    return render_template('security.html', name = current_user.name)


