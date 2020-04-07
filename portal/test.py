

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
                                    p.Tutor1=u.username
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
                            p.Tutor1=u.username
                            p.alloc_status ='1'
                            db.session.merge(p)
                            db.session.flush()
                            db.session.commit()
                            i=i+1
            flag1=1
            quotient = phd_val//user_val
            remainder = phd_val%user_val
            fla=0
            i=0
            for u in user:
                flag1=1
                if u.is_admin==False and u.is_manager==False :
                    if fla==1:
                        for p in phds:
                            if i==quotient:
                                if remainder > 0 :
                                    flag1=0
                                    if p.alloc_status=='1' and p.Tutor1 != u.username:
                                        p.Tutor2=u.username
                                        p.alloc_status='0'
                                        db.session.merge(p)
                                        db.session.flush()
                                        db.session.commit()
                                        remainder =remainder - 1
                                        flag1=1
                                if flag1 == 1:
                                    i=0
                                    break
                            if i<quotient and p.alloc_status=='1' and p.Tutor1!=u.username:
                                p.Tutor2=u.username
                                p.alloc_status ='0'
                                db.session.merge(p)
                                db.session.flush()
                                db.session.commit()
                                i=i+1
                    fla=1
                
            flag1=1
            fla=0
            quotient = phd_val//user_val
            i=0
            for u in user:
                flag1=1
                if u.is_admin==False and u.is_manager==False:
                    for p in phds:
                        if i==quotient:
                            if remainder > 0 :
                                flag1=0
                                if p.alloc_status =='1' and p.Tutor1 != u.username:
                                    p.Tutor2=u.username
                                    p.alloc_status='0'
                                    db.session.merge(p)
                                    db.session.flush()
                                    db.session.commit()
                                    remainder =remainder - 1
                                    flag1=1
                            if flag1 == 1:
                                i=0
                                break
                        if i<quotient and p.alloc_status=='1' and p.Tutor1!=u.username:
                            p.Tutor2=u.username
                            p.alloc_status ='0'
                            db.session.merge(p)
                            db.session.flush()
                            db.session.commit()
                            i=i+1
                    break
            for pd in phds:
                pd.alloc_status='1'

        foo(user,phds)
        return redirect(url_for('phd'))
    else:
        return render_template('error.html')



@app.route("/allocate_mtech", methods=['GET', 'POST'])
@login_required
def allocate_mtech():
    if current_user.is_admin == True:
        user=User.query.all()
        def loo(user,mtechs):
            i=0
            user_val=0
            mt_val=0
            flag1=1
            for x in user:
                if x.is_admin == False and x.is_manager == False:
                    user_val=user_val+1
            for mt in mtechs:
                mt_val=mt_val+1
            quotient = mt_val//user_val
            remainder = mt_val%user_val
            for u in user:
                flag1=1
                if u.is_admin==False and u.is_manager==False:
                    for p in mtechs:
                        if i==quotient:
                            if remainder > 0 :
                                flag1=0
                                if p.alloc_status=='0':
                                    p.Tutor1=u.username
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
                            p.Tutor1=u.username
                            p.alloc_status ='1'
                            db.session.merge(p)
                            db.session.flush()
                            db.session.commit()
                            i=i+1
            flag1=1
            quotient = mt_val//user_val
            remainder = mt_val%user_val
            fla=0
            i=0
            for u in user:
                flag1=1
                if u.is_admin==False and u.is_manager==False :
                    if fla==1:
                        for p in mtechs:
                            if i==quotient:
                                if remainder > 0 :
                                    flag1=0
                                    if p.alloc_status=='1' and p.Tutor1 != u.username:
                                        p.Tutor2=u.username
                                        p.alloc_status='0'
                                        db.session.merge(p)
                                        db.session.flush()
                                        db.session.commit()
                                        remainder =remainder - 1
                                        flag1=1
                                if flag1 == 1:
                                    i=0
                                    break
                            if i<quotient and p.alloc_status=='1' and p.Tutor1!=u.username:
                                p.Tutor2=u.username
                                p.alloc_status ='0'
                                db.session.merge(p)
                                db.session.flush()
                                db.session.commit()
                                i=i+1
                    fla=1
                
            flag1=1
            fla=0
            quotient = mt_val//user_val
            i=0
            for u in user:
                flag1=1
                if u.is_admin==False and u.is_manager==False:
                    for p in phds:
                        if i==quotient:
                            if remainder > 0 :
                                flag1=0
                                if p.alloc_status =='1' and p.Tutor1 != u.username:
                                    p.Tutor2=u.username
                                    p.alloc_status='0'
                                    db.session.merge(p)
                                    db.session.flush()
                                    db.session.commit()
                                    client.close()
                                    remainder =remainder - 1
                                    flag1=1
                            if flag1 == 1:
                                i=0
                                break
                        if i<quotient and p.alloc_status=='1' and p.Tutor1!=u.username:
                            p.Tutor2=u.username
                            p.alloc_status ='0'
                            db.session.merge(p)
                            db.session.flush()
                            db.session.commit()
                            i=i+1
                    break
            for pd in mtechs:
                pd.alloc_status='1'

        loo(user,mtechs)
        return redirect(url_for('mtech'))
    else:
        return render_template('error.html')




