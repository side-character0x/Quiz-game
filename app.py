from flask import Flask,request,render_template,session,redirect
from questions import Question
import random
app=Flask(__name__)
app.secret_key="secret"
@app.route("/")
def base():
    return render_template("base.html")

@app.route("/home", methods=["GET","POST"])
def home():
    if request.method=="POST":
        difficulty=request.form.get("difficulty")
        if difficulty=="easy":
            data=Question().fetch(10,"easy")
            max_qn=10
        elif difficulty=="medium":
            data=Question().fetch(13,"medium")
            max_qn=13
        elif difficulty=="hard":
            data=Question().fetch(10,"easy")
            max_qn=15
        session["data"]=data
        session["index"]=0
        session["difficulty"]=difficulty
        session["max_qn"]=max_qn
        session["score"]=0
        return redirect("/quiz")
    return render_template("home.html",username=None,coins=0,high=0)
@app.route("/quiz")
def quiz():
    if session["index"]>=session["max_qn"]:
        return render_template("quiz_result.html")
    data=session.get("data")
    index=session.get("index")
    options=data[index][1]
    random.shuffle(options)
    return render_template("test.html",max_qn=session.get("max_qn"),qn_no=index+1,question=data[index][0],op1=options[0],op2=options[1],op3=options[2],op4=options[3],score=session.get("score"))

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
    return render_template("result.html",result=option==correct_ans,coins=coins)
app.run(debug=True)