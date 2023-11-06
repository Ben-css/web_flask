from flask import *
import pymongo
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, DateTimeField,
                     RadioField, SelectField,
                     TextAreaField, SubmitField)
from wtforms.validators import DataRequired
import pytz
import json


client = pymongo.MongoClient(
    "mongodb+srv://root:root123@cluster0.9cjg4lw.mongodb.net/?retryWrites=true&w=majority")
db = client.test


# class MyForm(FlaskForm):
#     dorm = RadioField(
#         '棟別', choices=[('B1', 'B1'), ('B2', 'B2'), ('H', 'H'), ('M', 'M'), ('N', 'N')])
#     place = RadioField('地點', choices=[('寢室', '寢室'), ('公共區域', '公共區域')])
#     fix_items = RadioField('類別', choices=[('電燈', '電燈'), ('門栓', '門栓'), ('窗戶', '窗戶'), (
#         '鏡子', '鏡子'), ('水龍頭', '水龍頭'), ('洗衣機', '洗衣機'), ('烘衣機', '烘衣機'), ('消防設備', '消防設備'), ('其他', '其他')])
#     other_fix_items = TextAreaField('其他維修項目')
#     explain = TextAreaField('說明')
#     submit = SubmitField("確認")


app = Flask(
    __name__,
    static_folder="static",
    static_url_path="/"
)
bootstrap = Bootstrap(app)
moment = Moment(app)
# 設定session key
app.secret_key = "Hello World"

# 首頁
@app.route("/")
def index():
    return render_template("index.html")

# 註冊route
@app.route("/signup_page")
def signuppage():
    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup():
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
    student_id = request.form["student_id"]
    password = request.form["password"]
    # 和資料庫做互動
    collection = db.users
    # 檢查帳號密碼是否正確
    result = collection.find_one({
        "$and": [
            {"student_id": student_id},
            {"password": password},
        ]
    })

    # 登入失敗，到錯誤頁面
    if result == None:
        return redirect("/error?msg=帳號或密碼輸入錯誤")
    # 登入成功，在 session 紀錄會員資訊，到會員頁面
    session["student_id"] = result["student_id"]
    session["name"] = result["name"]
    # session["number"] = result["number"]
    # print(session['student_id'])
    return redirect("/form")

# 會員頁
@app.route("/member")
def member():
    # form = MyForm()
    # 如果student_id在session才能登入
    if "student_id" in session:
        return render_template("member.html",
        #    form=form,
            name=session.get('name'),
            student_id=session.get('student_id'),         
            )
    else:
        return redirect("/")

# 表單頁
@app.route("/form",methods=["GET"])
def form():
    # form = MyForm()
    # 如果student_id在session才能登入
    if "student_id" in session:
        student_id=session.get('student_id')
        collection = db.forms
        form_list =  list(collection.find({"student_id": student_id}).sort("submit_at", pymongo.DESCENDING))
        
        for student in form_list:
            student["_id"] = str(student["_id"])

        # print(form_list)
        return render_template("form.html",
        #    form=form,
            name=session.get('name'),
            student_id=session.get('student_id'),
            form_list=form_list
            )
    else:
        return redirect("/error?msg=未進行登入，請先登入")


# 進度表
@app.route("/tesk_info")
def get_progress():
        return render_template("tesk_info.html")
    # # 和資料庫做互動
    # collection = db.forms
    
    # # 使用者學號&姓名
    # result = collection.find()

    # # 從資料庫動態抓取資料
    # # itemvalue = []
    # # subtime = []
    # # status = []
    # progress = []
    # len = 0
    # # 從資料庫中抓資料做成list
    # for items in result:
    #     if items['student_id'] != session['student_id']:
    #         continue
    #     len += 1
    #     # itemvalue.append(items['fix_items'])
    #     # subtime.append(items['submit_at'])
    #     # status.append(items['status'])
    #     progress.append([
    #         items['fix_items'],
    #         items['dorms'],
    #         items['place'],
    #         items['number'],
    #         items['submit_at'],
    #         items['explain'],
    #         items['status'],
    #         items['other_fix_items'],
    #         items['progress_explain']])
    
    # # print(explain)
    # # print(subtime)
    # # print(status)

    # # print(progress)
    # # 再把資料轉成json後傳給前端
    # return jsonify(progress)

#公告頁
#僅供測試使用，你可以搬到自己喜歡的地方
@app.route("/announcement")
def get_announcement():
    return render_template("announcement.html")


