from flask import Blueprint, render_template, request, flash, current_app, send_file, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
# import qrcode
import pyotp
from . import db
import os, re
from io import BytesIO
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


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
        return redirect(url_for('auth.login'))

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
    confirm = request.form.get('confirm')
    des = request.form.get('description')
    file = request.files['profile']

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists.')
        return redirect(url_for('auth.signup'))

    if not email:
        flash('Email address is required.')
        return redirect(url_for('auth.signup'))
    
    if not name:
        flash('Name is required.')
        return redirect(url_for('auth.signup'))
    
    if not password:
        flash('Password is required.')
        return redirect(url_for('auth.signup'))
    
    if password != confirm:
        flash('Passwords don\'t match.')
        return redirect(url_for('auth.signup'))
    
    if not pass_validation(password):
        flash("Password does not meet requirements.")
        return redirect(url_for('auth.signup'))
    
    if not log_validation(name):
        flash('There is a thirteen character Username limit.')
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

def log_validation(name):
    
    if len(name) > 10:
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

@auth.route('/change_pass', methods=['GET', 'POST'])
def change_pass():
    key = pyotp.random_base32()
    totp = pyotp.TOTP(key)
    newKey = totp.now()
    session['newKey'] = newKey
    userMail = current_user.email

    message = Mail(
        from_email='dkmg@goldwyntech.com',
        to_emails=f'{userMail}',
        subject='Your Authentication Code',
        html_content= f'Your authentication code is {newKey}')
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return redirect(url_for('auth.authenticateNewKey'))
    
    except Exception as e:
        print('hi')

    return render_template('authorize.html', name = current_user.name, email = current_user.email)

@auth.route('/authorize', methods=['GET', 'POST'])
def authenticateNewKey():
    newKey = session.get('newKey')
    print(newKey)
    
    if request.method == 'POST':
        userKey = request.form.get('auth')
        newKey = session.get('newKey')
        print(userKey)
        print(newKey)
        if (newKey == userKey):
            flash('Successfully authorized')
            return redirect(url_for(f'auth.finalAuth'))

        elif(newKey != userKey):
            flash('Unsuccessful authorization.')

    return render_template('authorize.html', name = current_user.name, email = current_user.email)
    

@auth.route("/passAuth", methods=['GET', 'POST'])
def finalAuth():
   currentPass = request.form.get('currentP')
   newPass = request.form.get('cPass')
   newPassV = request.form.get('cPassV')

   if current_user.password != currentPass:
       flash('Please Re-Enter Your Current password')

   if newPass != newPassV:
       flash('Passwords do not match')

   if len(newPass) < 8 or len(newPassV) > 30:
        return render_template('authorized.html')
   
   if not re.search("[a-z]", newPass):
        return render_template('authorized.html')

   if not re.search("[A-Z]", newPass):
        return render_template('authorized.html')

   if not re.search("[0-9]", newPassV):
        return render_template('authorized.html')
       
   if not re.search("[!@#\\$%^&*(),.?\":{}|<>]", newPass):
        return render_template('authorized.html')

   current_user.password = newPass
   db.sesssion.commit()

   return redirect(url_for('main.security'))
    
    



# @auth.route('/select', methods=['POST'])
# def files():
#     sFile = request.form.get('sFile')
#     current_user.fPath = sFile
#     db.session.commit()
#     flash('sFile')
#     return redirect(url_for('main.profileInfo'))    
    