from flask import Flask, render_template, request, redirect, url_for
from twilio.rest import Client

app = Flask(__name__)

# Twilio configuration
TWILIO_ACCOUNT_SID = 'AC6afaec39d242884639fda5418e78afb2'
TWILIO_AUTH_TOKEN = '0abf2d0a60ffbc62008eaabaa55e4962'
TWILIO_PHONE_NUMBER = '+18334081809'

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Waiting list
waiting_list = []

@app.route('/')
def index():
    return render_template('index.html', waiting_list=waiting_list)

@app.route('/add', methods=['POST'])
def add_to_list():
    name = request.form['name']
    phone = request.form['phone']
    if name and phone:
        waiting_list.append({'name': name, 'phone': phone})
    return redirect(url_for('index'))

@app.route('/notify/<int:index>')
def notify(index):
    if 0 <= index < len(waiting_list):
        customer = waiting_list[index]
        send_sms(customer['phone'], customer['name'])
        del waiting_list[index]
    return redirect(url_for('index'))

def send_sms(phone_number, customer_name):
    message = client.messages.create(
        body=f"Hello {customer_name}, your table is ready at Nishikawa!",
        from_=TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    print(f"Sent message to {customer_name}: {message.sid}")

if __name__ == '__main__':
    app.run(debug=True)