from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin, AsaList, SQLAlchemyUserDatastore
from sqlalchemy.ext.mutable import MutableList

db = SQLAlchemy()

class test(db.Model):
    __tablename__ = 'test_table'
    id = db.Column(db.Integer, primary_key=True)
    var1FromDb = db.Column(db.String())
    var2FromDb = db.Column(db.Boolean)
    var3FromDb = db.Column(db.Integer)
    example = db.Column(db.String())

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255)) # 
    permissions = db.Column(MutableList.as_mutable(AsaList()), nullable=True) #

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True) #*
    email = db.Column(db.String(255), unique=True) #*
    username = db.Column(db.String(255), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=False) #*

    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)

    active = db.Column(db.Boolean()) #*

    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False) #*

    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary='roles_users',
                         backref=db.backref('users', lazy='dynamic')) #*
    
user_datastore = SQLAlchemyUserDatastore(db,User, Role)