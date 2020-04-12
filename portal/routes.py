from flask import Flask,abort, session, render_template, url_for, flash, redirect, request
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


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route("/allocate_phd", methods=['GET', 'POST'])
@login_required
def allocate_phd():
    if current_user.is_active==True:
        if current_user.is_admin == True:
            conn = sqlite3.connect('portal/site.db') 
            c = conn.cursor()
            test=c.execute('''SELECT * FROM phd''').fetchall()
            test=[tup[::-1] for tup in test] 
            test = [list(ele) for ele in test] 
            user=User.query.all()
            def foo(user,test):
                i=0
                user_val=0
                phd_val=0
                flag1=1
                # for p in test:
                #     p[1]="1"
                for x in user:
                    if x.is_admin == False and x.is_manager == False and x.is_active == True:
                        user_val=user_val+1
                for pd in test:
                    phd_val=phd_val+1
                if user_val==0:
                    flash('No Tutor exists','danger')
                else:
                    quotient = phd_val//user_val 
                    remainder = phd_val%user_val 
                    #flash(phd_val)
                    
                    for p in test:
                        c.execute('''update phd set alloc_status = "0" WHERE Application = "'''+p[0]+'''";''')
                        conn.commit()
                        c.execute('''update phd set Tutor1 = "0" WHERE Application = "'''+p[0]+'''";''')
                        conn.commit()
                        
                    for u in user:
                        flag1=1
                        conn.commit()
                        i=0
                        conn.commit()
                        if u.is_admin==False and u.is_manager==False and u.is_active == True:
                            # print(u.username)
                            conn.commit()
                            for p in test:
                                # c.execute('''update phd set Tutor1 = "'''+p[1]+'''" WHERE Application = "'''+p[0]+'''";''')
                                # conn.commit()
                                if  i==quotient:
                                    if  remainder > 0 :
                                        flag1=0
                                        if p[1]=="0":
                                            p[1]="1"
                                            conn.commit()
                                            c.execute('''update phd set Tutor1 = "'''+u.username+'''" WHERE Application = "'''+p[0]+'''";''')
                                            conn.commit()
                                            c.execute('''update phd set alloc_status = "1" WHERE Application = "'''+p[0]+'''";''')
                                            conn.commit()
                                            remainder =remainder - 1
                                            flag1=1
                                    if  flag1 == 1:
                                        i=0
                                        break
                                if i<quotient and p[1]=="0" :
                                    p[1]="1"
                                    conn.commit()
                                    c.execute('''update phd set alloc_status = "1" WHERE Application = "'''+p[0]+'''";''')
                                    conn.commit()
                                    c.execute('''update phd set Tutor1 = "'''+u.username+'''" WHERE Application = "'''+p[0]+'''";''')
                                    conn.commit()
                                    c.execute('''update phd set alloc_status = "1" WHERE Application = "'''+p[0]+'''";''')
                                    conn.commit()
                                    i=i+1
                                conn.commit()
                    for p in test:
                        p[1]="1"
                    flag1=1
                    quotient = phd_val//user_val
                    remainder = phd_val%user_val
                    fla=0
                    i=0
                    for u in user:
                        flag1=1
                        if u.is_admin==False and u.is_manager==False and u.is_active == True :
                            if fla==1:
                                for p in test:
                                    if i==quotient:
                                        if remainder > 0 :
                                            flag1=0
                                            if p[1]=="1" and p[3] != u.username:
                                                p[1]="0"
                                                c.execute('''update phd set Tutor2 = "'''+u.username+'''" WHERE Application = "'''+p[0]+'''";''')
                                                conn.commit()
                                                c.execute('''update phd set alloc_status = "0" WHERE Application = "'''+p[0]+'''";''')
                                                conn.commit()
                                                remainder =remainder - 1
                                                flag1=1
                                        if flag1 == 1:
                                            i=0
                                            break
                                    if i<quotient and p[1]=="1" and p[3]!=u.username:
                                        p[1]="0"
                                        conn.commit()
                                        c.execute('''update phd set Tutor2 = "'''+u.username+'''" WHERE Application = "'''+p[0]+'''";''')
                                        conn.commit()
                                        c.execute('''update phd set alloc_status = "0" WHERE Application = "'''+p[0]+'''";''')
                                        conn.commit()
                                        i=i+1
                            fla=1
                        
                    flag1=1
                    fla=0
                    quotient = phd_val//user_val
                    i=0
                    for u in user:
                        flag1=1
                        if u.is_admin==False and u.is_manager==False and u.is_active == True:
                            for p in test:
                                if i==quotient:
                                    if remainder > 0 :
                                        flag1=0
                                        if p[1] =="1" and p[3] != u.username:
                                            p[1]="0"
                                            conn.commit()
                                            c.execute('''update phd set Tutor2 = "'''+u.username+'''" WHERE Application = "'''+p[0]+'''";''')
                                            conn.commit()
                                            c.execute('''update phd set alloc_status = "0" WHERE Application = "'''+p[0]+'''";''')
                                            conn.commit()
                                            remainder =remainder - 1
                                            flag1=1
                                    if flag1 == 1:
                                        i=0
                                        break
                                if i<quotient and p[1]=="1" and p[3]!=u.username:
                                    p[1]="0"
                                    conn.commit()
                                    c.execute('''update phd set Tutor2 = "'''+u.username+'''" WHERE Application = "'''+p[0]+'''";''')
                                    conn.commit()
                                    c.execute('''update phd set alloc_status = "0" WHERE Application = "'''+p[0]+'''";''')
                                    conn.commit()
                                    i=i+1
                            break
                    for pd in test:
                        pd[1]="1"
                    flash("Phd files allocated successfully","success")
            foo(user,test)
            return redirect(url_for('phd'))
        else:
            report=str(current_user.username)+'  tried to accessed unauthorized route -> allocate_phd '
            fillReport(report,current_user.username,datetime.now())
            return render_template('error.html',error=404)
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))


