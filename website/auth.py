from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Contact, Costumer
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy import and_

auth = Blueprint('auth',__name__)

@auth.route('/about')
def about():
    return render_template("about.html", user=current_user)

@auth.route('/')
def index():
    return render_template("index.html", user=current_user)

@auth.route('/east')
def east():
    return render_template("east.html", user=current_user)

@auth.route('/west')
def west():
    return render_template("west.html", user=current_user)

@auth.route('/north')
def north():
    return render_template("north.html", user=current_user)

@auth.route('/northeast')
def northeast():
    return render_template("northeast.html", user=current_user)

@auth.route('/central')
def central():
    return render_template("central.html", user=current_user)

@auth.route('/south')
def south():
    return render_template("south.html", user=current_user)

@auth.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == 'POST':  
        name = request.form.get('name')
        email = request.form.get('email')
        contact = request.form.get('contact')
        role = request.form.get('role')
        message = request.form.get('message')
        
        if len(name) < 3:
            flash('Name must be at least 2 characters.',category='error')
        elif len(email) < 3:
            flash('Email must be at least 3 characters.',category='error')
        elif not (contact.isdigit() and len(contact) == 10):                            
            flash('Contact must be at 10 digits.', category='error')
        elif len(message) < 3:
            flash('Message must be at least 3 characters.',category='error')    
        else:
            feedback = Contact(name=name, email=email, contact=contact, role=role, message=message)
            db.session.add(feedback)
            db.session.commit()
            flash('Feedback successfully send!',category='success')
        
    return render_template("contact.html", user=current_user)

@auth.route('/database')
def database():
    return render_template("database.html", user=current_user)

@auth.route('/state/<state_name>', methods=['GET','POST'])
def state(state_name):
    state_select = User.query.filter_by(state = state_name)
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        pname = User.query.filter(and_(User.state == state_name,User.product_name.like(search)))
        return render_template('state.html', user=pname, tag=tag, title=state_name)
    return render_template("state.html", user=state_select, title=state_name)

@auth.route('/state/<state_name>/info/<id>', methods=['GET','POST'])
def info(state_name,id):
    return render_template("info.html", user=User.query.filter_by(id = id) , title=id)

@auth.route('/login', methods=['GET','POST'])
def login(): 
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')     
        
        if email == "admin@mail.com" and password == "admin123":
            return redirect(url_for('views.admin'))
        elif role == 'weavers':
            user = User.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password, password):
                    flash('Login successfully!',category='success')
                    login_user(user,remember=True)
                    return redirect(url_for('views.profile'))
                else:
                    flash('Incorrect password',category='error')
            else:
                flash('User does not exist!',category='error')
        elif role == 'costumer':
            user = Costumer.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password, password):
                    flash('Login successfully!',category='success')
                    login_user(user,remember=True)
                    return redirect(url_for('views.order',email=email))
                else:
                    flash('Incorrect password',category='error')
            else:
                flash('User does not exist!',category='error')
    return render_template("login.html", user=current_user)

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        role = request.form.get('role')        
        
        if role == 'weavers':
            user = User.query.filter_by(email=email).first()
            if user:
                flash('Email already exists.', category='error')
            elif len(email) < 4:
                flash('Email must be at least 3 characters.',category='error')
            elif len(firstName) < 3:
                flash('First name must be at least 2 characters.',category='error')
            elif password1 != password2:
                flash('Password does not match.',category='error')
            elif len(password1) < 8:
                flash('Password must be at least 7 characters.',category='error')
            else:
                new_user = User(email=email, first_name=firstName, password=generate_password_hash(password1,method='sha256'), contact='None', company_Name='None', state='None', address='None', product_name='None', description='None', image='website/static/images/profile/00default.png')
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user,remember=True)
                flash('Account created!.',category='success')
                return redirect(url_for('views.profile'))
        elif role == 'costumer':
            user = Costumer.query.filter_by(email=email).first()
            if user:
                flash('Email already exists.', category='error')
            elif len(email) < 4:
                flash('Email must be at least 3 characters.',category='error')
            elif len(firstName) < 3:
                flash('First name must be at least 2 characters.',category='error')
            elif password1 != password2:
                flash('Password does not match.',category='error')
            elif len(password1) < 8:
                flash('Password must be at least 7 characters.',category='error')
            else:
                new_user = Costumer(email=email, name=firstName, password=generate_password_hash(password1,method='sha256'), contact='None', address='None',company_Name='None',product_name='None',quantity = 1,price='--',status='order')
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user,remember=True)
                flash('Account created!.',category='success')
                return redirect(url_for('views.order',email=email))
    return render_template("signUp.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Successfully logout!',category='success')
    return redirect(url_for('auth.login'))