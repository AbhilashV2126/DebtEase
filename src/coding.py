from flask import*
from src.dbconnection import *

from werkzeug.utils import secure_filename
import os


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

@app.route("/blockUnblockCanteen")
def blockUnblockCanteen():
    return render_template("Admin/blockUnblockCanteen.html")


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
    license = request.files["textfield7"]
    username = request.form["textfield8"]
    password = request.form["textfield9"]

    license_name = secure_filename(license.filename)
    license.save(os.path.join("static/uploads", license_name))

    qry = "INSERT INTO`login` VALUES(NULL,%s,%s,'pending')"
    val = (username, password)
    id = iud(qry, val)

    qry = "INSERT INTO `canteen` VALUES(NULL,%s,%s,%s,%s,%s,%s,%s, %s)"
    val = (id, name, place, post, pin, phone, email, license_name)

    iud(qry,val)
    return '''<script>alert("Registration partially completed....wait for verification");window.location="/"</script>'''



@app.route("/verifyUser")
def verifyUser():
    return render_template("Canteen/verifyUser.html")


@app.route("/user")
def user():
    return render_template("User/userHome.html")


@app.route("/userRegistration")
def userRegistration():

    qry = 'SELECT `canteen`.name,`canteen`.lid FROM `canteen` JOIN `login` ON `canteen`.lid = `login`.id WHERE `login`.type = "canteen"'
    res = selectall(qry)


    return render_template("User/userRegistration.html", val = res)

@app.route("/user_register_code",methods=['post'])
def user_register_code():
    canteen_id = request.form["select"]
    name = request.form["textfield"]
    id_dtails = request.files["file"]
    email = request.form["textfield2"]
    phone = request.form["textfield3"]
    profile_photo = request.files["file2"]
    username = request.form["textfield4"]
    password = request.form["textfield5"]

    id_details_name = secure_filename(id_dtails.filename)
    id_dtails.save(os.path.join("static/uploads", id_details_name))

    profile_photo_name = secure_filename(profile_photo.filename)
    profile_photo.save(os.path.join("static/uploads", profile_photo_name))

    qry = "INSERT INTO`login` VALUES(NULL,%s,%s,'pending')"
    val = (username, password)
    id = iud(qry, val)

    qry = "INSERT INTO `user` VALUES(NULL,%s,%s,%s,%s,%s,%s,%s)"
    val = (id, canteen_id, name, id_details_name, email, phone, profile_photo_name)

    iud(qry, val)
    return '''<script>alert("Registration partially completed...wait for verification");window.location="/"</script>'''


app.run(debug = True)