@app.route("/reset_phd", methods=['GET', 'POST'])
@login_required
def reset_phd():
	if current_user.is_admin == True:
		conn = sqlite3.connect('portal/site.db') 
        c = conn.cursor()
        df=pd.read_csv('portal/mtech.csv')
        c.execute('''DELETE FROM phd;''')
		return redirect('phd')
	else:
		return render_template('error.html')


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
            return redirect(next_page) if next_page else redirect(url_for('checkUser'))
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


@app.route("/checkUser")
@login_required
def checkUser():
    if current_user.is_admin==True or current_user.is_manager==True:
        return redirect('dashboard')
    else:
        return redirect('workspace')


@app.route("/dashboard")
@login_required
def dashboard():
    if current_user.is_admin == True or current_user.is_manager == True:
        user=User.query.all()
        image_file = url_for('static',filename='faces/' + current_user.image_file)
        pi=0
        mi=0
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
        t=c.execute('''PRAGMA table_info('phd')''').fetchall()
        for p in pobj:
            pi+=1
        for p in mobj:
            mi+=1
        for p in phds:
            if p.Submission == 'Done':
                p_sub_count=p_sub_count+1
            if p.Validation == 'Done':
                p_val_count=p_val_count+1
            if p.alloc_status == '0':
                p_bundle=0
        for p in mtechs:
            if p.Submission == 'Done':
                m_sub_count=m_sub_count+1
            if p.Validation == 'Done':
                m_val_count=m_val_count+1
            if p.alloc_status == '0':
                m_bundle=0
        for x in user:
            if x.is_admin == False and x.is_manager == False:
                u_val=u_val+1
            if x.is_admin == False and x.is_manager == True:
                m_val=m_val+1
            if x.is_admin == True:
                a_val=a_val+1
        if (len(pobj)):
            length=len(pobj[0])
        else:
            length=0
        pobj=[tup[::-1] for tup in pobj] 
        t.reverse()
        return render_template('dashboard.html', title='Dashboard',
                        image_file=image_file,phd=pobj,t=t,length=length,
                        user=user,pi=pi,p_sub_count=p_sub_count,
                        p_val_count=p_val_count,u_val=u_val,m_val=m_val,a_val=a_val,
                        p_bundle=p_bundle,mtech=mtechs,
                        mi=mi,m_sub_count=m_sub_count,
                        m_val_count=m_val_count,
                        m_bundle=m_bundle)
    else:
        return render_template('error.html')


@app.route("/reset")
@login_required
def reset():
    if current_user.is_admin == True:
        image_file = url_for('static',filename='faces/' + current_user.image_file)
        return render_template('reset.html', title='Reset',image_file=image_file)
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
    image_file = url_for('static',filename='faces/' + current_user.image_file)
    return render_template('workspace.html', title='WorkSpace',image_file=image_file,user=user)

@app.route("/phd")
@login_required
def phd():
    user=User.query.all()
    conn = sqlite3.connect('portal/site.db') 
    c = conn.cursor()
    test=c.execute('''SELECT * FROM phd''').fetchall()
    t=c.execute('''PRAGMA table_info('phd')''').fetchall()
    if (len(test)):
        length=len(test[0])
    else:
        length=0
    t_pos=0
    test=[tup[::-1] for tup in test] 
    t.reverse()
    image_file = url_for('static',filename='faces/' + current_user.image_file)
    for col in t:
        t_pos+=1
        if col[1]=='Tutor2':
            break
    if current_user.is_admin==True or current_user.is_manager == True:
        return render_template('phd_admin.html', title='Phd',user=user,image_file=image_file,phd=test,t=t,length=length,t_pos=t_pos)
    else:
        return render_template('phd_ta.html', title='Phd',user=user,image_file=image_file,phd=phds)



