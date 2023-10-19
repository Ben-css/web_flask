from flask import Flask,redirect,render_template,request,session,jsonify
from flask_bootstrap import Bootstrap
import mysql.connector
from datetime import datetime
from mysql.connector import Error
import pytz
import json


# 連接 MySQL 資料庫
connection = mysql.connector.connect(
    host='localhost',          # 主機名稱
    database='project',  # 資料庫名稱
    user='root',        # 帳號
    password='ea658903')  # 密碼

db = connection.cursor(buffered=True)
# cursor.execute("SELECT DATABASE();")
# record = cursor.fetchone()

app = Flask(
    __name__,
    static_folder="static",
    static_url_path="/"
            )
app.secret_key = "Hello World"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup_page",methods=["GET"])
def signuppage():
    return render_template("signup.html")

# 註冊
@app.route("/signup", methods=["POST"])
def signup():
    print(request)
    student_id = request.form['student_id']
    password = request.form['password']
    # email = request.form['email']
    name = request.form['name']
    # number = request.form['number']

    collection = db.users
    result = collection.find_one({
        "student_id": student_id
    })
    if result != None:
        return redirect("/error?msg=信箱已被註冊")

    collection.insert_one({
        "student_id": student_id,
        "password": password,
        # "email": email,
        "name": name,
        # "number": number
    })
    return redirect("/")

#登入route
@app.route("/signin", methods=["POST"])
def signin():
    studentid = request.form["studentid"]
    password = request.form["password"]
    # 和資料庫做互動
    collection = db.users
    # 檢查帳號密碼是否正確
    result = collection.find_one({
        "$and": [
            {"studentid": studentid},
            {"password": password},
        ]
    })

    # 登入失敗，到錯誤頁面
    if result == None:
        return redirect("/error?msg=帳號或密碼輸入錯誤")
    # 登入成功，在 session 紀錄會員資訊，到會員頁面
    session["student_id"] = result["studentid"]
    session["student_name"] = result["student_name"]
    session["number"] = result["number"]
    print(session['studentid'])
    return redirect("/member")

app.run(
    host= '0.0.0.0',
    port=2000,
    debug='true'
    )