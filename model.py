from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# import datetime
import warnings
warnings.filterwarnings("ignore")
# import pymysql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:021020@localhost:3306/db'
# 关闭数据库修改跟踪操作[提高性能]，可以设置为True，这样可以跟踪操作：
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 开启输出底层执行的sql语句
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
class Person(db.Model):
    #表模型
    __tablename__ = "person"   #表名
    id = db.Column(db.Integer, primary_key=True,nullable=False,autoincrement=True)
    person_name = db.Column(db.String(255),unique=True)

class Classroom(db.Model):
    #表模型
    __tablename__ = "classroom"   #表名
    id = db.Column(db.Integer, primary_key=True,nullable=False,autoincrement=True)
    classroom_name = db.Column(db.String(255),unique=True)

class InfoData(db.Model):
    #表模型
    __tablename__ = "data"   #表名
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    classroom_id = db.Column(db.Integer,db.ForeignKey("classroom.id"),nullable=False,autoincrement=True) 
    person_id = db.Column(db.Integer,db.ForeignKey("person.id"),nullable=False,autoincrement=True) 
    week  = db.Column(db.Integer,nullable=False)
    day  = db.Column(db.Integer,nullable=False)
    section  = db.Column(db.Integer,nullable=False)

