from flask import Flask,abort, session, render_template, url_for, flash, redirect, request,send_file
from portal import app, db, bcrypt,mail
from portal.forms import RegistrationForm, LoginForm,PostForm,RequestResetForm,ResetPasswordForm
from portal.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import os 
import json
from os import path
from os.path import join, dirname, realpath
from sqlalchemy.sql.functions import func
from sqlalchemy.sql import text
from sqlalchemy import update
import pandas as pd
import sqlite3
from datetime import datetime ,date ,timedelta
from portal.mtech.routes import mData
from portal.phd.routes import phdData
from portal.course import cdir
from portal.helper_code.helper import delete_courses

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()



def fillReport(msg,usr,dt):
    conn = sqlite3.connect('portal/site.db') 
    c = conn.cursor()
    c.execute("INSERT INTO violations (Report,User,Date) VALUES (?,?,?) ",(msg,usr,dt))
    conn.commit()
    conn.close()
    return


@app.route("/violation", methods=['GET', 'POST'])
@login_required
def violation():
    if current_user.is_active == True:
        if current_user.is_admin == True:
            conn = sqlite3.connect('portal/site.db') 
            c = conn.cursor()
            c.execute('''DROP TABLE violations;''')
            c.execute('''
                    CREATE TABLE violations (
                        "id" INTEGER  PRIMARY KEY AUTOINCREMENT,
                        "Report" TEXT,
                        "User" TEXT,
                        "Date" TEXT
            );''')
            conn.commit()
            conn.close()
            flash('Database successfully created', 'info')
            return redirect(url_for('dashboard'))
        else:
            return render_template('error.html',error=403)
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))


UPLOAD_FOLDER_PDF = 'portal/static/pdf/'
app.config['UPLOAD_FOLDER_PDF'] = UPLOAD_FOLDER_PDF

UPLOAD_FOLDER_CSV = 'portal/static/original-csv/'
app.config['UPLOAD_FOLDER_CSV'] = UPLOAD_FOLDER_CSV



@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if current_user.is_active == True:
        if current_user.is_admin == True or current_user.is_manager == True:
            user=User.query.all()
            image_file = url_for('static',filename='assets/img/faces/' + current_user.image_file)
            if request.method == 'POST' and 'csv' in request.files:
                files = request.files.getlist("csv")
                i=0
                for file in files:
                    file.save(os.path.join(app.config['UPLOAD_FOLDER_CSV'], file.filename))
                    i=i+1
                flash(str(i) +' csv files uploaded successfully ', 'info')
            if request.method == 'POST' and 'pdf' in request.files:
                files = request.files.getlist("pdf")
                i=0
                for file in files:
                    file.save(os.path.join(app.config['UPLOAD_FOLDER_PDF'], file.filename))
                    i=i+1
                flash(str(i) +' pdf files uploaded successfully ', 'info')
            return render_template('upload.html',title='Uploads',image_file=image_file,user=user)
        else:
            return render_template('error.html',error=404)
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))



@app.route('/upload_pdf', methods=['GET', 'POST'])
@login_required
def upload_pdf():
    if current_user.is_active == True:
        if current_user.is_admin == True or current_user.is_manager == True:
            if request.method == 'POST' and 'file' in request.files:
                files = request.files.getlist("file")
                i=0
                for file in files:
                    file.save(os.path.join(app.config['UPLOAD_FOLDER_PDF'], file.filename))
                    i=i+1
                flash(str(i) +' pdf files uploaded successfully ', 'info')
            return redirect(url_for('upload'))
        else:
            return render_template('error.html',error=404)
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))


@app.route('/upload_csv', methods=['GET', 'POST'])
@login_required
def upload_csv():
    if current_user.is_active == True:
        if current_user.is_admin == True or current_user.is_manager == True:
            if request.method == 'POST' and 'file' in request.files:
                files = request.files.getlist("file")
                i=0
                for file in files:
                    file.save(os.path.join(app.config['UPLOAD_FOLDER_CSV'], file.filename))
                    i=i+1
                flash(str(i) +' csv files uploaded successfully ', 'info')
            return redirect(url_for('upload'))
        else:
            return render_template('error.html',error=404)
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))




