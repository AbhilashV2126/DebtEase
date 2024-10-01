from flask import*
from src.dbconnection import *
from flask_mail import *
from werkzeug.utils import secure_filename
import os
import smtplib
from email.mime.text import MIMEText
import razorpay


app =Flask(__name__)


app.secret_key = "59867876507"

app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Use the server for your mail service
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'debtease797@gmail.com'  # Your email address
app.config['MAIL_PASSWORD'] = 'fxmx obzz bvfr niwd'  # Your email password
app.config['MAIL_DEFAULT_SENDER'] = ('debt management', 'debtease797@gmail.com')

mail = Mail(app)


@app.route("/")
def login():
    return render_template("login_index.html")


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
        session['lid'] = res['id']
        return '''<script>alert("Welcome Admin");window.location="/admin"</script>'''
    elif res['type'] == "canteen":
        session['lid'] = res['id']
        return '''<script>alert("Welcome Canteen");window.location="/canteen"</script>'''
    elif res['type'] == "user":
        session['lid'] = res['id']
        return '''<script>alert("Welcome User");window.location="/user"</script>'''
    else:
        return '''<script>alert("Invalid username or password");window.location="/"</script>'''


@app.route("/admin")
def admin():
    return render_template("Admin/admin_index.html")


@app.route("/verifyCanteen")
def verifyCanteen():
    qry = 'SELECT * FROM `canteen` JOIN `login` ON `canteen`.lid = `login`.id WHERE `type`="pending"'
    res = selectall(qry)
    return render_template("Admin/verifyCanteen.html", val=res)


@app.route("/accept_canteen")
def accept_canteen():
    id = request.args.get('id')
    qry = 'UPDATE `login` SET `type`="canteen" WHERE `id`=%s'
    iud(qry, id)
    return '''<script>alert("Successfully accepted");window.location="/verifyCanteen"</script>'''


@app.route("/reject_canteen")
def reject_canteen():
    id = request.args.get('id')
    qry = 'UPDATE `login` SET `type`="rejected" WHERE `id`=%s'
    iud(qry, id)
    return '''<script>alert("rejected");window.location="/verifyCanteen"</script>'''


@app.route("/viewComplaint")
def viewComplaint():

    return render_template("Admin/viewComplaint.html")


@app.route("/Display_Complaint", methods=['post'])
def Display_Complaint():

    status = request.form['select']

    if status == "Replied":

        qry = "SELECT `complaint`.*,`user`.name FROM `complaint` JOIN user on `complaint`.user_id = `user`.lid where complaint.reply !='pending' "
        res = selectall(qry)
        return render_template("Admin/viewComplaint.html", val=res)
    else:
        qry = "SELECT `complaint`.*,`user`.name FROM `complaint` JOIN user on `complaint`.user_id = `user`.lid where complaint.reply ='pending' "
        res = selectall(qry)
        return render_template("Admin/viewComplaint.html", val=res, status = status)


@app.route("/complaintReply")
def complaintReply():
    cid = request.args.get('id')
    session['cid'] = cid
    return render_template("Admin/complaintReply.html")


@app.route("/insert_reply_code", methods=['post'])
def insert_reply_code():
    reply = request.form["textfield"]
    qry = "UPDATE `complaint` SET `reply`=%s WHERE id = %s"
    iud(qry,(reply, session['cid']))
    return '''<script>alert("Reply send successfully");window.location="/viewComplaint"</script>'''


@app.route("/blockUnblockCanteen")
def blockUnblockCanteen():
    qry = 'SELECT * FROM `canteen` JOIN `login` ON `canteen`.lid = `login`.id WHERE `type`="canteen" or `type`="blocked"'
    res = selectall(qry)
    return render_template("Admin/blockUnblockCanteen.html", val=res)


@app.route("/block_canteen")
def block_canteen():
    id = request.args.get('id')
    qry = 'UPDATE `login` SET `type`= "blocked" WHERE `id`=%s'
    iud(qry, id)
    return '''<script>alert("Blocked");window.location="/blockUnblockCanteen"</script>'''

