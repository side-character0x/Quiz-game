from flask import Flask,request,render_template,session,redirect
from questions import Question
import random
from db import Database

app=Flask(__name__)
app.secret_key="secret"
@app.route("/")
def base():
    return render_template("base.html")

@app.route("/home", methods=["GET","POST"])
def home():
    if request.method=="POST":
        if "categories" in session:
            difficulty=request.form.get("difficulty")
            if difficulty=="easy":
                data=Question().fetch(10,"easy",category=session["categories"])
                max_qn=10
            elif difficulty=="medium":
                data=Question().fetch(13,"medium",category=session["categories"])
                max_qn=13
            elif difficulty=="hard":
                data=Question().fetch(15,"easy",category=session["categories"])
                max_qn=15
            session["data"]=data
            session["index"]=0
            session["difficulty"]=difficulty
            session["max_qn"]=max_qn
            session["score"]=0
            session["coins_earned"]=0
            return redirect("/quiz")
        else:
            return render_template("home.html",username=session["username"],coins=Database().get_coins(session["username"]),high=Database().get_highscore(session["username"]),category="not_selected")
    return render_template("home.html",username=session["username"],coins=Database().get_coins(session["username"]),high=Database().get_highscore(session["username"]),category=False)
@app.route("/quiz")
def quiz():
    if session["index"]>=session["max_qn"]:
        if session["score"]>Database().get_highscore(session["username"]):
            Database().add_highscore(session["username"],session['score'])
        return render_template("game_result.html",score=session["score"],total_qn=session["max_qn"],accuracy=(int(session['score'])/int(session['max_qn']))*100,coins=session["coins_earned"])
    data=session.get("data")
    index=session.get("index")
    options=data[index][1]
    Category=data[index][3]
    print(Category)
    random.shuffle(options)
    return render_template("test.html",max_qn=session.get("max_qn"),qn_no=index+1,question=data[index][0],op1=options[0],op2=options[1],op3=options[2],op4=options[3],score=session.get("score"),coins=Database().get_coins(session["username"]),category=Category)

@app.route("/answer", methods=["GET","POST"])
def answer():
    option=request.form.get("option")
    correct_ans=session["data"][session['index']][2]
    session['index']+=1
    coins=0
    if option==correct_ans:
        session["score"]+=1
        if session['difficulty']=="easy":
            coins=1
        elif session["difficulty"]=="medium":
            coins=2
        else:
            coins=4
        session["coins_earned"]+=coins
        Database().add_coins(session["username"],coins)
    last=False
    if session['index']==session["max_qn"]:
        last=True
    return render_template("result.html",result=option==correct_ans,coins=coins,last=last if last else False)

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=='POST':
        username=request.form.get("name")
        pin=request.form.get("pin")
        check=Database().check_user(username,pin)
        if check:
            session["username"]=username
            return render_template("home.html",coins=Database().get_coins(username),username=username)
        else:
            return render_template("login.html",error=True)
    return render_template("login.html")

@app.route("/signin", methods=["GET","POST"])
def signin():
    if request.method=="POST":
        username=request.form.get("name")
        session["username"]=username
        pin=request.form.get("pin")
        Database().add_user(username,pin)
        return render_template("home.html",coins=Database().get_coins(username),username=username)
    return render_template("signin.html")

@app.route("/category",methods=["GET","POST"])
def category():
    if request.method=="POST":
        categories=request.form.getlist("category")
        session["categories"]=categories
        return redirect("/home")
    return render_template("category.html",categories=Question().get_categories())
app.run(debug=True)