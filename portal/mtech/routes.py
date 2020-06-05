from flask import Flask,abort, session, render_template, url_for, flash, redirect, request,send_file, Blueprint
from portal import app, db
from portal.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
import os 
import json
from os import path
import pandas as pd
import sqlite3
from datetime import datetime ,date ,timedelta


mtechs=Blueprint('mtechs',__name__,template_folder='templates')



@mtechs.route("/allocate_mtech", methods=['GET', 'POST'])
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
                if user_val==0:
                    flash('No Tutor exists','danger')
                else:
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
                    flash("mtech files allocated successfully","success")
            foo(user,test)
            return redirect(url_for('mtechs.mtech'))
        else:
            report=str(current_user.username)+'  tried to accessed unauthorized route -> allocate_mtech '
            fillReport(report,current_user.username,datetime.now())
            return render_template('error.html',error=404)
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))





@mtechs.route("/mtechcsv", methods=['GET', 'POST'])
@login_required
def mtechcsv():
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
            c.execute('''ALTER TABLE mtech ADD tt2 DATE  DEFAULT "None"''')  #15
            c.execute('''ALTER TABLE mtech ADD tt1 DATE DEFAULT "None"''')   #14
            c.execute('''ALTER TABLE mtech ADD ft2 DATE  DEFAULT "None"''')   #13
            c.execute('''ALTER TABLE mtech ADD st2 DATE DEFAULT "None"''')   #12
            c.execute('''ALTER TABLE mtech ADD ft1 DATE DEFAULT "None"''')   #11
            c.execute('''ALTER TABLE mtech ADD st1 DATE DEFAULT "None"''')   #10
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




@mtechs.route("/reset_mtech", methods=['GET', 'POST'])
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
            return redirect(url_for('mtechs.mtech'))
        else:
            report=str(current_user.username)+'  tried to accessed unauthorized route -> mtech Reset '
            fillReport(report,current_user.username,datetime.now())
            flash('This incident will be reported ','danger')
            return render_template('error.html',error=403)
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))





@mtechs.route("/downloadmtechCsv")
@login_required
def downloadmtechCsv():
    if current_user.is_active == True:
        if current_user.is_admin == True or current_user.is_manager==True:
            conn = sqlite3.connect('portal/site.db') 
            c = conn.cursor()
            db_df=pd.read_sql_query("SELECT * FROM mtech", conn)
            db_df=db_df.drop('alloc_status',1)
            db_df=db_df.drop('Submission1',1)
            db_df=db_df.drop('Submission2',1)
            db_df=db_df.drop('Comment2',1)
            if 'st1' in db_df.columns:
                db_df=db_df.drop('st1',1)
            if 'ft1' in db_df.columns:
                db_df=db_df.drop('ft1',1)
            if 'st2' in db_df.columns:
                db_df=db_df.drop('st2',1)
            if 'ft2' in db_df.columns:
                db_df=db_df.drop('ft2',1)
            if 'tt1' in db_df.columns:
                db_df=db_df.drop('tt1',1)
            if 'tt2' in db_df.columns:
                db_df=db_df.drop('tt2',1)
            db_df=db_df.drop('Reject_Reason',1)
            db_df=db_df.drop('Validation',1)
            db_df=db_df.drop('Application',1)
            db_df=db_df.drop('Comment1',1)
            db_df=db_df.drop('Tutor1',1)
            db_df=db_df.drop('Tutor2',1)
            db_df.to_csv('portal/static/Updated-CSV/Updated-mtech.csv', index=False)
            p="static/Updated-CSV/Updated-mtech.csv"
            return send_file(p,as_attachment=True)
        else:
            return render_template('error.html',error=403)
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))


@mtechs.route("/mtech")
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
            return render_template('mtech_admin.html', title='mtech',user=user,image_file=image_file,mtech=test,t=t,length=length)
        else:
            return render_template('mtech_ta.html', title='mtech',user=user,image_file=image_file,mtech=test,t=t,length=length)
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))



@mtechs.route('/lab_mtech/<application>')
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


@mtechs.route('/ta_lab_mtech/<application>')
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
                if current_user.username==p[3]:
                    if p[10] == 'None':
                        c.execute("update mtech set st1 = ? WHERE Application = ?",(datetime.now(),application))
                        conn.commit()
                else:
                    if p[12] == 'None':
                        c.execute("update mtech set st2 = ? WHERE Application = ?",(datetime.now(),application))
                        conn.commit()
                return render_template('ta_lab_mtech.html',image_file=image_file,title='Lab',cand=p,t=t,length=length)
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))


