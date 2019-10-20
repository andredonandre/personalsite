import firebase_admin
from firebase_admin import credentials, firestore, db
from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

cred = credentials.Certificate("sembatya-firebase-adminsdk-dk6sp-5dacc1dd07.json")
firebase = firebase_admin.initialize_app(cred, options = {
'databaseURL':'https://sembatya.firebaseio.com'
})

db = firestore.client()

class Subscriber:
    def __init__(self, name, email):
        self.name = name
        self.email = email
    def to_dict(self):
        dest = {
            u'name': self.name,
            u'email': self.email
        }
        return dest

    def __repr__(self):
        return(
            u'Subscriber(name={}, email={})'
            .format(self.name, self.email))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about/')
def about():
    subs = []
    docs = db.collection(u'subscribers').list_documents()
    for doc in docs:
       obj = doc.get().to_dict()
       subs.append(Subscriber(obj['name'],obj['email']))
    return render_template('about.html',subscribers = subs)

@app.route('/subscribers/')
def subscribers():
    subs = []
    docs = db.collection(u'subscribers').stream()
    for doc in docs:
        subs.append('{}'.format(json.dumps(doc.to_dict())))
    return '<h1>test</h1>'+'\n'.join(subs)

@app.route('/addSubscriber/', methods=['POST'])
def addsubscriber():
    try:
        sub = Subscriber(request.form['name'], request.form['email'])
        db.collection(u'subscribers').document().set(sub.to_dict())
        return render_template("about.html", success = "User was successfully added")
    except Exception as e:
        return render_template("about.html", error = e)

if __name__=='__main__':
    app.run(debug=True)