@app.route("/unblock_canteen")
def unblock_canteen():
    id = request.args.get('id')
    qry = 'UPDATE `login` SET `type`= "canteen" WHERE `id`=%s'
    iud(qry, id)
    return '''<script>alert("Unblocked");window.location="/blockUnblockCanteen"</script>'''

@app.route("/blockUnblockUser")
def blockUnblockUser():
    qry = 'SELECT * FROM `user` JOIN `login` ON `user`.lid = `login`.id WHERE `type`="user" or `type`="blocked"'
    res = selectall(qry)
    return render_template("Admin/blockUnblockUser.html", val=res)

@app.route("/block_user")
def block_user():
    id = request.args.get('id')
    qry = 'UPDATE `login` SET `type`= "blocked" WHERE `id`=%s'
    iud(qry, id)
    return '''<script>alert("Blocked");window.location="/blockUnblockUser"</script>'''

@app.route("/unblock_user")
def unblock_user():
    id = request.args.get('id')
    qry = 'UPDATE `login` SET `type`= "user" WHERE `id`=%s'
    iud(qry, id)
    return '''<script>alert("Unblocked");window.location="/blockUnblockUser"</script>'''



@app.route("/canteen")
def canteen():
    return render_template("Canteen/canteen_index.html")


@app.route("/registerCanteen")
def registerCanteen():
    return render_template("Canteen/registerCanteen.html")


@app.route("/canteen_register_code", methods=['post'])
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



@app.route("/manage_user")
def manage_user():

    return render_template("Canteen/manage_user.html")


@app.route("/search_user", methods=['post'])
def search_user():
    name = request.form['textfield']
    qry = "SELECT * FROM `user` JOIN `login` ON `user`.lid = `login`.id WHERE `type`='user' and user.canteen_id="+str(session['lid'])+" and user.name like '"+name+"%'"
    res = selectall(qry)
    return render_template("Canteen/manage_user.html", val=res, uname = name)


@app.route("/view_debt")
def view_debt():
    id = request.args.get('id')
    session['uid'] = id
    qry = "SELECT * FROM `debtdetails` WHERE user_id=%s"
    res = selectall2(qry, id)

    return render_template("Canteen/view_debt.html", val=res)


@app.route("/delete_debt")
def delete_debt():
    id = request.args.get('id')
    qry = "DELETE FROM `debtdetails` WHERE id = %s"
    iud(qry, id)

    return '''<script>alert("Deleted");window.location="manage_user"</script>'''


@app.route("/add_debt", methods=['post'])
def add_debt():
    return render_template("Canteen/Add_debt.html")


@app.route("/insert_debt", methods=['post'])
def insert_debt():
    amount = request.form['textfield']
    details = request.form['textfield2']

    qry = "SELECT * FROM `wallet` WHERE lid=%s"
    res = selectone(qry, session['uid'])
    if res is not None:
        amt = res['amount']
    else:
        return '''<script>alert("User Wallet do not have minimum balance");window.location="manage_user"</script>'''


    qry = "SELECT * FROM `debtdetails` WHERE `user_id`=%s"
    res = selectall2(qry, session['uid'])
    tamt = 0
    for i in res :
         tamt = tamt + i['amount']

    if (amt >= 500 and tamt <= 2000):
          qry = "INSERT INTO `debtdetails` VALUES(NULL, %s, %s, %s, CURDATE(), 'pending')"
          iud(qry, (session['uid'], amount, details))
          return '''<script>alert("Success");window.location="manage_user"</script>'''
    elif(amt <= 500) :
        return '''<script>alert("User Wallet do not have minimum balance");window.location="manage_user"</script>'''
    else:
        return '''<script>alert("Maximum debt limit reached");window.location="manage_user"</script>'''


@app.route("/verifyUser")
def verifyUser():
    qry = 'SELECT * FROM `user` JOIN `login` ON `user`.lid = `login`.id WHERE `type`="pending" and user.canteen_id=%s'
    res = selectall2(qry, session['lid'])
    return render_template("Canteen/verifyUser.html", val=res)


@app.route("/send_mail")
def send_mail():
    return render_template("Canteen/mail.html")


