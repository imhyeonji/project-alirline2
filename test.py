from flask import Flask, render_template, jsonify, request

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def saving():
    firstName_receive = request.form['firstName_give']
    lastName_receive = request.form['lastName_give']
    to_receive = request.form['to_give']
    from_receive = request.form['from_give']
    email_receive = request.form['email_give']
    departure_receive = request.form['departure_give']
    destination_receive = request.form['destination_give']
    passenger_receive = request.form['passenger_give']
    price_receive = request.form['price_give']

    ticket = {

        'firstName' : firstName_receive,
        'lastName' : lastName_receive,
        'to' : to_receive,
        'from' : from_receive,
        'email' : email_receive,
        'departure' : departure_receive,
        'destination' : destination_receive,
        'passenger' : passenger_receive,
        'price' : price_receive,
        'is_emailed' : False
    }
    db.tickets.insert_one(ticket)
    return jsonify({'result' : 'success'})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5002,debug=True)
