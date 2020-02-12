from datetime import datetime
from flask import abort
from flaskblog import app,db, login_manager,bcrypt
from flask_login import UserMixin
from flask_admin import Admin
from flask_admin.contrib import sqla
from flask_security import utils
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask.ext.admin.contrib.fileadmin import FileAdmin
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

# class Controller(ModelView):
#     def is_accessible(self):
#         if current_user.is_active==True and current_user.is_admin:
#             return current_user.is_authenticated
#         else:
#             return abort(404)
#     def not_auth(self):
#         return "You are not authorized to view admin dashboard"

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

admin =Admin(app,template_mode='bootstrap3')
admin.add_view(Controller(User,db.session))
path = op.join(op.dirname(__file__), 'static')
admin.add_view(FileAdmin(path, '/static/', name='Static Files'))