@app.route("/send_mail2", methods=['post'])
def send_mail2():
    sub = request.form['textfield']

    qry = 'SELECT `user`.email, SUM(`debtdetails`.`amount`) AS amt FROM `debtdetails` JOIN `user` ON `debtdetails`.`user_id` = `user`.`lid` WHERE `user`.`canteen_id`=%s GROUP BY `user`.email HAVING SUM(`debtdetails`.`amount`) >= 2000 '
    res = selectall2(qry,session['lid'])

    def mail(s, email):
        try:
            # Establish a secure session with Gmail's SMTP server
            gmail = smtplib.SMTP('smtp.gmail.com', 587)
            gmail.ehlo()
            gmail.starttls()

            # Use environment variables or secure methods to handle credentials
            gmail.login('debtease797@gmail.com', 'fxmx obzz bvfr niwd')
            print("=====================login done")

            # Prepare the email content
            msg = MIMEText("Hi, " + str(s))
            msg['Subject'] = 'Pay Debt'
            msg['To'] = email
            msg['From'] = 'debtease797@gmail.com'

            # Send the email
            gmail.send_message(msg)
            print("Email sent successfully to", email)

        except Exception as e:
            print("Couldn't send email:", str(e))
            return '''<script>alert("Can't send mail"); window.location="/"</script>'''

        finally:
            gmail.quit()

        return '''<script>alert("Email sent successfully"); window.location="/"</script>'''

    # Assuming `res` is a list of dictionaries with user data
    if len(res) == 0:
        return '''<script>alert("No users have debt greater than 2000"); window.location="/"</script>'''

    for i in res:
        email = i['email']
        mail(sub, email)

    return '''<script>alert("Done"); window.location="/"</script>'''


@app.route("/accept_user")
def accept_user():
    id = request.args.get('id')
    qry = 'UPDATE `login` SET `type`="user" WHERE `id`=%s'
    iud(qry, id)
    return '''<script>alert("Successfully accepted");window.location="/verifyUser"</script>'''


@app.route("/reject_user")
def reject_user():
    id = request.args.get('id')
    qry = 'UPDATE `login` SET `type`="rejected" WHERE `id`=%s'
    iud(qry, id)
    return '''<script>alert("rejected");window.location="/verifyUser"</script>'''



@app.route("/user")
def user():
    return render_template("User/user_index.html")


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


@app.route("/recharge_wallet")
def recharge_wallet():
    return render_template("User/recharge_wallet.html")


@app.route("/recharge_wallet_proceed", methods=['post'])
def recharge_wallet_proceed():
    amt = request.form['textfield']
    amount = int(amt)*100
    session['amt'] = amount
    session['camt'] = amt
    return redirect("user_pay_proceed")


@app.route('/user_pay_proceed')
def user_pay_proceed():
    client = razorpay.Client(auth=("rzp_test_edrzdb8Gbx5U5M", "XgwjnFvJQNG6cS7Q13aHKDJj"))
    payment = client.order.create({'amount': session['amt'], 'currency': "INR", 'payment_capture': '1'})
    return render_template('UserPayProceed.html', p=payment)


@app.route("/user_pay_complete", methods=['post'])
def user_pay_complete():

    if session['curpay'] == "paying_debt":
        qry = "UPDATE `debtdetails` SET STATUS='payed' WHERE `id`=%s"
        iud(qry, session['payid'])
        return '''<script>alert("Debt Successfully Payed");window.location="view_debt_details"</script>'''

    elif session['curpay'] == "totalpayment":
        qry = "UPDATE `debtdetails` SET STATUS='payed' WHERE `user_id`=%s"
        iud(qry,session['lid'])
        return '''<script>alert("Debt Successfully Payed");window.location="view_debt_details"</script>'''

    qry = " SELECT * FROM `wallet` WHERE lid= %s"
    res = selectone(qry, session['lid'])

    if res is None:

        qry = "INSERT INTO `wallet` VALUES(NULL,%s,%s)"
        iud(qry, (session['lid'], session['camt']))

    else:

        qry = "UPDATE `wallet` SET amount = amount+%s WHERE lid=%s"
        iud(qry, (session['camt'], session['lid']))

    return '''<script>alert("Successfully Recharged");window.location="recharge_wallet"</script>'''


