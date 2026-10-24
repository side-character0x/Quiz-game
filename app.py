from flask import Flask,request,render_template,session,redirect
from questions import Question
import random
from db import Database
import time

app=Flask(__name__)
app.secret_key="secret"
@app.route("/")
def base():
    return render_template("base.html")

@app.route("/prehome")
def start():
    username=session["username"]
    session.clear()
    session["username"]=username
    return redirect("/home")
@app.route("/home", methods=["GET","POST"])
def home():
    if request.method=="POST":
        if "categories" in session:
            difficulty=request.form.get("difficulty")
            if difficulty=="easy":
                if session["categories"]=="all":
                    data=Question().fetch(10,"easy")
                else:
                    data=Question().fetch(10,"easy",category=session["categories"])
                max_qn=10
            elif difficulty=="medium":
                if session["categories"]=="all":
                    data=Question().fetch(13,"medium")
                else:
                    data=Question().fetch(13,"medium",category=session["categories"])
                max_qn=13
            elif difficulty=="hard":
                if session["categories"]=="all":
                    data=Question().fetch(15,"hard")
                else:
                    data=Question().fetch(15,"hard",category=session["categories"])
                max_qn=15
            if not data:
                return redirect("/error")
            session["data"]=data
            session["index"]=0
            session["difficulty"]=difficulty
            session["max_qn"]=max_qn
            session["score"]=0
            session["coins_earned"]=0
            session["hint_used"]=False
            session["hint"]=False
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
    data=session["data"]
    index=session.get("index")
    options=data[index][1]
    sec_hint=False
    if session["hint"] and session["hint_used"]:
        sec_hint=True
        options=session["hinted_qn"]
    lack=False
    if session["hint"] and not session["hint_used"] :
        if Database().get_coins(session["username"])<20:
            lack=True
        else:
            Database().reduce_coins(session["username"],20)
            options=options[2:]
            session["hinted_qn"]=options
            session["hint_used"]=True
    Category=data[index][3]
    if not sec_hint:
        random.shuffle(options)
    return render_template("test.html",max_qn=session.get("max_qn"),qn_no=index+1,question=data[index][0],options=options,score=session.get("score"),coins=Database().get_coins(session["username"]),category=Category,lack=lack,sec_hint=sec_hint)

@app.route("/answer", methods=["GET","POST"])
def answer():
    session["hint"]=request.form.get("hint")
    if session["hint"]:
        return redirect("/quiz")
    option=request.form.get("option")
    correct_ans=session["data"][session['index']][2]
    session['index']+=1
    session["hint"]=False
    session["hint_used"]=False
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
        session.pop("categories", None)
    return render_template("result.html",result=option==correct_ans,coins=coins,last=last if last else False)

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=='POST':
        username=request.form.get("name")
        pin=request.form.get("pin")
        check=Database().check_user(username,pin)
        if check:
            session.clear()
            session["username"]=username
            return render_template("home.html",coins=Database().get_coins(username),username=username)
        else:
            return render_template("login.html",error=True)
    return render_template("login.html")

@app.route("/signin", methods=["GET","POST"])
def signin():
    if request.method=="POST":
        session.clear()
        username=request.form.get("name")
        session["username"]=username
        pin=request.form.get("pin")
        Database().add_user(username,pin)
        return render_template("home.html",coins=Database().get_coins(username),username=username)
    return render_template("signin.html")

@app.route("/category",methods=["GET","POST"])
def category():
    if request.method=="POST":
        categories=request.form.get("category")
        session["categories"]=categories
        return redirect("/home")
    return render_template("category.html",categories=Question().get_categories())

@app.route("/error")
def error():
    return render_template("error.html")

@app.route("/rapid")
def rapid():
    session["time"]=time.time()+30
    session["rapid_data"]=Question().rapid_qn()
    session["rapid_index"]=0
    session["rapid_score"]=0
    return redirect("/startrapid")

@app.route("/startrapid")
def startrapid():
    time_left=int(session["time"] - time.time())
    if time_left<=0:
        return render_template("rapid_result.html",question=session["rapid_index"],correct=session["rapid_score"],coins=session["rapid_score"]*2)
    index=session["rapid_index"]
    question=session["rapid_data"][index][0]
    options=session["rapid_data"][index][1]
    return render_template("rapid.html",time=time_left,question=question,options=options,score=session["rapid_score"],question_no=session["rapid_index"]+1)

@app.route("/rapidans",methods=["GET","POST"])
def rapidans():
    if request.method=="POST":
        option=request.form["option"]
        correct_ans=session["rapid_data"][session["rapid_index"]][2]
        if option==correct_ans:
            session["rapid_score"]+=1
        session["rapid_index"]+=1
        return redirect("/startrapid")



app.run( debug=True)