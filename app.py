# -------------------------------------------------------------------------------------------------------- #
# TATIA, Final Project - Emojislation                                                                      #
# -------------------------------------------------------------------------------------------------------- #
# 30 Jan 2024, Université Côte d'Azur.                                                                     #
# Charafeddine Achir & Rafael Baptista.                                                                    #
# -------------------------------------------------------------------------------------------------------- #
# This file contains the server-side code for the Emojislation web application.                            #
# Responsible for storing the data from validation surveys in the database.                                #
# -------------------------------------------------------------------------------------------------------- #

import  json
import  csv
import  string

from    flask       import Flask
from    flask       import request
from    flask       import jsonify
from    flask       import Flask
from    flask       import session
from    flask       import render_template
from    pymongo     import MongoClient
from    datetime    import datetime
from    main        import *

app = Flask(__name__)

# -------------------------------------------------------------------------------------------------------- #
# Setting up the database connection.                                                                      #
# -------------------------------------------------------------------------------------------------------- #

client           = MongoClient("mongodb+srv://admin:admin@waterbnb.lo1mkvx.mongodb.net/")
dbname           = 'WaterBnB'
dbnames          = client.list_database_names()
db               = client.WaterBnB
collname         = 'emojis'
collEmojislation = db.emojislation

# -------------------------------------------------------------------------------------------------------- #
# Setting up the routes.                                                                                   #
# -------------------------------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------------------------------- #
# Home page.                                                                                               #
# -------------------------------------------------------------------------------------------------------- #
@app.route('/')                                                                    # Home route (index.html)
def hello_world():

    # ---------------------------------------------------------------------------------------------------- #
    # Making a translation.                                                                                #
    # ---------------------------------------------------------------------------------------------------- #

    translation = ""
    translation = translator("Night is shinning with stars")

    return render_template('index.html',translation=translation)    # Render the home page

# -------------------------------------------------------------------------------------------------------- #
# Validation page 1.                                                                                       #
# -------------------------------------------------------------------------------------------------------- #
@app.route('/validation')
def validation():
    return render_template('emojis.html')

# -------------------------------------------------------------------------------------------------------- #
# Validation page 2.                                                                                       #
# -------------------------------------------------------------------------------------------------------- #
@app.route('/validation2')
def validation2():
    return render_template('emojis2.html')

# -------------------------------------------------------------------------------------------------------- #
# Validation page 3.                                                                                       #
# -------------------------------------------------------------------------------------------------------- #
@app.route('/validation3')
def validation3():
    return render_template('emojis3.html')

# -------------------------------------------------------------------------------------------------------- #
# Validation Input Received.                                                                               #
# -------------------------------------------------------------------------------------------------------- #
@app.route('/validated')
def validated():

    # ---------------------------------------------------------------------------------------------------- #
    # Getting the number of validated phrases and the total number of phrases.                             #
    # ---------------------------------------------------------------------------------------------------- #

    validated = request.args.get('nb_validated')                   # Getting the number of validated phrases
    total     = request.args.get('nb_total')                           # Getting the total number of phrases

    # ---------------------------------------------------------------------------------------------------- #
    # Inserting the number of validated phrases and the total number of phrases to the database.           #
    # ---------------------------------------------------------------------------------------------------- #

    collEmojislation.insert_one({"total": total, "validated": validated, "date": datetime.now()})

    return render_template('validated.html')                                         # Render validated form