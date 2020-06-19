import os
import json
import requests
from flask import Flask, session, render_template, jsonify, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)
good_read_key = "djdT4M51nVgc8OrYSxPlA"

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=["POST", "GET"])
def index():
    msg="no"
    session.clear()
    if request.method=="POST":
        user=request.form.get('username')
        password=request.form.get('passwrd')
        data=db.execute("SELECT * FROM users WHERE username = :user",{"user":user}).fetchone()
        if data!=None:
            if data.username==user and data.password==password:
                    session["username"]=user
                    return redirect(url_for("search"))
            else:
                msg="pass"
        else:
            msg="user"
    return render_template("index.html",msg=msg)


@app.route("/register", methods=["POST", "GET"])
def register():
    msg="no"
    session.clear()
    if request.method=="POST":
        user=request.form.get('username')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        data=db.execute("SELECT * FROM users WHERE username = :user",{"user":user}).fetchone()
        user_exists=False
        if data != None:
            if data.username==user:
                msg="user"
                user_exists=True
        if user_exists==False:
            if user==None or user=="":
                msg="no_User"
            elif len(password1)<8:
                msg="long"
            elif password1 != password2:
                msg="pass"
            else:
                db.execute("INSERT INTO users (username,password) VALUES (:user,:pass)",{"user":user,"pass":password1})
                db.commit()
                return  redirect(url_for("index"))
    return render_template("register.html",msg=msg)

@app.route("/search", methods=["POST", "GET"])
def search():
    msg="no"
    session["books"]=[]   
    if request.method=="POST":
        text=request.form.get('text') 
        data=db.execute("SELECT * FROM books WHERE author iLIKE '%"+text+"%' OR title iLIKE '%"+text+"%' OR isbn iLIKE '%"+text+"%'").fetchall()
        
        for book in data:
            session['books'].append(book)
        if len(session["books"])==0:
            msg="no_results"

    return render_template("search.html",data=session['books'], msg=msg)

@app.route("/book/<string:isbn>", methods=["POST", "GET"])
def book(isbn):
    msg="no"
    username=session.get('username')
    mess="no"
    if username is None:
        mess="no_user"
    
    session["reviews"]=[]
    second=db.execute("SELECT * FROM reviews WHERE isbn = :isbn AND username= :username",{"username":username,"isbn":isbn}).fetchone()
    if request.method=="POST":
        if second!=None:
            msg="second"
        else:
            review=request.form.get('text') 
            rate=request.form.get('rate')
            db.execute("INSERT INTO reviews (isbn, review, rating, username) VALUES (:Isbn,:Review,:Rating,:Username)",{"Isbn":isbn,"Review":review,"Rating":rate,"Username":username})
            db.commit()
    good_read_data = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": good_read_key, "isbns": isbn})
    avg_rating=good_read_data.json()['books'][0]['average_rating']
    rating_count=good_read_data.json()['books'][0]['work_ratings_count']
    reviews=db.execute("SELECT * FROM reviews WHERE isbn = :isbn",{"isbn":isbn}).fetchall() 
    for review in reviews:
        session['reviews'].append(review)
    data=db.execute("SELECT * FROM books WHERE isbn = :isbn",{"isbn":isbn}).fetchone()

    return render_template("book.html",data=data,reviews=session['reviews'],avg_rating=avg_rating,rating_count=rating_count,username=username,msg=msg,mess=mess)


@app.route("/api/<string:isbn>")
def api(isbn):


    good_read_data = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": good_read_key, "isbns": isbn})
    if good_read_data.status_code!=200:
        raise Exception("ERROR:404 API request not found")
    book=db.execute("SELECT * FROM books WHERE isbn = :isbn",{"isbn":isbn}).fetchone()
    avg_rating=good_read_data.json()['books'][0]['average_rating']
    rating_count=good_read_data.json()['books'][0]['work_ratings_count']

    jsons = {
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "isbn": isbn,
        "review_count": rating_count,
        "average_score": avg_rating
    }
    api=json.dumps(jsons)
    return render_template("api.json",api=api)