@mtechs.route('/send_mtech1/<application>')
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
                    if p[3] == current_user.username:
                        c.execute("update mtech set ft1 = ? WHERE Application = ?",(datetime.now(),application))
                        conn.commit()
                        filltime1(application)
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
        return redirect(url_for('mtechs.mtech'))
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))



@mtechs.route('/send_mtech2/<application>')
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
                    if  p[2] == current_user.username:
                        c.execute("update mtech set ft2 = ? WHERE Application = ?",(datetime.now(),application))
                        conn.commit()
                        filltime2(application)
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
        too(test)
        return redirect(url_for('mtechs.mtech'))
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))


@mtechs.route('/verify_mtech/<application>')
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
            return redirect(url_for('dashboard'))
        else:
            report=str(current_user.username)+'  tried to submit an unassigned file = '+str(application)
            fillReport(report,current_user.username,datetime.now())
            flash('This incident will be reported','danger')
            return render_template('error.html',error=403)
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))



@mtechs.route('/comment_mtech1/<application>', methods=['GET', 'POST'])
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
        return redirect(url_for('mtechs.ta_lab_mtech',application=application))
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))


@mtechs.route('/comment_mtech2/<application>', methods=['GET', 'POST'])
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
        return redirect(url_for('mtechs.ta_lab_mtech',application=application))
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))



@mtechs.route('/edit_mtech/<application>/<key>', methods=['GET', 'POST'])
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
            return redirect(url_for('mtechs.lab_mtech',application=application))
        else:
            report=str(current_user.username)+'  tried to submit an unassigned file = '+str(application)
            fillReport(report,current_user.username,datetime.now())
            flash('This incident will be reported ','danger')
    else:
        return redirect(url_for('logout'))


@mtechs.route('/reject_mtech/<application>', methods=['GET', 'POST'])
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
                        c.execute('''update mtech set Submission1 = "Pending" WHERE Application = "'''+application+'''";''')
                        conn.commit()
                        c.execute('''update mtech set Submission2 = "Pending" WHERE Application = "'''+application+'''";''')
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


@mtechs.route('/change_mtech1/<application>', methods=['GET', 'POST'])
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
        return redirect(url_for('mtechs.mtech'))
    else:
        flash('Your account has been deactivated by administrator','danger')
        return redirect(url_for('logout'))



@mtechs.route('/change_mtech2/<application>', methods=['GET', 'POST'])
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
        return redirect(url_for('mtechs.mtech'))
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



def filltime1(application):
    conn = sqlite3.connect('portal/site.db') 
    c = conn.cursor()
    test=c.execute('''SELECT * FROM mtech''').fetchall()   
    test=[tup[::-1] for tup in test] 
    test = [list(ele) for ele in test]
    for p in test:
        if p[0]==application:
            t1=p[10]
            t2=p[11]
            t3=datetime.strptime(t1,'%Y-%m-%d %H:%M:%S.%f')
            t4=datetime.strptime(t2,'%Y-%m-%d %H:%M:%S.%f')
            diff=t4-t3
            c.execute("update mtech set tt1 = ? WHERE Application = ?",(diff.seconds,application))
            conn.commit()

def filltime2(application):
    conn = sqlite3.connect('portal/site.db') 
    c = conn.cursor()
    test=c.execute('''SELECT * FROM mtech''').fetchall()   
    test=[tup[::-1] for tup in test] 
    test = [list(ele) for ele in test]
    for p in test:
        if p[0]==application:
            t1=p[12]
            t2=p[13]
            t3=datetime.strptime(t1,'%Y-%m-%d %H:%M:%S.%f')
            t4=datetime.strptime(t2,'%Y-%m-%d %H:%M:%S.%f')
            diff=t4-t3
            c.execute("update mtech set tt2 = ? WHERE Application = ?",(diff.seconds,application))
            conn.commit()



def fillReport(msg,usr,dt):
    conn = sqlite3.connect('portal/site.db') 
    c = conn.cursor()
    c.execute("INSERT INTO violations (Report,User,Date) VALUES (?,?,?) ",(msg,usr,dt))
    conn.commit()
    conn.close()
    return
