from flask import Flask,request,render_template

app=Flask(__name__)

@app.route("/")
def base():
    return render_template("base.html")

@app.route("/home")
def home():
    return render_template("home.html")
app.run(debug=True)