# 表單驗證、儲存
@app.route('/submit_form',methods=["POST"])
def submit_form():
    # form = MyForm()

    twtime = pytz.timezone('Asia/Taipei')
    twtime = datetime.now(twtime)
    submit_at = twtime.strftime("%Y.%m.%d %H:%M")

    if request.method == "POST":
        student_id = session['student_id']
        name = session['name']
        # number = session['number']
        dorms = request.form["dorm"]
        location = request.form["location"]
        fix_items = request.form["fix_items"]
        other_fix_items = request.form["other_fix_items"]
        fix_explain = request.form["fix_explain"]
        # 進度說明預設為空
        progress_explain = ""

        # print(request.form)
        # print(dorm)

        forms = db.forms
        # default_values = {
        #     "dorms": "未提供",
        #     "number": 0,
        #     "location": "未提供",
        #     "fix_items": "未提供",
        #     "other_fix_items": "未提供",
        #     "fix_explain": "未提供",
        #     "status": "待確認",
        #     "progress_explain": "未提供"
        # }
        forms.insert_one({
            "student_id": student_id,
            "name": name,
            # "dorms": dorms,
            # "number": number,
            "location": location,
            "fix_items": fix_items,
            "other_fix_items": other_fix_items,
            "fix_explain": fix_explain,
            "status": "待確認",
            "submit_at": submit_at,
            "progress_explain": progress_explain
        })
        # 不需要==
        # form.dorm.data = ''
        # form.place.data = ''
        # form.fixsubject_1.data = ''
        # form.fixsubject_2.data = ''
        # form.explain.data = ''

        # 刪除資料用
    #     collection = db.forms
    #     result = collection.delete_many({
    #         "name": "阿偉"
    # })
    #     print("實際上被刪除的資料",result.deleted_count + "筆")

    # 記得重新導向回/member !!
    # 不然用render_template("/member",form=form)會被導到/forms
    return redirect('/form')
# redirect(url_for('member'))


# 管理員登入
@app.route("/manager_signin_page", methods=["GET"])
def manager_signin_page():
    return render_template('manager_login.html')


@app.route("/manager_signin", methods=["POST"])
def manager_signin():
    account = request.form["account"]
    password = request.form["password"]
    # 和資料庫做互動
    collection = db.managers
    # 檢查帳號密碼是否正確
    result = collection.find_one({
        "$and": [
            {"account": account},
            {"password": password},
        ]
    })

    # 登入失敗，到錯誤頁面
    if result == None:
        return redirect("/error?msg=帳號或密碼輸入錯誤")
    # 登入成功，在 session 紀錄會員資訊，到會員頁面
    session["account"] = result["account"]
    session["manager_name"] = result["manager_name"]
    print(session['account'])
    return render_template('manager_page.html')



# 管理員註冊
@app.route("/manager_signup", methods=["POST"])
def manager_signup():
    manager_name = request.form['manager_name']
    account = request.form['account']
    password = request.form['password']

    collection = db.managers
    result = collection.find_one({
        "account": account,
    })
    if result != None:
        return redirect("/error?msg=帳號已被註冊")

    collection.insert_one({
        "manager_name": manager_name,
        "account": account,
        "password": password,
    })
    return redirect("/manager_signup_page")


@app.route("/manager_signup_page", methods=["POST"])
def manager_signup_page():
    return render_template('mg_signup.html')



# 維修單
@app.route("/fix_page")
def  fix_page():
    # 和資料庫做互動
    collection = db.forms

    # 使用者學號&姓名
    result = collection.find()
  

    # result1 = collection1.find()

    # 從資料庫動態抓取資料
    # itemvalue = []
    # subtime = []
    # status = []
    fixlist = []
    len = 0
    # 從資料庫中抓資料做成list
    for items in result:
        len += 1
        # itemvalue.append(items['fix_items'])
        # subtime.append(items['submit_at'])
        # status.append(items['status'])
        fixlist.append([
            items['dorms'],
            items['name'],
            items['fix_items'],
            items['place'],
            items['number'],
            items['status'],
            items['submit_at'],
            items['explain'],
            items['other_fix_items'],
            items['progress_explain']])
    
    # print(itemvalue)
    # print(subtime)
    # print(status)
    print(fixlist)
    # 再把資料轉成json後傳給前端
    return jsonify(fixlist)



@app.route("/fixlist_change")
def fixlist_change():
    twtime = pytz.timezone('Asia/Taipei')
    twtime = datetime.now(twtime)
    changetime = twtime.strftime("%Y.%m.%d %H:%M")

    if request.method == "POST":
        time = request.form["status"]
        name = request.form["name"]
        # 進度說明預設為空
        progress_explain = request.form["progress_explain"]

        print(request.form)
        # print(dorm)

        forms = db.forms
        # 找到要修改的fixform
        # result = forms.update_one({
        #     "$and": [
        #     {"submit_at": time},
        #     {"name": name},
        # ],"$set":{
        #     "status"
        #     }
        # })
    return redirect(url_for('fix_page'))
        


# 錯誤route
@app.route("/error")
def error():
    message = request.args.get("msg", "發生錯誤")
    return render_template("error.html", message=message)


# 使用者登出
@app.route("/signout")
def signout():
    del session['name']
    del session['student_id']
    # del session["number"]
    return redirect("/")

@app.route("/manager_signout")
def manager_signout():
    del session['account']
    del session['manager_name']
    return redirect("/")


app.run(
    # host= '0.0.0.0', 任何ip都可訪問
    port=3000, 
    debug=True
    )
