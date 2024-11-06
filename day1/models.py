from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class test(db.Model):
    __tablename__ = 'test_table'
    id = db.Column(db.Integer, primary_key=True)
    var1FromDb = db.Column(db.String())
    var2FromDb = db.Column(db.Boolean)
    var3FromDb = db.Column(db.Integer)