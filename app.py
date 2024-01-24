from flask import Flask
import json
import csv
import string
from flask import request
from flask import jsonify
from flask import Flask
from flask import session
from flask import render_template
from pymongo import MongoClient
from datetime import datetime
app = Flask(__name__)

client           = MongoClient("mongodb+srv://admin:admin@waterbnb.lo1mkvx.mongodb.net/")
dbname           = 'WaterBnB'
dbnames          = client.list_database_names()
db               = client.WaterBnB
collname         = 'emojis'
collEmojislation = db.emojislation


@app.route('/')
def hello_world():

    return 'Hello, World!'

@app.route('/validation')
def validation():

    return render_template('emojis.html')               # Render validation form

@app.route('/validated')
def validated():

    # Recover data from get request

    validated = request.args.get('nb_validated')
    total     = request.args.get('nb_total')

    collEmojislation.insert_one({"total": total, "validated": validated, "date": datetime.now()})

    return 'Thank you, for your contribution!'