from flask import*
from src.dbconnection import *


app =Flask(__name__)
@app.route("/")
def login():
    return render_template("login.html")


@app.route("/login_code",methods=["post"])
def login_code():
    username = request.form["textfield"]
    password = request.form["textfield2"]
    qry = "SELECT * FROM `login` WHERE `username`=%s AND `password`=%s"
    val = (username, password)
    res = selectone(qry, val)


    if res is None:
        return '''<script>alert("Invalid username or password");window.location="/"</script>'''
    elif res['type'] == "admin":
        return '''<script>alert("Welcome Admin");window.location="/admin"</script>'''
    elif res['type'] == "canteen":
        return '''<script>alert("Welcome Canteen");window.location="/canteen"</script>'''
    elif res['type'] == "user":
        return '''<script>alert("Welcome User");window.location="/user"</script>'''
    else:
        return '''<script>alert("Invalid username or password");window.location="/"</script>'''


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

@app.route("/canteen_register_code",methods=['post'])
def canteen_register_code():
    name = request.form["textfield"]
    place = request.form["textfield2"]
    post = request.form["textfield3"]
    pin = request.form["textfield4"]
    phone = request.form["textfield5"]
    email = request.form["textfield6"]
    license = request.form["textfield7"]
    username = request.form["textfield8"]
    password = request.form["textfield9"]

    qry = "INSERT INTO`login` VALUES(NULL,%s,%s,'canteen')"
    val = (username,password)
    id = iud(qry,val)

    qry = "INSERT INTO `canteen` VALUES(NULL,%s,%s,%s,%s,%s,%s,%s, %s)"
    val = (id, name, place, post, pin, phone, email, license)

    iud(qry,val)
    return '''<script>alert("Registration successfull");window.location="/"</script>'''



@app.route("/verifyUser")
def verifyUser():
    return render_template("Canteen/verifyUser.html")


@app.route("/user")
def user():
    return render_template("User/userHome.html")

app.run(debug = True)