from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
import sqlite3

app = Flask(__name__)

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USERNAME='favourowoeye038@gmail.com',        
    MAIL_PASSWORD='xulyrtqmpkptqijz',           
    MAIL_USE_TLS=False,
    MAIL_USE_SSL=True
)
mail = Mail(app)

 
@app.route('/')
def home():
    return render_template("index.html")

 
@app.route('/appointment', methods=['POST'])
def appointment():
    # Get form data
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    department = request.form['department']
    date = request.form['date']

   
    conn = sqlite3.connect('appointments.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            department TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    c.execute('''
        INSERT INTO appointments (name, email, phone, department, date)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, email, phone, department, date))
    conn.commit()
    conn.close()
 
    msg = Message(
        "New Appointment Booked",
        sender="favourowoeye038@gmail.com",
        recipients=["favourowoeye4@gmail.com"]  
    )
    msg.body = f"""
New Appointment Details:

Name: {name}
Email: {email}
Phone: {phone}
Department: {department}
Date: {date}
"""
    mail.send(msg)

    
    return redirect(url_for('home', success=1))

 
if __name__ == "__main__":
    app.run(debug=True)