@app.route("/view_debt_details")
def view_debt_details():
    return render_template("User/view_debt_details.html")


@app.route("/display_debt_details", methods=['post'])
def display_debt_details():
    type = request.form['select']

    if type == "UnPayed":
        qry = "SELECT`debtdetails`.* FROM `debtdetails` WHERE `user_id`=%s AND STATUS='pending'"
        res = selectall2(qry,session['lid'])

        qry = "SELECT SUM(amount) AS amt FROM `debtdetails` WHERE `user_id`=%s AND STATUS='pending'"
        res2 = selectall2(qry, session['lid'])
        print(res)
        return render_template("User/view_debt_details.html", val=res, type="unpayed", amt=res2 [0]['amt'], status=type)
    else:
        qry = "SELECT * FROM `debtdetails` WHERE `user_id`=%s AND STATUS='payed'"
        res = selectall2(qry, session['lid'])
        return render_template("User/view_debt_details.html", val=res)


@app.route("/pay_debt")
def pay_debt():
    id = request.args.get('id')
    session['payid'] = id

    session['curpay'] = "paying_debt"

    amt = request.args.get('amt')
    session['actual_amt'] = amt

    amount = int(amt) * 100
    session['amt'] = amount
    session['camt'] = amt
    return render_template("User/user_pay_amount.html")


@app.route("/pay_total_amount")
def pay_total_amount():
    session['curpay'] = "totalpayment"

    amt = request.args.get('amt')

    session['actual_amt'] = amt

    amount = int(amt) * 100
    session['amt'] = amount
    session['camt'] = amt
    return render_template("User/user_pay_amount.html")


@app.route("/pay_from_wallet")
def pay_from_wallet():
    qry = "SELECT * FROM `wallet` WHERE lid=%s"
    res = selectone(qry, session['lid'])
    return render_template("User/user_pay_through_wallet.html", val=res)


@app.route("/pay_wallet_proceed")
def pay_wallet_proceed():

    balance = request.args.get('balance')

    if session['curpay'] == "paying_debt":

        if int(balance)<int(session['actual_amt']):
            return '''<script>alert("Not Enough Balance ");window.location="view_debt_details"</script>'''
        else:
            qry = "UPDATE `wallet` SET amount=amount-%s WHERE lid=%s"
            iud(qry, (session['actual_amt'], session['lid']))
            qry = "UPDATE `debtdetails` SET `status`='payed' where id=%s"
            iud(qry, session['payid'])
            return '''<script>alert("Payment Success");window.location="view_debt_details"</script>'''
    else:
        if int(balance) < int(session['actual_amt']):
            return '''<script>alert("Not Enough Balance ");window.location="view_debt_details"</script>'''
        else:
            qry = "UPDATE `wallet` SET amount=amount-%s WHERE lid=%s"
            iud(qry, (session['actual_amt'], session['lid']))
            qry = "UPDATE `debtdetails` SET `status`='payed' where user_id=%s"
            iud(qry, session['lid'])
            return '''<script>alert("Payment Success");window.location="view_debt_details"</script>'''


@app.route("/balance_view")
def balance_view():
    return render_template("User/balance_view.html")


@app.route("/balance_code")
def balance_code():
    qry ="SELECT * FROM `wallet` WHERE lid=%s"
    res = selectone(qry,session['lid'])
    return render_template("User/balance_view.html", val=res)


@app.route("/addComplaint")
def addComplaint():

    return render_template("User/addComplaint.html")

@app.route("/add_complaint_code" ,methods=['post'])
def add_complaint_code():
    id = session['lid']
    complaint = request.form['textfield']
    qry = "INSERT INTO `complaint` VALUES(NULL, %s, %s,  CURDATE(), 'pending')"
    iud(qry, (id, complaint ))
    return '''<script>alert("Successfully complaint added");window.location="addComplaint"</script>'''


app.run(debug=True)