@app.route("/mtech")
@login_required
def mtech():
    user=User.query.all()
    image_file = url_for('static',filename='faces/' + current_user.image_file)
    if current_user.is_admin==True or current_user.is_manager == True:
        return render_template('mtech_admin.html', title='M.TECH',user=user,image_file=image_file,mtech=mtechs)
    else:
        return render_template('mtech_ta.html', title='M.TECH',user=user,image_file=image_file,mtech=mtechs)



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
    return render_template('announcements.html',image_file=image_file,user=user,title='Announcements',form=form,post=post)


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

@app.route('/lab_phd/<application>')
@login_required
def lab_phd(application):
    image_file = url_for('static',filename='faces/' + current_user.image_file)
    for p in phds:
        if p.Application==application:
            if p.Submission != 'Done':
                flash('This file has not yet been submitted by TA', 'danger')
                return render_template('lab_phd.html',image_file=image_file,title='Lab',cand=p)
            else:
                return render_template('lab_phd.html',image_file=image_file,title='Lab',cand=p)


@app.route('/lab_mtech/<application>')
@login_required
def lab_mtech(application):
    image_file = url_for('static',filename='faces/' + current_user.image_file)
    for p in mtechs:
        if p.Application==application:
            if p.Submission != 'Done':
                flash('This file has not yet been submitted by TA', 'danger')
                return render_template('lab_mtech.html',image_file=image_file,title='Lab',cand=p)
            else:
                return render_template('lab_mtech.html',image_file=image_file,title='Lab',cand=p)


@app.route('/ta_lab_phd/<application>')
@login_required
def ta_lab_phd(application):
    image_file = url_for('static',filename='faces/' + current_user.image_file)
    for p in phds:
        if p.Application==application:
            return render_template('ta_lab_phd.html',image_file=image_file,title='Lab',cand=p)


@app.route('/ta_lab_mtech/<application>')
@login_required
def ta_lab_mtech(application):
    image_file = url_for('static',filename='faces/' + current_user.image_file)
    for k in mtechs:
        if k.Application==application:
            return render_template('ta_lab_mtech.html',image_file=image_file,title='Lab',cand=k)



@app.route('/send_phd/<application>')
@login_required
def send_phd(application):
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


@app.route('/send_mtech/<application>')
@login_required
def send_mtech(application):
    def too(mtechs):
        for p in mtechs:
            if p.Application == application:
                p.Submission='Done'
                db.session.merge(p)
                db.session.flush()
                db.session.commit()
                break
    too(mtechs)
    return redirect('mtech')




@app.route('/verify_phd/<application>')
@login_required
def verify_phd(application):
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



@app.route('/verify_mtech/<application>')
@login_required
def verify_mtech(application):
    def too(mtechs):
        for p in mtechs:
            if p.Application == application:
                p.Validation='Done'
                db.session.merge(p)
                db.session.flush()
                db.session.commit()
                break
    too(mtechs)
    return redirect('dashboard')




@app.route('/comment_phd/<application>', methods=['GET', 'POST'])
@login_required
def comment_phd(application):
    def too(phds):
        for p in phds:
            if p.Application == application:
                p.Comment=request.form['comment']
                db.session.merge(p)
                db.session.flush()
                db.session.commit()
                break
    too(phds)
    return redirect(url_for('ta_lab_phd',application=application))

@app.route('/comment_mtech/<application>', methods=['GET', 'POST'])
@login_required
def comment_mtech(application):
    def too(mtechs):
        for p in mtechs:
            if p.Application == application:
                p.Comment=request.form['comment']
                db.session.merge(p)
                db.session.flush()
                db.session.commit()
                break
    too(phds)
    return redirect(url_for('ta_lab_mtech',application=application))




@app.route('/change_phd/<application>', methods=['GET', 'POST'])
@login_required
def change_phd(application):
    def too(phds):
        for p in phds:
            if p.Application == application:
                p.Tutor1=request.form['tutor1']
                p.Tutor2=request.form['tutor2']
                db.session.merge(p)
                db.session.flush()
                db.session.commit()
                break
    too(phds)
    return redirect('phd')

@app.route('/change_mtech/<application>', methods=['GET', 'POST'])
@login_required
def change_mtech(application):
    def too(mtechs):
        for p in mtechs:
            if p.Application == application:
                p.Tutor1=request.form['tutor1']
                p.Tutor2=request.form['tutor2']
                db.session.merge(p)
                db.session.flush()
                db.session.commit()
                break
    too(phds)
    return redirect('mtech')