@app.route("/allocate_mtech", methods=['GET', 'POST'])
@login_required
def allocate_mtech():
    if current_user.is_active==True:
        if current_user.is_admin == True:
            conn = sqlite3.connect('portal/site.db') 
            c = conn.cursor()
            test=c.execute('''SELECT * FROM mtech''').fetchall()
            test=[tup[::-1] for tup in test] 
            test = [list(ele) for ele in test] 
            user=User.query.all()
            def foo(user,test):
                i=0
                user_val=0
                mtech_val=0
                flag1=1
                # for p in test:
                #     p[1]="1"
                for x in user:
                    if x.is_admin == False and x.is_manager == False and x.is_active == True:
                        user_val=user_val+1
                for pd in test:
                    mtech_val=mtech_val+1
                quotient = mtech_val//user_val 
                remainder = mtech_val%user_val 
                #flash(mtech_val)
                
                for p in test:
                    c.execute('''update mtech set alloc_status = "0" WHERE Application = "'''+p[0]+'''";''')
                    conn.commit()
                    c.execute('''update mtech set Tutor1 = "0" WHERE Application = "'''+p[0]+'''";''')
                    conn.commit()
                    
                for u in user:
                    flag1=1
                    conn.commit()
                    i=0
                    conn.commit()
                    if u.is_admin==False and u.is_manager==False and u.is_active == True:
                        # print(u.username)
                        conn.commit()
                        for p in test:
                            # c.execute('''update mtech set Tutor1 = "'''+p[1]+'''" WHERE Application = "'''+p[0]+'''";''')
                            # conn.commit()
                            if  i==quotient:
                                if  remainder > 0 :
                                    flag1=0
                                    if p[1]=="0":
                                        p[1]="1"
                                        conn.commit()
                                        c.execute('''update mtech set Tutor1 = "'''+u.username+'''" WHERE Application = "'''+p[0]+'''";''')
                                        conn.commit()
                                        c.execute('''update mtech set alloc_status = "1" WHERE Application = "'''+p[0]+'''";''')
                                        conn.commit()
                                        remainder =remainder - 1
                                        flag1=1
                                if  flag1 == 1:
                                    i=0
                                    break
                            if i<quotient and p[1]=="0" :
                                p[1]="1"
                                conn.commit()
                                c.execute('''update mtech set alloc_status = "1" WHERE Application = "'''+p[0]+'''";''')
                                conn.commit()
                                c.execute('''update mtech set Tutor1 = "'''+u.username+'''" WHERE Application = "'''+p[0]+'''";''')
                                conn.commit()
                                c.execute('''update mtech set alloc_status = "1" WHERE Application = "'''+p[0]+'''";''')
                                conn.commit()
                                i=i+1
                            conn.commit()
                for p in test:
                    p[1]="1"
                flag1=1
                quotient = mtech_val//user_val
                remainder = mtech_val%user_val
                fla=0
                i=0
                for u in user:
                    flag1=1
                    if u.is_admin==False and u.is_manager==False and u.is_active == True :
                        if fla==1:
                            for p in test:
                                if i==quotient:
                                    if remainder > 0 :
                                        flag1=0
                                        if p[1]=="1" and p[3] != u.username:
                                            p[1]="0"
                                            c.execute('''update mtech set Tutor2 = "'''+u.username+'''" WHERE Application = "'''+p[0]+'''";''')
                                            conn.commit()
                                            c.execute('''update mtech set alloc_status = "0" WHERE Application = "'''+p[0]+'''";''')
                                            conn.commit()
                                            remainder =remainder - 1
                                            flag1=1
                                    if flag1 == 1:
                                        i=0
                                        break
                                if i<quotient and p[1]=="1" and p[3]!=u.username:
                                    p[1]="0"
                                    conn.commit()
                                    c.execute('''update mtech set Tutor2 = "'''+u.username+'''" WHERE Application = "'''+p[0]+'''";''')
                                    conn.commit()
                                    c.execute('''update mtech set alloc_status = "0" WHERE Application = "'''+p[0]+'''";''')
                                    conn.commit()
                                    i=i+1
                        fla=1
                    
                flag1=1
                fla=0
                quotient = mtech_val//user_val
                i=0
                for u in user:
                    flag1=1
                    if u.is_admin==False and u.is_manager==False and u.is_active == True:
                        for p in test:
                            if i==quotient:
                                if remainder > 0 :
                                    flag1=0
                                    if p[1] =="1" and p[3] != u.username:
                                        p[1]="0"
                                        conn.commit()
                                        c.execute('''update mtech set Tutor2 = "'''+u.username+'''" WHERE Application = "'''+p[0]+'''";''')
                                        conn.commit()
                                        c.execute('''update mtech set alloc_status = "0" WHERE Application = "'''+p[0]+'''";''')
                                        conn.commit()
                                        remainder =remainder - 1
                                        flag1=1
                                if flag1 == 1:
                                    i=0
                                    break
                            if i<quotient and p[1]=="1" and p[3]!=u.username:
                                p[1]="0"
                                conn.commit()
                                c.execute('''update mtech set Tutor2 = "'''+u.username+'''" WHERE Application = "'''+p[0]+'''";''')
                                conn.commit()
                                c.execute('''update mtech set alloc_status = "0" WHERE Application = "'''+p[0]+'''";''')
                                conn.commit()
                                i=i+1
                        break
                for pd in test:
                    pd[1]="1"
                flash("Mtech files allocated successfully","success")
            foo(user,test)
            return redirect(url_for('mtech'))
        else:
            report=str(current_user.username)+'  tried to accessed unauthorized route -> allocate_mtech '
            fillReport(report,current_user.username,datetime.now())
            return render_template('error.html',error=404)
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))

