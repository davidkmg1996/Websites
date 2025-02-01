from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('home.html')

@main.route('/profileinfo')
def profileInfo():
    if current_user.is_authenticated:
        return render_template('profileinfo.html', name = current_user.name or 'Guest', des=current_user.des or '')
    else:
        return render_template('home.html')
@main.route('/profile')
def profile():
    return render_template('home.html')

@main.route('/index')
@login_required
def userHome():
    return render_template('index.html', name = current_user.name)


