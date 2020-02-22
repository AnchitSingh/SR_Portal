from datetime import datetime
from flask import abort
from portal import app,db, login_manager,bcrypt
from flask_login import UserMixin
from flask_admin import Admin,BaseView,expose
from flask_admin.contrib import sqla
from flask_security import utils
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_admin.contrib.fileadmin import FileAdmin
import os.path as op


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_manager = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Controller(ModelView):
    column_display_pk=True
    can_create=True
    can_edit=True
    can_delete=True
    can_export=True
    def on_model_change(self,form,model,is_create):
        model.password=bcrypt.generate_password_hash(model.password).decode('utf-8')
        return current_user.is_authenticated
    def is_accessible(self):
        if current_user.is_active==True and current_user.is_admin:
            return current_user.is_authenticated
        else:
            return abort(404)


class phd(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    View = db.Column(db.String(50))
    Application = db.Column(db.String(50), unique=True, nullable=False)
    payment = db.Column(db.String(50))
    fee=db.String(db.String(50))

    def __repr__(self):
        return f"phd('{self.View}', '{self.Application}')"


class beast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    View = db.Column(db.String(50))
    Application_Ref = db.Column('Application Ref.',db.String(50), unique=True, nullable=False)
    payment = db.Column(db.String(50))
    fee=db.String(db.String(50))

    def __repr__(self):
        return f"beast('{self.View}')"


admin =Admin(app,template_mode='bootstrap3')
admin.add_view(Controller(User,db.session))
path = op.join(op.dirname(__file__), 'static')
admin.add_view(FileAdmin(path, '/static/', name='Static Files'))



#  i=0
#     user=User.query.all()
#     phds=phd.query.all()
#     user_val=0
#     phd_val=0
#     for x in user:
#         if x.is_admin == False and x.is_manager == False:
#             user_val=user_val+1
#     for pd in phds:
#         phd_val=phd_val+1
#     quotient = phd_val//user_val
#     remainder = phd_val%user_val

#     for u in user:
#         if u.is_admin==False and u.is_manager==False:
#             for p in phds:
#                 if i==quotient:
#                     if remainder > 0 and p.payment == '1':
#                         p.View=u.username
#                         p.payment='0'
#                         db.session.add(p)
#                         db.session.commit()
#                         db.update(phd)
#                         remainder =remainder - 1
#                     break
#                 if i<quotient and p.payment=='1':
#                     p.View=u.username
#                     p.payment='0'
#                     db.session.add(p)
#                     db.session.commit()
#                     db.update(phd)
#                     i=i+1