from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('home.html')

@main.route('/profileinfo')
def profileInfo():
    return render_template('profileinfo.html', name = current_user.name)

@main.route('/profile')
@login_required
def profile():
    return render_template('home.html', name = current_user.name)
