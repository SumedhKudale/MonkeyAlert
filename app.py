from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Replace with your Gmail credentials
EMAIL_ADDRESS = 'pradyumna3andhare@gmail.com'
EMAIL_PASSWORD = 'xwjz hwxi qzwg mjch'

# Load your CSV data here
df = pd.read_csv('room.csv')
number_to_email = dict(zip(df.iloc[:, 0], df.iloc[:, 1]))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    if request.method == 'POST':
        n = int(request.form['room_number'])

        l = []

        if n != 214 and n != 246:
            l.append(n - 1)
            l.append(n + 1)
        else:
            if n == 214:
                l.append(213)
                l.append(245)
            elif n == 246:
                l.append(214)
                l.append(245)

        l.append(n - 100)
        l.append(n + 100)

        numbers = l

        email_addresses = [number_to_email.get(number, 'Email not found') for number in numbers]

        email_subject = 'Monkey Alert'
        email_message = 'A monkey is seen in Room ' + str(n)

        for to_email in email_addresses:
            send_email(email_subject, email_message, to_email, EMAIL_ADDRESS, EMAIL_PASSWORD)

        return redirect(url_for('index'))

def send_email(subject, message, to_email, email_address, email_password):
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_address, email_password)
        text = msg.as_string()
        server.sendmail(email_address, to_email, text)
        server.quit()
        print('Email sent successfully to', to_email)
    except Exception as e:
        print('Failed to send email:', str(e))

if __name__ == '__main__':
    app.run(debug=True)
