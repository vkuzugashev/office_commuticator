from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
    
class Calls(db.Model):
    #__tablename__ = 'calls'
    id = db.Column(db.Integer, primary_key=True)
    id_caller = db.Column(db.String(200), nullable=False)
    id_callee = db.Column(db.String(200),  nullable=True)
    client_id = db.Column(db.String(200),  nullable=False)
    call_start = db.Column(db.String(200), nullable=False)
    call_end = db.Column(db.String(200), nullable=True)
    call_status = db.Column(db.String(200), nullable=False)