@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('check'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Wait for admin approval', 'info')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)





@app.route("/admin_register/<key>", methods=['GET', 'POST'])
def admin_register(key):
    if '180085180200' == key:
        user=User.query.all()
        check=1
        for u in user:
            if u.is_admin==True:
                check=0
                break
        if check==1:
            if current_user.is_authenticated:
                return redirect(url_for('checkUser'))
            form = RegistrationForm()
            if form.validate_on_submit():
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                user = User(username=form.username.data, email=form.email.data, password=hashed_password,is_admin=True,is_active=True,is_manager=True)
                db.session.add(user)
                db.session.commit()
                flash('You are now admin.', 'info')
                return redirect(url_for('login'))
            return render_template('register.html', title='Register', form=form)
        elif check==0:
            flash('Admin account already exists','info')
            return redirect(url_for('login'))
    else:
        render_template('error.html',error=404)



@app.route("/")
def root():
    return redirect(url_for('login'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('checkUser'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('checkUser'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/checkUser")
@login_required
def checkUser():
    if current_user.is_active == True:
        check1=0
        if current_user.is_admin==True or current_user.is_manager==True:
            conn = sqlite3.connect('portal/site.db') 
            c = conn.cursor()
            c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='phd' ''')
            if c.fetchone()[0]==1 :
                check1=1
            else:
                phdData()
            c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='mtech' ''')
            if c.fetchone()[0]==1 :
                check1=1
            else:
                mData()
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('workspace'))
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))




@app.route("/dashboard")
@login_required
def dashboard():
    if current_user.is_active == True:
        if current_user.is_admin == True or current_user.is_manager == True:
            user=User.query.all()
            post=Post.query.all()
            image_file = url_for('static',filename='assets/img/faces/' + current_user.image_file)
            pi=0
            mi=0
            pc=0
            for p in post:
                pc+=1
            p_sub_count=0
            p_val_count=0
            m_sub_count=0
            m_val_count=0
            u_val=0
            m_val=0
            a_val=0
            p_bundle=1
            m_bundle=1
            conn = sqlite3.connect('portal/site.db') 
            c = conn.cursor()
            pobj=c.execute('''SELECT * FROM phd''').fetchall()
            mobj=c.execute('''SELECT * FROM mtech''').fetchall()
            pobj=[tup[::-1] for tup in pobj]
            mobj=[tup[::-1] for tup in mobj]
            for p in pobj:
                pi+=1
                if p[4] == 'Done' and p[8] == 'Done':
                    p_sub_count=p_sub_count+1
                if p[6] == 'Done':
                    p_val_count=p_val_count+1
            for p in mobj:
                mi+=1
                if p[4] == 'Done' and p[8] == 'Done':
                    m_sub_count=m_sub_count+1
                if p[6] == 'Done':
                    m_val_count=m_val_count+1
            for x in user:
                if x.is_admin == False and x.is_manager == False and x.is_active == True:
                    u_val=u_val+1
                if x.is_admin == False and x.is_manager == True and x.is_active == True:
                    m_val=m_val+1
                if x.is_admin == True and x.is_active == True:
                    a_val=a_val+1
            conn.close()
            return render_template('dashboard.html', title='Dashboard',
                            image_file=image_file,phd=pobj,
                            user=user,pi=pi,p_sub_count=p_sub_count,
                            p_val_count=p_val_count,u_val=u_val,m_val=m_val,a_val=a_val,
                            p_bundle=p_bundle,mtech=mobj,
                            mi=mi,m_sub_count=m_sub_count,
                            m_val_count=m_val_count,pc=pc,
                            m_bundle=m_bundle,post=post)
        else:
            return render_template('error.html',error=404)
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))


def checkStamps():
    conn = sqlite3.connect('portal/site.db') 
    c = conn.cursor()
    pobj=c.execute('''SELECT * FROM phd''').fetchall()
    mobj=c.execute('''SELECT * FROM mtech''').fetchall()
    pobj=[tup[::-1] for tup in pobj]
    mobj=[tup[::-1] for tup in mobj]





@app.route("/reset")
@login_required
def reset():
    if current_user.is_active == True:
        if current_user.is_admin == True:
            conn = sqlite3.connect('portal/site.db') 
            c = conn.cursor()
            test=c.execute('''SELECT * FROM violations''').fetchall()
            image_file = url_for('static',filename='assets/img/faces/' + current_user.image_file)
            return render_template('reset.html', title='Reset',image_file=image_file,violations=test)
        else:
            report=str(current_user.username)+'  tried to accessed unauthorized route -> Reset '
            fillReport(report,current_user.username,datetime.now())
            flash('This incident will be reported ','danger')
            return render_template('error.html',error=403)
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))


