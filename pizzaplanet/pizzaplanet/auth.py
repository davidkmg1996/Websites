from flask import Blueprint, render_template, request, flash, current_app, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from . import db
import os, re
from io import BytesIO
from flask import Blueprint, render_template, redirect, url_for

auth = Blueprint('auth', __name__)

@auth.route('/home')
def login():
    
    return render_template('home.html')

@auth.route('/login', methods=['POST'])
def login_post():
    
    if current_user.is_authenticated:
        logout_user()

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
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    else:
        return render_template('signup.html')
    
@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    des = request.form.get('description')
    file = request.files['profile']

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    if not email:
        flash('Email address is required')
        return redirect(url_for('auth.signup'))
    
    if not name:
        flash('Name is required')
        return redirect(url_for('auth.signup'))
    
    if not password:
        flash('Password is required')
        return redirect(url_for('auth.signup'))
    
    if not pass_validation(password):
        flash("Password does not meet requirements.")
        return redirect(url_for('auth.signup'))
    
    if file and file.filename.endswith(('png', 'jpg', 'jpeg', 'gif')):
        img = file.read()
    
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='pbkdf2:sha256'), des=des, profPic = img)

    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))

def pass_validation(password):

    if len(password) < 8 or len(password) > 30:
        return False
   
    if not re.search("[a-z]", password):
        return False

    if not re.search("[A-Z]", password):
        return False

    if not re.search("[0-9]", password):
        return False
       
    if not re.search("[!@#\\$%^&*(),.?\":{}|<>]", password):
        return False
    
    return True

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

# @auth.route('/uploads', methods=['POST'])
# def upload():
#     file = request.files['file']
#     uploadF= current_app.config['UPLOAD']
#     img = file.read()

#     if not os.path.exists(uploadF):
#         os.makedirs(uploadF)

#     user = current_user
#     user.fPath = img
#     db.session.commit()

#     return render_template('editprofile.html', name = current_user.name, des = current_user.des, img = img)

@auth.route('/uploads', methods=['POST'])
def profilePic():
    newPic = request.files['profile']
    profilePic = current_app.config['UPLOAD']
    pPic = newPic.read()

    if not os.path.exists(profilePic):
        os.makedirs(profilePic)

    user = current_user
    user.profPic = pPic
    db.session.commit()
    flash('Profile Picture Successfuly Changed')
    return render_template('editprofile.html', name = current_user.name, des = current_user.des, pPic = current_user.profPic)

@auth.route('/view_image')
def view_image():
    user = current_user
    if user and user.fPath:
        return send_file(BytesIO(user.fPath), mimetype='image/png') 
    return "No image found"

@auth.route('/profile_pic')
def profile_pic():
    user = current_user
    if user and user.profPic:
        return send_file(BytesIO(user.profPic), mimetype='image/png') 
    return "No image found"



# @auth.route('/select', methods=['POST'])
# def files():
#     sFile = request.form.get('sFile')
#     current_user.fPath = sFile
#     db.session.commit()
#     flash('sFile')
#     return redirect(url_for('main.profileInfo'))    
    