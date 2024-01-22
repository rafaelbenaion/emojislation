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


    collEmojislation.insert_one({"userid": "ui"})

    return 'Hello, World!'