@app.route("/profile")
@login_required
def profile():
    if current_user.is_active == True:
        image_file = url_for('static',filename='assets/img/faces/' + current_user.image_file)
        return render_template('profile.html', title='Profile',image_file=image_file)
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))



@app.route("/extra_courses")
@login_required
def extra_courses():
    if current_user.is_active == True:
        image_file = url_for('static',filename='assets/img/faces/' + current_user.image_file)
        return render_template('extra.html', title='Extra Courses',image_file=image_file)
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))



@app.route("/workspace")
@login_required
def workspace():
    if current_user.is_active == True:
        user=User.query.all()
        image_file = url_for('static',filename='assets/img/faces/' + current_user.image_file)
        return render_template('workspace.html', title='WorkSpace',image_file=image_file,user=user)
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))


@app.route("/add_course", methods=['GET', 'POST'])
@login_required
def add_course():
    if current_user.is_active == True:
        if current_user.is_admin==True or current_user.is_manager== True:
            image_file = url_for('static',filename='assets/img/faces/' + current_user.image_file)
            return render_template('add_course.html', title='Add New Course',image_file=image_file)
        else:
            report=str(current_user.username)+'  tried to accessed unauthorized route -> Reset '
            fillReport(report,current_user.username,datetime.now())
            flash('This incident will be reported ','danger')
            return render_template('error.html',error=403)
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))

@app.route("/course", methods=['GET', 'POST'])
@login_required
def course():
    if current_user.is_active == True:
        if current_user.is_admin==True or current_user.is_manager== True:
            new_course=request.form['ncourse']
            cdir(new_course)
            return redirect(url_for('add_course'))
        else:
            report=str(current_user.username)+'  tried to accessed unauthorized route -> Reset '
            fillReport(report,current_user.username,datetime.now())
            flash('This incident will be reported ','danger')
            return render_template('error.html',error=403)
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))


@app.route("/dcourse", methods=['GET', 'POST'])
@login_required
def dcourse():
    if current_user.is_active == True:
        if current_user.is_admin==True or current_user.is_manager== True:
            delete_courses()
            return redirect(url_for('workspace'))
        else:
            report=str(current_user.username)+'  tried to accessed unauthorized route -> Reset '
            fillReport(report,current_user.username,datetime.now())
            flash('This incident will be reported ','danger')
            return render_template('error.html',error=403)
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))


@app.route("/people")
@login_required
def people():
    if current_user.is_active == True:
        user=User.query.all()
        image_file = url_for('static',filename='assets/img/faces/' + current_user.image_file)
        return render_template('people.html',image_file=image_file,user=user,title='Members')
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    if current_user.is_active == True:
        form=PostForm()
        user=User.query.all()
        post=Post.query.all()
        image_file = url_for('static',filename='assets/img/faces/' + current_user.image_file)
        if form.validate_on_submit():
            if current_user.is_admin==True or current_user.is_manager==True:
                post = Post(title=form.title.data, content=form.content.data, author=current_user)
                db.session.add(post)
                db.session.commit()
                flash('Your post has been created!', 'success')
                return redirect(url_for('new_post'))
        return render_template('announcements.html',image_file=image_file,user=user,title='Announcements',form=form,post=post)
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))

@app.route("/delete_post/<post_id>", methods=['POST','GET'])
@login_required
def delete_post(post_id):
    if current_user.is_active == True:
        post = Post.query.get_or_404(post_id)
        if post.author != current_user:
            return render_template('error.html',error=403)
        else:
            db.session.delete(post)
            db.session.commit()
            flash('Your post has been deleted!', 'success')
            return redirect(url_for('new_post'))

@app.route('/user/<username>')
@login_required
def user(username):
    if current_user.is_active == True:
        user = User.query.filter_by(username=username).first_or_404()
        return render_template('user.html', user=user,title='Users')
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))



def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='flaskbeta@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(message=msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('A email has been sent with instructions to reset your password','info')
        return redirect(url_for('login'))
    return render_template('reset_request.html',title= 'Reset Password',form=form)



@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