@app.route("/mcsv", methods=['GET', 'POST'])
@login_required
def mcsv():
    if current_user.is_active ==True:
        if current_user.is_admin == True:
            conn = sqlite3.connect('portal/site.db') 
            c = conn.cursor()
            df=pd.read_csv('portal/static/original-csv/mtech.csv')
            c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='mtech' ''')
            if c.fetchone()[0]==1 :
                c.execute('''DROP TABLE mtech;''')
            c.execute('''
                    CREATE TABLE mtech (
                        "Application Ref. No." TEXT  PRIMARY KEY UNIQUE
            );''')
            new_columns=set(df.columns)
            new_columns.remove('Application Ref. No.')
            s=list(new_columns)
            for i in range(len(s)):
                c.execute('''ALTER TABLE mtech ADD'''+''' "'''+s[i]+'''" '''+'''TEXT''')
            df.to_sql(name='mtech', con=db.engine, if_exists = 'append', index=False)
            c.execute('''ALTER TABLE mtech ADD tt2 DATE  DEFAULT "None"''')
            c.execute('''ALTER TABLE mtech ADD tt1 DATE DEFAULT "None"''')
            c.execute('''ALTER TABLE mtech ADD ft2 DATE DEFAULT "None"''')
            c.execute('''ALTER TABLE mtech ADD st2 DATE DEFAULT "None"''')
            c.execute('''ALTER TABLE mtech ADD ft1 DATE DEFAULT "None"''')
            c.execute('''ALTER TABLE mtech ADD st1 DATE DEFAULT "None"''')
            c.execute('''ALTER TABLE mtech ADD Comment2 TEXT''')
            c.execute('''ALTER TABLE mtech ADD Submission2 TEXT DEFAULT "Pending" ''')
            c.execute('''ALTER TABLE mtech ADD Reject_Reason TEXT''')
            c.execute('''ALTER TABLE mtech ADD Validation TEXT DEFAULT "Pending" ''')
            c.execute('''ALTER TABLE mtech ADD Comment1 TEXT''')
            c.execute('''ALTER TABLE mtech ADD Submission1 TEXT DEFAULT "Pending" ''')
            c.execute('''ALTER TABLE mtech ADD Tutor1 TEXT DEFAULT "Not Assigned" ''')
            c.execute('''ALTER TABLE mtech ADD Tutor2 TEXT DEFAULT "Not Assigned" ''')
            c.execute('''ALTER TABLE mtech ADD alloc_status TEXT DEFAULT "0" ''')
            c.execute('''ALTER TABLE mtech ADD Application TEXT''')
            c.execute('''update mtech set Application = "Application Ref. No."; ''')
            # test=c.execute('''SELECT * from mtech''').fetchall()
            conn.commit()
            conn.close()
            flash('Database successfully created', 'info')
            return redirect(url_for('upload'))
        else:
            return render_template('error.html',error=404)
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))



@app.route("/pcsv", methods=['GET', 'POST'])
@login_required
def pcsv():
    if current_user.is_active ==True:
        if current_user.is_admin == True:
            conn = sqlite3.connect('portal/site.db') 
            c = conn.cursor()
            df=pd.read_csv('portal/static/original-csv/phd-10.csv')
            c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='phd' ''')
            if c.fetchone()[0]==1 :
                c.execute('''DROP TABLE phd;''')
            c.execute('''
                    CREATE TABLE phd (
                        "Application Ref. No." TEXT  PRIMARY KEY UNIQUE
            );''')
            new_columns=set(df.columns)
            new_columns.remove('Application Ref. No.')
            s=list(new_columns)
            for i in range(len(s)):
                c.execute('''ALTER TABLE phd ADD'''+''' "'''+s[i]+'''" '''+'''TEXT''')
            df.to_sql(name='phd', con=db.engine, if_exists = 'append', index=False)
            c.execute('''ALTER TABLE phd ADD tt2 DATE  DEFAULT "None"''')  #15
            c.execute('''ALTER TABLE phd ADD tt1 DATE DEFAULT "None"''')   #14
            c.execute('''ALTER TABLE phd ADD ft2 DATE  DEFAULT "None"''')   #13
            c.execute('''ALTER TABLE phd ADD st2 DATE DEFAULT "None"''')   #12
            c.execute('''ALTER TABLE phd ADD ft1 DATE DEFAULT "None"''')   #11
            c.execute('''ALTER TABLE phd ADD st1 DATE DEFAULT "None"''')   #10
            c.execute('''ALTER TABLE phd ADD Comment2 TEXT''')
            c.execute('''ALTER TABLE phd ADD Submission2 TEXT DEFAULT "Pending" ''')
            c.execute('''ALTER TABLE phd ADD Reject_Reason TEXT''')
            c.execute('''ALTER TABLE phd ADD Validation TEXT DEFAULT "Pending" ''')
            c.execute('''ALTER TABLE phd ADD Comment1 TEXT''')
            c.execute('''ALTER TABLE phd ADD Submission1 TEXT DEFAULT "Pending" ''')
            c.execute('''ALTER TABLE phd ADD Tutor1 TEXT DEFAULT "Not Assigned" ''')
            c.execute('''ALTER TABLE phd ADD Tutor2 TEXT DEFAULT "Not Assigned" ''')
            c.execute('''ALTER TABLE phd ADD alloc_status TEXT DEFAULT "0" ''')
            c.execute('''ALTER TABLE phd ADD Application TEXT''')
            c.execute('''update phd set Application = "Application Ref. No."; ''')
            # test=c.execute('''SELECT * from phd''').fetchall()
            conn.commit()
            conn.close()
            flash('Database successfully created', 'info')
            return redirect(url_for('upload'))
        else:
            return render_template('error.html',error=404)
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))




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


UPLOAD_FOLDER1 = 'portal/static/pdf/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER1



@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if current_user.is_active == True:
        if current_user.is_admin == True or current_user.is_manager == True:
            user=User.query.all()
            image_file = url_for('static',filename='assets/img/faces/' + current_user.image_file)
            if request.method == 'POST' and 'file' in request.files:
                files = request.files.getlist("file")
                i=0
                for file in files:
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
                    i=i+1
                flash(str(i) +' files uploaded successfully ', 'info')
            return render_template('upload.html',title='Uploads',image_file=image_file,user=user)
        else:
            return render_template('error.html',error=404)
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')



@app.route("/reset_phd", methods=['GET', 'POST'])
@login_required
def reset_phd():
    if current_user.is_active == True:
        if current_user.is_admin == True:
            conn = sqlite3.connect('portal/site.db') 
            c = conn.cursor()
            c.execute('''DELETE FROM phd;''')
            c.execute('''DELETE FROM violations;''')
            conn.commit()
            conn.close()
            return redirect(url_for('phd'))
        else:
            report=str(current_user.username)+'  tried to accessed unauthorized route -> Phd Reset '
            fillReport(report,current_user.username,datetime.now())
            flash('This incident will be reported ','danger')
            return render_template('error.html',error=403)
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))

