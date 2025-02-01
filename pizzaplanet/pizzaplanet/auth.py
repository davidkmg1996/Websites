from flask import Blueprint, render_template, request, flash, current_app, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from . import db
import os
from io import BytesIO
from flask import Blueprint, render_template, redirect, url_for

auth = Blueprint('auth', __name__)

@auth.route('/home')
def login():
    return render_template('home.html')

@auth.route('/login', methods=['POST'])
def login_post():

    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = User.query.filter_by(email=email).first()

    if not email:
        flash('Email is required.')
        return redirect(url_for('auth.login'))
    
    if not password:
        flash('Password is required.')

    if not user or not check_password_hash(user.password, password):
        flash('Incorrect email or password.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.userHome'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    des = request.form.get('description')

    if not email:
        flash('Email address is required')
        return redirect(url_for('auth.signup'))
    
    if not name:
        flash('Name is required')
        return redirect(url_for('auth.signup'))
    
    if not password:
        flash('Password is required')
        return redirect(url_for('auth.signup'))

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))
    
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='pbkdf2:sha256'), des=des)

    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))

@auth.route('/editnew', methods=['POST'])
def edit():
    newDes = request.form.get('editDesc')

    if not newDes:
        flash('Cannot be left blank')
        return redirect(url_for('main.editProfile'))


    current_user.des = newDes
    db.session.commit()
    return render_template('editprofile.html', name = current_user.name, des = current_user.des)

@auth.route('/logout')
def logout():
   logout_user()
   return redirect(url_for('main.index'))

@auth.route('/uploads', methods=['POST'])
def upload():
    file = request.files['file']
    fName = secure_filename(file.filename)
    uploadF= current_app.config['UPLOAD']
    
    img = file.read()

    if not os.path.exists(uploadF):
        os.makedirs(uploadF)

    user = current_user
    user.fPath = img
    db.session.commit()

    return render_template('editprofile.html', name = current_user.name, des = current_user.des, img = img)

@auth.route('/view_image')
def view_image():
    user = current_user
    if user and user.fPath:
        return send_file(BytesIO(user.fPath), mimetype='image/png') 
    return "No image found"

# @auth.route('/select', methods=['POST'])
# def files():
#     sFile = request.form.get('sFile')
#     current_user.fPath = sFile
#     db.session.commit()
#     flash('sFile')
#     return redirect(url_for('main.profileInfo'))    
    