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

    return render_template('index.html') # Render validation form

@app.route('/validation')
def validation():
    return render_template('emojis.html')

@app.route('/validation2')
def validation():
    return render_template('emojis2.html')

@app.route('/validation3')
def validation():
    return render_template('emojis3.html')

@app.route('/validated')
def validated():

    # Recover data from get request

    validated = request.args.get('nb_validated')
    total     = request.args.get('nb_total')

    collEmojislation.insert_one({"total": total, "validated": validated, "date": datetime.now()})

    return render_template('validated.html') # Render validation form