@app.route("/reset_mtech", methods=['GET', 'POST'])
@login_required
def reset_mtech():
    if current_user.is_active == True:
        if current_user.is_admin == True:
            conn = sqlite3.connect('portal/site.db') 
            c = conn.cursor()
            c.execute('''DELETE FROM mtech;''')
            c.execute('''DELETE FROM violations;''')
            conn.commit()
            conn.close()
            return redirect(url_for('mtech'))
        else:
            report=str(current_user.username)+'  tried to accessed unauthorized route -> MTech Reset '
            fillReport(report,current_user.username,datetime.now())
            flash('This incident will be reported ','danger')
            return render_template('error.html',error=403)
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
        return redirect(url_for('home'))
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
                return redirect(url_for('home'))
            return render_template('register.html', title='Register', form=form)
        else:
            flash('Admin account already exists','info')
            return redirect('home')
    else:
        render_template('error.html',error=404)




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
    return redirect(url_for('home'))

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
                pData()
            c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='mtech' ''')
            if c.fetchone()[0]==1 :
                check1=1
            else:
                mData()
            return redirect('dashboard')
        else:
            return redirect('workspace')
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))



def mData():
    conn = sqlite3.connect('portal/site.db') 
    c = conn.cursor()
    c.execute('''
        CREATE TABLE mtech (
            "Application Ref. No." INTEGER
        );''')
    c.execute('''ALTER TABLE mtech ADD Comment2 TEXT''')
    c.execute('''ALTER TABLE mtech ADD Submission2 TEXT DEFAULT "Pending" ''')
    c.execute('''ALTER TABLE mtech ADD Reject_Reason TEXT''')
    c.execute('''ALTER TABLE mtech ADD Validation TEXT DEFAULT "Pending" ''')
    c.execute('''ALTER TABLE mtech ADD Comment1 TEXT''')
    c.execute('''ALTER TABLE mtech ADD Submission1 TEXT DEFAULT "Pending" ''')
    c.execute('''ALTER TABLE mtech ADD Tutor1 TEXT DEFAULT "Not Assigned" ''')
    c.execute('''ALTER TABLE mtech ADD Tutor2 TEXT DEFAULT "Not Assigned" ''')
    c.execute('''ALTER TABLE mtech ADD alloc_status TEXT DEFAULT "0" ''')
    c.execute('''ALTER TABLE mtech ADD Application TEXT''')
    conn.commit()
    conn.close()
    return



def pData():
    conn = sqlite3.connect('portal/site.db') 
    c = conn.cursor()
    c.execute('''
        CREATE TABLE phd (
            "Application Ref. No." INTEGER
        );''')
    c.execute('''ALTER TABLE phd ADD Comment2 TEXT''')
    c.execute('''ALTER TABLE phd ADD Submission2 TEXT DEFAULT "Pending" ''')
    c.execute('''ALTER TABLE phd ADD Reject_Reason TEXT''')
    c.execute('''ALTER TABLE phd ADD Validation TEXT DEFAULT "Pending" ''')
    c.execute('''ALTER TABLE phd ADD Comment1 TEXT''')
    c.execute('''ALTER TABLE phd ADD Submission1 TEXT DEFAULT "Pending" ''')
    c.execute('''ALTER TABLE phd ADD Tutor1 TEXT DEFAULT "Not Assigned" ''')
    c.execute('''ALTER TABLE phd ADD Tutor2 TEXT DEFAULT "Not Assigned" ''')
    c.execute('''ALTER TABLE phd ADD alloc_status TEXT DEFAULT "0" ''')
    c.execute('''ALTER TABLE phd ADD Application TEXT''')
    c.execute('''update phd set Application = "Application Ref. No."; ''')
    conn.commit()
    conn.close()
    return

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



@app.route("/downloadpCsv")
@login_required
def downloadpCsv():
    if current_user.is_active == True:
        if current_user.is_admin == True or current_user.is_manager==True:
            conn = sqlite3.connect('portal/site.db') 
            c = conn.cursor()
            db_df=pd.read_sql_query("SELECT * FROM phd", conn)
            db_df=db_df.drop('alloc_status',1)
            db_df=db_df.drop('Submission1',1)
            db_df=db_df.drop('Submission2',1)
            db_df=db_df.drop('Comment2',1)
            db_df=db_df.drop('st1',1)
            db_df=db_df.drop('ft1',1)
            db_df=db_df.drop('st2',1)
            db_df=db_df.drop('ft2',1)
            db_df=db_df.drop('tt1',1)
            db_df=db_df.drop('tt2',1)
            db_df=db_df.drop('Reject_Reason',1)
            db_df=db_df.drop('Validation',1)
            db_df=db_df.drop('Application',1)
            db_df=db_df.drop('Comment1',1)
            db_df=db_df.drop('Tutor1',1)
            db_df=db_df.drop('Tutor2',1)
            db_df.to_csv('portal/static/Updated-phd.csv', index=False)
            flash('CSV exported successfully','success')
            return redirect('admin/fileadmin')
        else:
            return render_template('error.html',error=403)
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))


@app.route("/downloadmCsv")
@login_required
def downloadmCsv():
    if current_user.is_active == True:
        if current_user.is_admin == True or current_user.is_manager==True:
            conn = sqlite3.connect('portal/site.db') 
            c = conn.cursor()
            db_df=pd.read_sql_query("SELECT * FROM mtech", conn)
            db_df=db_df.drop('alloc_status',1)
            db_df=db_df.drop('Submission1',1)
            db_df=db_df.drop('Submission2',1)
            db_df=db_df.drop('Comment2',1)
            db_df=db_df.drop('st1',1)
            db_df=db_df.drop('ft1',1)
            db_df=db_df.drop('st2',1)
            db_df=db_df.drop('ft2',1)
            db_df=db_df.drop('tt1',1)
            db_df=db_df.drop('tt2',1)
            db_df=db_df.drop('Reject_Reason',1)
            db_df=db_df.drop('Validation',1)
            db_df=db_df.drop('Application',1)
            db_df=db_df.drop('Comment1',1)
            db_df=db_df.drop('Tutor1',1)
            db_df=db_df.drop('Tutor2',1)
            db_df.to_csv('portal/static/Updated-mtech.csv', index=False)
            flash('CSV exported successfully','success')
            return redirect('admin/fileadmin/')
        else:
            return render_template('error.html',error=403)
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))




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


@app.route("/phd")
@login_required
def phd():
    if current_user.is_active == True:
        user=User.query.all()
        conn = sqlite3.connect('portal/site.db') 
        c = conn.cursor()
        test=c.execute('''SELECT * FROM phd''').fetchall()
        t=c.execute('''PRAGMA table_info('phd')''').fetchall()
        if (len(test)):
            length=len(test[0])
        else:
            length=0
        test=[tup[::-1] for tup in test] 
        t.reverse()
        image_file = url_for('static',filename='assets/img/faces/' + current_user.image_file)
        conn.close()
        if current_user.is_admin==True or current_user.is_manager == True:
            return render_template('phd_admin.html', title='Phd',user=user,image_file=image_file,phd=test,t=t,length=length)
        else:
            return render_template('phd_ta.html', title='Phd',user=user,image_file=image_file,phd=test,t=t,length=length)
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))


@app.route("/mtech")
@login_required
def mtech():
    if current_user.is_active == True:
        user=User.query.all()
        conn = sqlite3.connect('portal/site.db') 
        c = conn.cursor()
        test=c.execute('''SELECT * FROM mtech''').fetchall()
        t=c.execute('''PRAGMA table_info('mtech')''').fetchall()
        if (len(test)):
            length=len(test[0])
        else:
            length=0
        test=[tup[::-1] for tup in test] 
        t.reverse()
        image_file = url_for('static',filename='assets/img/faces/' + current_user.image_file)
        conn.close()
        if current_user.is_admin==True or current_user.is_manager == True:
            return render_template('mtech_admin.html', title='M.TECH',user=user,image_file=image_file,mtech=test,t=t,length=length)
        else:
            return render_template('mtech_ta.html', title='M.TECH',user=user,image_file=image_file,mtech=test,t=t,length=length)
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


@app.route('/lab_phd/<application>')
@login_required
def lab_phd(application):
    if current_user.is_active == True:
        image_file = url_for('static',filename='assets/img/faces/' + current_user.image_file)
        conn = sqlite3.connect('portal/site.db') 
        c = conn.cursor()
        test=c.execute('''SELECT * FROM phd''').fetchall()
        t=c.execute('''PRAGMA table_info('phd')''').fetchall()
        if (len(test)):
            length=len(test[0])
        else:
            length=0
        test=[tup[::-1] for tup in test] 
        t.reverse()
        for p in test:
            if p[0]==application:
                if p[4] != 'Done':
                    flash('This file has not yet been submitted by TA', 'danger')
                    return render_template('lab_phd.html',image_file=image_file,title='Lab',cand=p,t=t,length=length)
                else:
                    return render_template('lab_phd.html',image_file=image_file,title='Lab',cand=p,t=t,length=length)
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))

@app.route('/lab_mtech/<application>')
@login_required
def lab_mtech(application):
    if current_user.is_active == True:
        image_file = url_for('static',filename='assets/img/faces/' + current_user.image_file)
        conn = sqlite3.connect('portal/site.db') 
        c = conn.cursor()
        test=c.execute('''SELECT * FROM mtech''').fetchall()
        t=c.execute('''PRAGMA table_info('mtech')''').fetchall()
        if (len(test)):
            length=len(test[0])
        else:
            length=0
        test=[tup[::-1] for tup in test] 
        t.reverse()
        for p in test:
            if p[0]==application:
                if p[4] != 'Done':
                    flash('This file has not yet been submitted by TA', 'danger')
                    return render_template('lab_mtech.html',image_file=image_file,title='Lab',cand=p,t=t,length=length)
                else:
                    return render_template('lab_mtech.html',image_file=image_file,title='Lab',cand=p,t=t,length=length)
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))


@app.route('/ta_lab_phd/<application>')
@login_required
def ta_lab_phd(application):
    if current_user.is_active == True:
        conn = sqlite3.connect('portal/site.db') 
        c = conn.cursor()
        test=c.execute('''SELECT * FROM phd''').fetchall()
        t=c.execute('''PRAGMA table_info('phd')''').fetchall()
        if (len(test)):
            length=len(test[0])
        else:
            length=0
        test=[tup[::-1] for tup in test] 
        t.reverse()
        image_file = url_for('static',filename='assets/img/faces/' + current_user.image_file)
        for p in test:
            if p[0]==application:
                if current_user.username==p[3]:
                    if p[10] == 'None':
                        c.execute("update phd set st1 = ? WHERE Application = ?",(datetime.now(),application))
                        conn.commit()
                else:
                    if p[12] == 'None':
                        c.execute("update phd set st2 = ? WHERE Application = ?",(datetime.now(),application))
                        conn.commit()
                return render_template('ta_lab_phd.html',image_file=image_file,title='Lab',cand=p,t=t,length=length)
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))


@app.route('/ta_lab_mtech/<application>')
@login_required
def ta_lab_mtech(application):
    if current_user.is_active == True:
        conn = sqlite3.connect('portal/site.db') 
        c = conn.cursor()
        test=c.execute('''SELECT * FROM mtech''').fetchall()
        t=c.execute('''PRAGMA table_info('mtech')''').fetchall()
        if (len(test)):
            length=len(test[0])
        else:
            length=0
        test=[tup[::-1] for tup in test] 
        t.reverse()
        image_file = url_for('static',filename='assets/img/faces/' + current_user.image_file)
        for p in test:
            if p[0]==application:
                return render_template('ta_lab_mtech.html',image_file=image_file,title='Lab',cand=p,t=t,length=length)
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))


@app.route('/send_phd1/<application>')
@login_required
def send_phd1(application):
    if current_user.is_active == True:
        conn = sqlite3.connect('portal/site.db') 
        c = conn.cursor()
        test=c.execute('''SELECT * FROM phd''').fetchall()   
        test=[tup[::-1] for tup in test] 
        test = [list(ele) for ele in test]         
        def too(test):
            flag=0
            for p in test:
                if p[0]==application:
                    if p[3] == current_user.username:
                        c.execute("update phd set ft1 = ? WHERE Application = ?",(datetime.now(),application))
                        conn.commit()
                        filltime1(application)
                        c.execute('''update phd set Submission1 = "Done" WHERE Application = "'''+application+'''";''')
                        conn.commit()
                        c.execute('''update phd set Validation = "Pending" WHERE Application = "'''+application+'''";''')
                        conn.commit()
                        c.execute('''update phd set Reject_Reason = "None" WHERE Application = "'''+application+'''";''')
                        conn.commit()
                        flag=1
                        flash('File submitted successfully ','success')
                        break
                    else:
                        report=str(current_user.username)+'  tried to submit an unassigned file = '+str(application)
                        fillReport(report,current_user.username,datetime.now())
                        flag=1
                        flash('This incident will be reported ','danger')
                        break
            if flag==0:
                flash('No such file exist','danger')
        too(test)
        return redirect('phd')
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))


def filltime1(application):
    conn = sqlite3.connect('portal/site.db') 
    c = conn.cursor()
    test=c.execute('''SELECT * FROM phd''').fetchall()   
    test=[tup[::-1] for tup in test] 
    test = [list(ele) for ele in test]
    for p in test:
        if p[0]==application:
            t1=p[10]
            t2=p[11]
            t3=datetime.strptime(t1,'%Y-%m-%d %H:%M:%S.%f')
            t4=datetime.strptime(t2,'%Y-%m-%d %H:%M:%S.%f')
            diff=t4-t3
            c.execute("update phd set tt1 = ? WHERE Application = ?",(diff.seconds,application))
            conn.commit()

def filltime2(application):
    conn = sqlite3.connect('portal/site.db') 
    c = conn.cursor()
    test=c.execute('''SELECT * FROM phd''').fetchall()   
    test=[tup[::-1] for tup in test] 
    test = [list(ele) for ele in test]
    for p in test:
        if p[0]==application:
            t1=p[12]
            t2=p[13]
            t3=datetime.strptime(t1,'%Y-%m-%d %H:%M:%S.%f')
            t4=datetime.strptime(t2,'%Y-%m-%d %H:%M:%S.%f')
            diff=t4-t3
            c.execute("update phd set tt2 = ? WHERE Application = ?",(diff.seconds,application))
            conn.commit()




@app.route('/send_phd2/<application>')
@login_required
def send_phd2(application):
    if current_user.is_active == True:
        conn = sqlite3.connect('portal/site.db') 
        c = conn.cursor()
        test=c.execute('''SELECT * FROM phd''').fetchall()   
        test=[tup[::-1] for tup in test] 
        test = [list(ele) for ele in test]         
        def too(test):
            flag=0
            for p in test:
                if p[0]==application:
                    if  p[2] == current_user.username:
                        c.execute("update phd set ft2 = ? WHERE Application = ?",(datetime.now(),application))
                        conn.commit()
                        filltime2(application)
                        c.execute('''update phd set Submission2 = "Done" WHERE Application = "'''+application+'''";''')
                        conn.commit()
                        c.execute('''update phd set Validation = "Pending" WHERE Application = "'''+application+'''";''')
                        conn.commit()
                        c.execute('''update phd set Reject_Reason = "None" WHERE Application = "'''+application+'''";''')
                        conn.commit()
                        flag=1
                        flash('File submitted successfully ','success')
                        break
                    else:
                        report=str(current_user.username)+'  tried to submit an unassigned file = '+str(application)
                        fillReport(report,current_user.username,datetime.now())
                        flag=1
                        flash('This incident will be reported ','danger')
                        break
            if flag==0:
                flash('No such file exist','danger')
        too(test)
        return redirect('phd')
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))



@app.route('/send_mtech1/<application>')
@login_required
def send_mtech1(application):
    if current_user.is_active == True:
        conn = sqlite3.connect('portal/site.db') 
        c = conn.cursor()
        test=c.execute('''SELECT * FROM mtech''').fetchall()   
        test=[tup[::-1] for tup in test] 
        test = [list(ele) for ele in test]         
        def too(test):
            flag=0
            for p in test:
                if p[0]==application:
                    if p[3] == current_user.username or p[2] == current_user.username:
                        c.execute('''update mtech set Submission1 = "Done" WHERE Application = "'''+application+'''";''')
                        conn.commit()
                        c.execute('''update mtech set Validation = "Pending" WHERE Application = "'''+application+'''";''')
                        conn.commit()
                        c.execute('''update mtech set Reject_Reason = "None" WHERE Application = "'''+application+'''";''')
                        conn.commit()
                        flag=1
                        flash('File submitted successfully ','success')
                        break
                    else:
                        report=str(current_user.username)+'  tried to submit an unassigned file = '+str(application)
                        fillReport(report,current_user.username,datetime.now())
                        flag=1
                        flash('This incident will be reported ','danger')
                        break
            if flag==0:
                flash('No such file exist','danger')
        too(test)
        return redirect('mtech')
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))


@app.route('/send_mtech2/<application>')
@login_required
def send_mtech2(application):
    if current_user.is_active == True:
        conn = sqlite3.connect('portal/site.db') 
        c = conn.cursor()
        test=c.execute('''SELECT * FROM mtech''').fetchall()   
        test=[tup[::-1] for tup in test] 
        test = [list(ele) for ele in test]         
        def too(test):
            flag=0
            for p in test:
                if p[0]==application:
                    if p[3] == current_user.username or p[2] == current_user.username:
                        c.execute('''update mtech set Submission2 = "Done" WHERE Application = "'''+application+'''";''')
                        conn.commit()
                        c.execute('''update mtech set Validation = "Pending" WHERE Application = "'''+application+'''";''')
                        conn.commit()
                        c.execute('''update mtech set Reject_Reason = "None" WHERE Application = "'''+application+'''";''')
                        conn.commit()
                        flag=1
                        flash('File submitted successfully ','success')
                        break
                    else:
                        report=str(current_user.username)+'  tried to submit an unassigned file = '+str(application)
                        fillReport(report,current_user.username,datetime.now())
                        flag=1
                        flash('This incident will be reported ','danger')
                        break
            if flag==0:
                flash('No such file exist','danger')
        too(test)
        return redirect('mtech')
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))



@app.route('/verify_phd/<application>')
@login_required
def verify_phd(application):
    if current_user.is_active == True:
        if current_user.is_admin==True or current_user.is_manager == True:
            conn = sqlite3.connect('portal/site.db') 
            c = conn.cursor()
            test=c.execute('''SELECT * FROM phd''').fetchall()   
            test=[tup[::-1] for tup in test] 
            test = [list(ele) for ele in test]         
            def too(test):
                for p in test:
                    if p[0] == application:
                        c.execute('''update phd set Validation = "Done" WHERE Application = "'''+application+'''";''')
                        conn.commit()
                        if p[4] == 'Done':
                            flash('File verified successfully','success')
                        else:
                            flash("You have a verified non submitted file",'info')
                        break
            too(test)
            return redirect('dashboard')
        else:
            report=str(current_user.username)+'  tried to submit an unassigned file = '+str(application)
            fillReport(report,current_user.username,datetime.now())
            flash('This incident will be reported','danger')
            return render_template('error.html',error=403)
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))


@app.route('/verify_mtech/<application>')
@login_required
def verify_mtech(application):
    if current_user.is_active == True:
        if current_user.is_admin==True or current_user.is_manager == True:
            conn = sqlite3.connect('portal/site.db') 
            c = conn.cursor()
            test=c.execute('''SELECT * FROM mtech''').fetchall()   
            test=[tup[::-1] for tup in test] 
            test = [list(ele) for ele in test]         
            def too(test):
                for p in test:
                    if p[0] == application:
                        c.execute('''update mtech set Validation = "Done" WHERE Application = "'''+application+'''";''')
                        conn.commit()
                        if p[4] == 'Done':
                            flash('File verified successfully','success')
                        else:
                            flash("You have a verified non submitted file",'info')
                        break
            too(test)
            return redirect('dashboard')
        else:
            report=str(current_user.username)+'  tried to submit an unassigned file = '+str(application)
            fillReport(report,current_user.username,datetime.now())
            flash('This incident will be reported','danger')
            return render_template('error.html',error=403)
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))




@app.route('/comment_phd1/<application>', methods=['GET', 'POST'])
@login_required
def comment_phd1(application):
    if current_user.is_active == True:
        conn = sqlite3.connect('portal/site.db') 
        c = conn.cursor()
        test=c.execute('''SELECT * FROM phd''').fetchall()   
        test=[tup[::-1] for tup in test] 
        test = [list(ele) for ele in test]         
        def too(test):
            for p in test:
                if p[0]==application:
                    if p[3] == current_user.username or p[2] == current_user.username:
                        c.execute('''update phd set Comment1 = "'''+request.form['comment']+'''" WHERE Application = "'''+application+'''";''')
                        conn.commit()
                        flash('Comment added successfully', 'info')
                        break
                    else:
                        report=str(current_user.username)+'  tried to add comment an unassigned file = '+str(application)
                        fillReport(report,current_user.username,datetime.now())
                        flash('This incident will be reported ','danger')
                        break
        too(test)
        return redirect(url_for('ta_lab_phd',application=application))
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))



@app.route('/comment_phd2/<application>', methods=['GET', 'POST'])
@login_required
def comment_phd2(application):
    if current_user.is_active == True:
        conn = sqlite3.connect('portal/site.db') 
        c = conn.cursor()
        test=c.execute('''SELECT * FROM phd''').fetchall()   
        test=[tup[::-1] for tup in test] 
        test = [list(ele) for ele in test]         
        def too(test):
            for p in test:
                if p[0]==application:
                    if p[3] == current_user.username or p[2] == current_user.username:
                        c.execute('''update phd set Comment2 = "'''+request.form['comment']+'''" WHERE Application = "'''+application+'''";''')
                        conn.commit()
                        flash('Comment added successfully', 'info')
                        break
                    else:
                        report=str(current_user.username)+'  tried to add comment an unassigned file = '+str(application)
                        fillReport(report,current_user.username,datetime.now())
                        flash('This incident will be reported ','danger')
                        break
        too(test)
        return redirect(url_for('ta_lab_phd',application=application))
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))



@app.route('/comment_mtech1/<application>', methods=['GET', 'POST'])
@login_required
def comment_mtech1(application):
    if current_user.is_active == True:
        conn = sqlite3.connect('portal/site.db') 
        c = conn.cursor()
        test=c.execute('''SELECT * FROM mtech''').fetchall()   
        test=[tup[::-1] for tup in test] 
        test = [list(ele) for ele in test]         
        def too(test):
            for p in test:
                if p[0]==application:
                    if p[3] == current_user.username or p[2] == current_user.username:
                        c.execute('''update mtech set Comment1 = "'''+request.form['comment']+'''" WHERE Application = "'''+application+'''";''')
                        conn.commit()
                        flash('Comment added successfully', 'info')
                        break
                    else:
                        report=str(current_user.username)+'  tried to add comment an unassigned file = '+str(application)
                        fillReport(report,current_user.username,datetime.now())
                        flash('This incident will be reported ','danger')
                        break
        too(test)
        return redirect(url_for('ta_lab_mtech',application=application))
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))



@app.route('/comment_mtech2/<application>', methods=['GET', 'POST'])
@login_required
def comment_mtech2(application):
    if current_user.is_active == True:
        conn = sqlite3.connect('portal/site.db') 
        c = conn.cursor()
        test=c.execute('''SELECT * FROM mtech''').fetchall()   
        test=[tup[::-1] for tup in test] 
        test = [list(ele) for ele in test]         
        def too(test):
            for p in test:
                if p[0]==application:
                    if p[3] == current_user.username or p[2] == current_user.username:
                        c.execute('''update mtech set Comment2 = "'''+request.form['comment']+'''" WHERE Application = "'''+application+'''";''')
                        conn.commit()
                        flash('Comment added successfully', 'info')
                        break
                    else:
                        report=str(current_user.username)+'  tried to add comment an unassigned file = '+str(application)
                        fillReport(report,current_user.username,datetime.now())
                        flash('This incident will be reported ','danger')
                        break
        too(test)
        return redirect(url_for('ta_lab_mtech',application=application))
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))



@app.route('/edit_phd/<application>/<key>', methods=['GET', 'POST'])
@login_required
def edit_phd(application,key):
    if current_user.is_active == True:
        if current_user.is_manager==True or current_user.is_admin==True:
            conn = sqlite3.connect('portal/site.db') 
            c = conn.cursor()
            test=c.execute('''SELECT * FROM phd''').fetchall()  
            t=c.execute('''PRAGMA table_info('phd')''').fetchall()
            t.reverse() 
            test=[tup[::-1] for tup in test] 
            test = [list(ele) for ele in test]         
            def too(test):
                var=key
                c.execute("update phd set '"+var+"' = ? WHERE Application = ?",(request.form[var],application))
                conn.commit() 
                flash('Updated '+var,'success')        
            too(test)
            return redirect(url_for('lab_phd',application=application))
        else:
            report=str(current_user.username)+'  tried to submit an unassigned file = '+str(application)
            fillReport(report,current_user.username,datetime.now())
            flash('This incident will be reported ','danger')
    else:
        return redirect(url_for('logout'))


@app.route('/edit_mtech/<application>/<key>', methods=['GET', 'POST'])
@login_required
def edit_mtech(application,key):
    if current_user.is_active == True:
        if current_user.is_manager==True or current_user.is_admin==True:
            conn = sqlite3.connect('portal/site.db') 
            c = conn.cursor()
            test=c.execute('''SELECT * FROM mtech''').fetchall()  
            t=c.execute('''PRAGMA table_info('mtech')''').fetchall()
            t.reverse() 
            test=[tup[::-1] for tup in test] 
            test = [list(ele) for ele in test]         
            def too(test):
                var=key
                c.execute("update mtech set '"+var+"' = ? WHERE Application = ?",(request.form[var],application))
                conn.commit() 
                flash('Updated '+var,'success')        
            too(test)
            return redirect(url_for('lab_mtech',application=application))
        else:
            report=str(current_user.username)+'  tried to submit an unassigned file = '+str(application)
            fillReport(report,current_user.username,datetime.now())
            flash('This incident will be reported ','danger')
    else:
        return redirect(url_for('logout'))



@app.route('/reject_phd/<application>', methods=['GET', 'POST'])
@login_required
def reject_phd(application):
    if current_user.is_active == True:
        if current_user.is_admin == True or current_user.is_manager==True:
            conn = sqlite3.connect('portal/site.db') 
            c = conn.cursor()
            test=c.execute('''SELECT * FROM phd''').fetchall()   
            test=[tup[::-1] for tup in test] 
            test = [list(ele) for ele in test]         
            def too(test):
                for p in test:
                    if p[0]==application:
                        c.execute('''update phd set Reject_Reason = "'''+request.form['msg']+'''" WHERE Application = "'''+application+'''";''')
                        conn.commit()
                        c.execute('''update phd set Submission1 = "Pending" WHERE Application = "'''+application+'''";''')
                        conn.commit()
                        c.execute('''update phd set Submission2 = "Pending" WHERE Application = "'''+application+'''";''')
                        conn.commit()
                        c.execute('''update phd set Validation = "Rejected" WHERE Application = "'''+application+'''";''')
                        conn.commit()
                        flash('TA notified successfully', 'info')
                        break
            too(test)
            return redirect(url_for('dashboard'))
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))

@app.route('/reject_mtech/<application>', methods=['GET', 'POST'])
@login_required
def reject_mtech(application):
    if current_user.is_active == True:
        if current_user.is_admin == True or current_user.is_manager==True:
            conn = sqlite3.connect('portal/site.db') 
            c = conn.cursor()
            test=c.execute('''SELECT * FROM mtech''').fetchall()   
            test=[tup[::-1] for tup in test] 
            test = [list(ele) for ele in test]         
            def too(test):
                for p in test:
                    if p[0]==application:
                        c.execute('''update mtech set Reject_Reason = "'''+request.form['msg']+'''" WHERE Application = "'''+application+'''";''')
                        conn.commit()
                        c.execute('''update mtech set Submission = "Pending" WHERE Application = "'''+application+'''";''')
                        conn.commit()
                        c.execute('''update mtech set Validation = "Rejected" WHERE Application = "'''+application+'''";''')
                        conn.commit()
                        flash('TA notified successfully', 'info')
                        break
            too(test)
            return redirect(url_for('dashboard'))
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))

@app.route('/change_phd1/<application>', methods=['GET', 'POST'])
@login_required
def change_phd1(application):
    if current_user.is_active == True:
        conn = sqlite3.connect('portal/site.db') 
        c = conn.cursor()
        test=c.execute('''SELECT * FROM phd''').fetchall()   
        test=[tup[::-1] for tup in test] 
        test = [list(ele) for ele in test]         
        def too(test):
            for p in test:
                if p[0]==application:
                    if current_user.is_admin==True or current_user.is_manager==True:
                        c.execute('''update phd set Tutor1 = "'''+request.form['tutor1']+'''" WHERE Application = "'''+application+'''";''')
                        conn.commit()
                        flash('Tutor changed successfully', 'success')
                        break
                    else:
                        report=str(current_user.username)+'  tried to reasign Tutor = '+str(application)
                        fillReport(report,current_user.username,datetime.now())
                        flash('This incident will be reported ','danger')
                        break
        too(test)
        return redirect(url_for('phd'))
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))



@app.route('/change_phd2/<application>', methods=['GET', 'POST'])
@login_required
def change_phd2(application):
    if current_user.is_active == True:
        conn = sqlite3.connect('portal/site.db') 
        c = conn.cursor()
        test=c.execute('''SELECT * FROM phd''').fetchall()   
        test=[tup[::-1] for tup in test] 
        test = [list(ele) for ele in test]         
        def too(test):
            for p in test:
                if p[0]==application:
                    if current_user.is_admin==True or current_user.is_manager==True:
                        c.execute('''update phd set Tutor2 = "'''+request.form['tutor2']+'''" WHERE Application = "'''+application+'''";''')
                        conn.commit()
                        flash('Tutor changed successfully', 'success')
                        break
                    else:
                        report=str(current_user.username)+'  tried to reasign Tutor = '+str(application)
                        fillReport(report,current_user.username,datetime.now())
                        flash('This incident will be reported ','danger')
                        break
        too(test)
        return redirect(url_for('phd'))
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))


@app.route('/change_mtech1/<application>', methods=['GET', 'POST'])
@login_required
def change_mtech1(application):
    if current_user.is_active == True:
        conn = sqlite3.connect('portal/site.db') 
        c = conn.cursor()
        test=c.execute('''SELECT * FROM mtech''').fetchall()   
        test=[tup[::-1] for tup in test] 
        test = [list(ele) for ele in test]         
        def too(test):
            for p in test:
                if p[0]==application:
                    if current_user.is_admin==True or current_user.is_manager==True:
                        c.execute('''update mtech set Tutor1 = "'''+request.form['tutor1']+'''" WHERE Application = "'''+application+'''";''')
                        conn.commit()
                        flash('Tutor changed successfully', 'success')
                        break
                    else:
                        report=str(current_user.username)+'  tried to reasign Tutor = '+str(application)
                        fillReport(report,current_user.username,datetime.now())
                        flash('This incident will be reported ','danger')
                        break
        too(test)
        return redirect(url_for('mtech'))
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))



@app.route('/change_mtech2/<application>', methods=['GET', 'POST'])
@login_required
def change_mtech2(application):
    if current_user.is_active == True:
        conn = sqlite3.connect('portal/site.db') 
        c = conn.cursor()
        test=c.execute('''SELECT * FROM mtech''').fetchall()   
        test=[tup[::-1] for tup in test] 
        test = [list(ele) for ele in test]         
        def too(test):
            for p in test:
                if p[0]==application:
                    if current_user.is_admin==True or current_user.is_manager==True:
                        c.execute('''update mtech set Tutor2 = "'''+request.form['tutor2']+'''" WHERE Application = "'''+application+'''";''')
                        conn.commit()
                        flash('Tutor changed successfully', 'success')
                        break
                    else:
                        report=str(current_user.username)+'  tried to reasign Tutor = '+str(application)
                        fillReport(report,current_user.username,datetime.now())
                        flash('This incident will be reported ','danger')
                        break
        too(test)
        return redirect(url_for('mtech'))
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
        return redirect(url_for('home'))
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
        return redirect(url_for('home'))
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


