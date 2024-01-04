from model import app,db,Person,Classroom,InfoData
import pymysql
import pandas as pd
from flask import render_template,redirect,url_for,request,flash,Response


app.secret_key = '123456'


def CookieCheck():
    username_ = request.cookies.get('username')
    password_ = request.cookies.get('password')
    if username_!="admin" and password_!="admin":
        return 0
    # resp.set_cookie("password", password_)
    return 1
@app.route('/importData')
def initData():
    # 初始化
    db.drop_all()
    db.create_all()
    # 导入数据
    person_data = pd.read_csv('./csv_data/person.csv')
    for index, row in person_data.iterrows():
        newdata = Person(id = row[0],person_name =row[1])
        db.session.add(newdata)

    classroom_data = pd.read_csv('./csv_data/classroom.csv')
    for index, row in classroom_data.iterrows():
        newdata = Classroom(id = row[0],classroom_name =row[1])
        db.session.add(newdata)
    db.session.commit()
    data = pd.read_csv('./csv_data/data.csv')
    for index, row in data.iterrows():
        newdata = InfoData(id=row[0],classroom_id=row[1],person_id=row[2],week=row[3],day=row[4],section=row[5])
        db.session.add(newdata)
    db.session.commit()
    return redirect('/')

@app.route('/')
def home():
    # if CookieCheck()==0:
    #     return redirect('/login')
    username_ = request.cookies.get('username')
    password_ = request.cookies.get('password')
    if username_!="admin" and password_!="admin":
        return redirect('/login')
    sql_query_5 = "SELECT data.id,classroom_name,person_name,week,day,section FROM data,person,classroom where data.person_id=person.id and data.classroom_id=classroom.id order by classroom_name asc"
    connect = pymysql.Connect(host='localhost', port=3306,user='root',passwd='021020',db='db',charset='utf8') 
    cursor = connect.cursor()
    cursor.execute(sql_query_5)
    result_5 = cursor.fetchall()
    return render_template('home.html',data=result_5,flag=0) 
@app.route('/insert')
def InsertFun():
    return render_template('insert.html',flag1=0)

@app.route('/insert_page',methods=['GET','POST'])
def insert_page():
    #接受数据
    classroom_name_ =  request.form["classroom_name"]
    person_name_ =  request.form["person_name"]
    week_ =  request.form["week"]
    day_ =  request.form["day"]
    section_ =  request.form["section"]

    #判断时间是否冲突
    connect = pymysql.Connect(host='localhost', port=3306,user='root',passwd='021020',db='db',charset='utf8') 
    cursor = connect.cursor()
    sql_query_1 = "SELECT count(*) FROM data,person,classroom where data.person_id=person.id and data.classroom_id=classroom.id and week=%s and day=%s and section=%s and classroom.classroom_name='%s'"%(week_,day_,section_,classroom_name_)
    cursor.execute(sql_query_1)
    result_1 = cursor.fetchone()[0]
    if result_1!=0:
        flash('时间冲突！请更改预定时间')
        return redirect('/')
     
     
    #确定id号
    sql_query_2 = "SELECT max(id) from data"
    cursor.execute(sql_query_2)
    result_2 = cursor.fetchone()[0]
    id_ = result_2+1
    # 确定classroom_id和person_id

    sql_query_3 = "SELECT id from classroom where classroom_name='%s'"%classroom_name_
    cursor.execute(sql_query_3)
    result_3 = cursor.fetchone()
    if result_3==None:
        flash('教室名称错误！请重新输入')
        return redirect('/')
    else:
        classroom_id_ = result_3[0]

    sql_query_4 = "SELECT id from person where person_name='%s'"%person_name_
    cursor.execute(sql_query_4)
    result_4 = cursor.fetchone()
    if result_4==None:
        flash('学员队名称错误！请重新输入')
        return redirect('/')
    else:
        person_id_ = result_4[0]

    newdata = InfoData(id=id_,classroom_id=classroom_id_,person_id=person_id_,week=week_,day=day_,section=section_)
    db.session.add(newdata)
    db.session.commit()
    return redirect('/')
@app.route('/query')
def query():
    return render_template('query.html')
@app.route('/query_page',methods=['GET','POST'])
def query_page():
    classroom_name_ =  request.form["classroom_name"]
    week_ =  request.form["week"]

    connect = pymysql.Connect(host='localhost', port=3306,user='root',passwd='021020',db='db',charset='utf8') 
    cursor = connect.cursor()    
    sql_query_3 = "SELECT id from classroom where classroom_name='%s'"%classroom_name_
    cursor.execute(sql_query_3)
    result_3 = cursor.fetchone()
    if result_3==None:
        flash('教室名称错误！请重新输入')
        return redirect('/')
    #开始查询
    sql_query_4 = "SELECT data.id,classroom_name,person_name,week,day,section FROM data,person,classroom where data.person_id=person.id and data.classroom_id=classroom.id and week=%s and classroom.classroom_name='%s'"%(week_,classroom_name_)

    cursor.execute(sql_query_4)
    result_4 = cursor.fetchall()
    return render_template('home.html',data=result_4,flag=1) 

@app.route('/delete',methods=['GET','POST'])
def deletePage():
    #取出需要删除的id
    id_=request.args.get("id")
    user_info = InfoData()
    user_info.query.filter_by(id=id_).delete()
    db.session.commit()
    return redirect('/')

@app.route('/modify',methods=['GET','POST'])
def modifyPage():
    #取出需要删除的id
    id_=request.form["id"]
    user_info = InfoData()
    user_info.query.filter_by(id=id_).delete()
    db.session.commit()
    #取出信息
    allData=[]
    allData.append(request.form["classroom_name"])
    allData.append(request.form["person_name"])
    allData.append(request.form["week"])
    allData.append(request.form["day"])
    allData.append(request.form["section"])
    return render_template('insert.html',allData=allData)
@app.route('/login')
def Mylogin():
    return render_template('login.html')

@app.route('/set_cookie',methods=['POST'])
def MySetCookie():
    #取出用户名和密码
    username_ = request.form["username"]
    password_ = request.form["password"]
    resp = redirect('/')
    resp.set_cookie("username", username_)
    resp.set_cookie("password", password_)

    return resp
if __name__ == '__main__':
    app.run(host='0.0.0.0', port= 8888, debug=True) 