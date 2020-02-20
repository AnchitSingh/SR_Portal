from flask import render_template, url_for, flash, redirect, request
from portal import app, db, bcrypt
from portal.forms import RegistrationForm, LoginForm
from portal.models import User, Post,phd
from flask_login import login_user, current_user, logout_user, login_required
import os 
import json
from os.path import join, dirname, realpath


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Wait for admin approval', 'info')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    image_file = url_for('static',filename='faces/' + current_user.image_file)
    return render_template('account.html', title='Account',image_file=image_file)

@app.route("/dashboard")
@login_required
def dashboard():
    user=User.query.all()
    phds=phd.query.all()
    image_file = url_for('static',filename='faces/' + current_user.image_file)
    return render_template('dashboard.html', title='Dashboard',image_file=image_file,user=user,phd=phds)

@app.route("/calendar")
@login_required
def calendar():
    image_file = url_for('static',filename='faces/' + current_user.image_file)
    return render_template('calendar.html', title='Calendar',image_file=image_file)

@app.route("/profile")
@login_required
def profile():
    image_file = url_for('static',filename='faces/' + current_user.image_file)
    return render_template('profile.html', title='Profile',image_file=image_file)

@app.route("/workspace")
@login_required
def workspace():
    path=join(dirname(realpath(__file__)), 'static/pdf/')
    a=os.listdir(path)
    text=json.dumps(sorted(a))
    image_file = url_for('static',filename='faces/' + current_user.image_file)
    return render_template('workspace.html', title='WorkSpace',contents=text,image_file=image_file)


@app.route("/people")
def people():
    user=User.query.all()
    image_file = url_for('static',filename='faces/' + current_user.image_file)
    return render_template('people.html',image_file=image_file,user=user,title='Members')

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user,title='Users')