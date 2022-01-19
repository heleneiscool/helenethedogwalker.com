import sys
import json
print(sys.path)
from flask import Flask, render_template, request, redirect
import requests

# import os
# from os import path
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

email = "walks4wagz@gmail.com"
app = Flask(__name__)
app.secret_key = "banana"

@app.route("/")
def home():
    message = request.args.get('message')
    return render_template("home.html", message=message)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/do_contact", methods=['POST'])
def do_contact():

    name = request.form['user_name']
    user_email = request.form['email']
    phone = request.form['phone']
    message = request.form['message']
    print('Name: ', name)
    print('Email: ', user_email)
    print('Phone: ', phone)
    print('message:', message)
    captcha_response = request.form['g-recaptcha-response']
    secret = "6LcLJ4sdAAAAAHKUibfKR2qVT7OzQEq018O6yADw"
    payload = {'response':captcha_response, 'secret':secret}
    response = requests.post("https://www.google.com/recaptcha/api/siteverify", payload)
    response_text = json.loads(response.text)
    if not response_text['success']:
       return redirect("/?message=Sorry+no+robots")

    for item in [name, user_email, phone, message]:
        if len(item) < 1:
            return redirect(request.referrer + "?message=Please+enter+valid+data+in+all+fields")
    banana = "secret"
    msg = "<p>sender:{}<br>Email: {}<br>Phone: {}<br>Message:<br>{}".format(name, user_email, phone, message)
    message = MIMEMultipart('alternative')
    message['Subject'] = 'subject'
    message['From'] = email
    message['To'] = email
    email_content = MIMEText(msg, 'html')
    message.attach(email_content)
    port = 465
    smtp_server = "smtp.gmail.com"
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(email, banana)
        server.sendmail(email, email, message.as_string())
    return redirect("/?message=Thanks+you+are+one+step+closer+to+joining+the+pack")


if __name__ == "__main__":
    app.run(debug=True)
    app.run(host='0.0.0.0')
