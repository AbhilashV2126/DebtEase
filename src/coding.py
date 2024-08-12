from flask import*
from src.dbconnection import *


app =Flask(__name__)
@app.route("/")
def login():
    return render_template("login.html")


@app.route("/admin")
def admin():
    return render_template("Admin/adminHome.html")


@app.route("/verifyCanteen")
def verifyCanteen():
    return render_template("Admin/verifyCanteen.html")


@app.route("/viewComplaint")
def viewComplaint():
    return render_template("Admin/viewComplaint.html")


@app.route("/complaintReply")
def complaintReply():
    return render_template("Admin/complaintReply.html")


@app.route("/canteen")
def canteen():
    return render_template("Canteen/canteenHome.html")


@app.route("/registerCanteen")
def registerCanteen():
    return render_template("Canteen/registerCanteen.html")


@app.route("/verifyUser")
def verifyUser():
    return render_template("Canteen/verifyUser.html")


@app.route("/user")
def user():
    return render_template("User/userHome.html")

app.run(debug = True)