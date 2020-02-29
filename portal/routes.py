from flask import Flask, render_template, url_for, flash, redirect, request
from portal import app, db, bcrypt,mail
from portal.forms import RegistrationForm, LoginForm,PostForm,RequestResetForm,ResetPasswordForm
from portal.models import User, Post,phd
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import os 
import json
from os.path import join, dirname, realpath
from flask_uploads import UploadSet, configure_uploads, ALL
from sqlalchemy.sql.functions import func
phds=db.session.query(phd).all()
# mtechs=db.session.query(mtech).all()
from sqlalchemy import update
import pandas as pd

@app.route("/allocate_phd", methods=['GET', 'POST'])
@login_required
def allocate_phd():
    if current_user.is_admin == True:
        user=User.query.all()
        def foo(user,phds):
            i=0
            user_val=0
            phd_val=0
            flag1=1
            for x in user:
                if x.is_admin == False and x.is_manager == False:
                    user_val=user_val+1
            for pd in phds:
                phd_val=phd_val+1
            quotient = phd_val//user_val
            remainder = phd_val%user_val
            for u in user:
                flag1=1
                if u.is_admin==False and u.is_manager==False:
                    for p in phds:
                        if i==quotient:
                            if remainder > 0 :
                                flag1=0
                                if p.alloc_status=='0':
                                    p.Tutor_name=u.username
                                    p.alloc_status='1'
                                    db.session.merge(p)
                                    db.session.flush()
                                    db.session.commit()
                                    remainder =remainder - 1
                                    flag1=1
                            if flag1 == 1:
                                i=0
                                break
                        if i<quotient and p.alloc_status=='0':
                            p.Tutor_name=u.username
                            p.alloc_status ='1'
                            db.session.merge(p)
                            db.session.flush()
                            db.session.commit()
                            i=i+1
        foo(user,phds)
        return redirect(url_for('phd'))
    else:
        return render_template('error.html')



@app.route("/csv", methods=['GET', 'POST'])
@login_required
def csv():
    if current_user.is_admin == True:
        df=pd.read_csv('portal/mtech.csv')
        df.to_sql(name='mtech',con=db.engine,if_exists='replace')
        return redirect(url_for('phd'))
    else:
        return render_template('error.html')




UPLOAD_FOLDER = 'portal/static/pdf/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if current_user.is_admin == True:
        user=User.query.all()
        image_file = url_for('static',filename='faces/' + current_user.image_file)
        if request.method == 'POST' and 'file' in request.files:
            files = request.files.getlist("file")
            i=0
            for file in files:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
                i=i+1
            flash(str(i) +' files uploaded successfully ', 'info')
        return render_template('upload.html',title='Uploads',image_file=image_file,user=user,phd=phds)
    else:
        return render_template('error.html')

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
            return redirect(next_page) if next_page else redirect(url_for('workspace'))
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
    if current_user.is_admin == True:
        user=User.query.all()
        image_file = url_for('static',filename='faces/' + current_user.image_file)
        i=0
        for p in phds:
            i=i+1
        return render_template('dashboard.html', title='Dashboard',image_file=image_file,phd=phds,user=user,i=i)
    else:
        return render_template('error.html')


@app.route("/calendar")
@login_required
def calendar():
    if current_user.is_admin == True or current_user.is_manager == True:
        image_file = url_for('static',filename='faces/' + current_user.image_file)
        return render_template('calendar.html', title='Calendar',image_file=image_file)
    else:
        return render_template('error.html')

@app.route("/profile")
@login_required
def profile():
    image_file = url_for('static',filename='faces/' + current_user.image_file)
    return render_template('profile.html', title='Profile',image_file=image_file)

@app.route("/workspace")
@login_required
def workspace():
    user=User.query.all()
    # path=join(dirname(realpath(__file__)), 'static/pdf/')
    # a=os.listdir(path)
    # text=json.dumps(sorted(a))
    image_file = url_for('static',filename='faces/' + current_user.image_file)
    return render_template('workspace.html', title='WorkSpace',image_file=image_file,user=user)

@app.route("/phd")
@login_required
def phd():
    user=User.query.all()
    image_file = url_for('static',filename='faces/' + current_user.image_file)
    return render_template('phd.html', title='Phd',user=user,image_file=image_file,phd=phds)



@app.route("/mtech")
@login_required
def mtech():
    user=User.query.all()
    image_file = url_for('static',filename='faces/' + current_user.image_file)
    return render_template('mtech.html', title='M.TECH',user=user,image_file=image_file,mtech=phds)



@app.route("/people")
@login_required
def people():
    user=User.query.all()
    image_file = url_for('static',filename='faces/' + current_user.image_file)
    return render_template('people.html',image_file=image_file,user=user,title='Members')

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form=PostForm()
    user=User.query.all()
    post=Post.query.all()
    image_file = url_for('static',filename='faces/' + current_user.image_file)
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('new_post'))
    return render_template('annoucements.html',image_file=image_file,user=user,title='Annoucements',form=form,post=post)


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('new_post'))

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user,title='Users')

@app.route('/lab/<application>')
@login_required
def lab(application):
    image_file = url_for('static',filename='faces/' + current_user.image_file)
    for p in phds:
        if p.Application==application:
            return render_template('lab.html',image_file=image_file,title='Lab',cand=p)

    


@app.route('/send/<application>')
@login_required
def send(application):
    def too(phds):
        for p in phds:
            if p.Application == application:
                p.Submission='Done'
                db.session.merge(p)
                db.session.flush()
                db.session.commit()
                break
    too(phds)
    return redirect('phd')

@app.route('/verify/<application>')
@login_required
def verify(application):
    def too(phds):
        for p in phds:
            if p.Application == application:
                p.Validation='Done'
                db.session.merge(p)
                db.session.flush()
                db.session.commit()
                break
    too(phds)
    return redirect('dashboard')




@app.route('/comment/<application>', methods=['GET', 'POST'])
@login_required
def comment(application):
    def too(phds):
        for p in phds:
            if p.Application == application:
                p.Comment=request.form['comment']
                db.session.merge(p)
                db.session.flush()
                db.session.commit()
                break
    too(phds)
    return redirect('phd')



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



