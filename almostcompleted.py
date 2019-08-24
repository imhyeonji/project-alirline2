import requests
import smtplib
import schedule
import time

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta


def make_alarm(destination, from_date, to_date, passenger, target_price):
    url = "https://api.skypicker.com/flights?fly_from=SEL&fly_to=" + destination + "&date_from=" + from_date + "&date_to=" + from_date + "&return_from=" + to_date + "&return_to=" + to_date + "&adults=" + str(passenger) + "&curr=KRW&sort=price&partner=picky"
    result = requests.get(url)
    result_text = result.json()
    price = result_text['data'][0]['price']

    if price <= int(target_price):
        return True
    else:
        return False

def sending_email(send_to_email):
    email = 'sending.scc.project@gmail.com'  # Your email
    password = 'scc123123!'  # Your email account password

    message = 'This is my message_test'  # The message in the email

    server = smtplib.SMTP('smtp.gmail.com', 587)  # Connect to the server
    server.starttls()  # Use TLS
    server.login(email, password)  # Login to the email server
    server.sendmail(email, send_to_email, message)  # Send the email
    server.quit()  # Logout of the email server

    db.tickets.update_one({'is_emailed':False,'email':send_to_email},{'$set':{'is_emailed': True}})

def get_db_data():
    tickets = db.tickets.find({'is_emailed':False},{'_id':0})
    for ticket in tickets:
        destination = ticket['destination']
        from_date = ticket['from']
        to_date = ticket['to']
        passenger = ticket['passenger']
        target_price = ticket['price']
        email = ticket['email']
        print('ticket info ----',destination,from_date,to_date,passenger,target_price)

        is_email = make_alarm(destination,from_date,to_date,passenger,target_price)
        if (is_email):
            print('sending..')
            sending_email(email)
        else:
            print('yet sending')

def job():
    print("정해진 시간이 됐으니 실행하자")
    get_db_data()

schedule.every(3600).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)