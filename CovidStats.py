import re
import time
import spacy
import sqlite3
import datetime
from flask import Flask, render_template, request
from sqlite3.dbapi2 import OperationalError
from GetDataFile import DownloadFile
from QnA import *

#DownloadFile()

app = Flask(__name__)

# access the Database
conn = sqlite3.connect('data/CovidData.sqlite', check_same_thread=False)
c = conn.cursor()

# trained pipelines for English
nlp = spacy.load("en_core_web_sm")

bot = create_bot("Bob")
custom_train(bot)

# all kinds of stats the chatbot knows
stats = ["total cases", "new cases", "total deaths", "new deaths", "recovers",
        "hosp patients", "total tests", "new tests", "tests per case", "new vaccinations",
        "total vaccinations", "people vaccinated", "people fully vaccinated",
        ]

def detect_entity(message):
    category = ""
    location = ""   #init
    date = ""
    
    doc = nlp(message)
    for ent in doc.ents:
        # check the entity is a country or continent
        if ent.label_=="GPE" or ent.label_=="LOC":  
            location = ent.text.title()
        # check the entity is a date
        elif ent.label_=="DATE" or ent.label_=="CARDINAL":  
            date = datetime.datetime.strptime(ent.text, '%d/%m/%Y').strftime('%Y-%m-%d')
    # check which stats asked
    for s in stats:
        if s in message:   
            category = s.replace(" ", "_")
            break
    # location can be whole world
    if "world" in message:  
        location = "World"
    return (category, location, date)

def find_stats(message):    # return the stats user asked
    t = detect_entity(message)
    # get the figure from Database
    c.execute("SELECT " + t[0] + " FROM CovidData WHERE location = ? AND date = ?", t[1:3])
    res = c.fetchall()
    return res[0][0]

def respond(message): # return the bot's respond
    t = detect_entity(message)
    s = t[0]
    s = s.replace("_", " ")
    responses = "The number of %s in %s on %s is: " %(s, t[1], t[2])
    bot_response = responses + str(find_stats(message)) + '.'
    return bot_response

@app.route("/") # render html file
def home():
    return render_template("index.html")

@app.route("/get") # print the bot's response on UI
def get_bot_response():
    try:
        message = request.args.get('msg')  # get user's message
        time.sleep(0.5)
        return respond(message)
    except(OperationalError, IndexError):  #if message not in stats part
        return str(get_start_chatbot(bot, message)) # move to QnA part

if __name__ == "__main__":
    app.run()