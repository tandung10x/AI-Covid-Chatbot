import re
import time
import spacy
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request
from sqlite3.dbapi2 import OperationalError
from calendar import month_name
from GetDataFile import DownloadFile
from QnA import *

DownloadFile()

app = Flask(__name__)

# access the Database
conn = sqlite3.connect('data/CovidData.sqlite', check_same_thread=False)
c = conn.cursor()

# trained pipelines for English
nlp = spacy.load("en_core_web_md")

bot = create_bot("Bob")
custom_train(bot) # chatbot learn the Q&A lists

# all kinds of stats the chatbot knows
stats = ["total cases", "new cases", "total deaths", "new deaths", "hosp patients",
         "total tests", "new tests", "tests per case", "new vaccinations",
         "total vaccinations", "people vaccinated", "people fully vaccinated",
        ]

def detect_entity(message):
    category = ""   #
    location = ""   # 3 entities chatbot will recognize
    date = ""       #
    doc = nlp(message)

    # check entity is a location (country/continent)
    for ent in doc.ents:
        if ent.label_=="GPE" or ent.label_=="LOC":  
            location = ent.text.title()
    if "world" in message: # location can be whole world
        location = "World"
    
    # check which stats asked
    for s in stats:
        if s in message:
            category = s.replace(" ", "_")
            break
         
    # check entity is about date
    # types of format users may enter
    dateFormat = (r"\d?\d/\d?\d/20\d{2}", r"\d?\d-\d?\d-20\d{2}",
                  r"\d?\d/\d?\d/\d{2}"  , r"\d?\d-\d?\d-\d{2}") 
    monthYearFormat = '(' + '|'.join(month_name[1:]) + ')' + ".?\s\d{4}"
    yearFormat = r"20\d{2}"
    # check which format users entered
    if(re.search(dateFormat[0], message)):
        date = re.search(dateFormat[0], message).group()
        date = datetime.strptime(date, '%d/%m/%Y').strftime('%Y-%m-%d')
    elif(re.search(dateFormat[1], message)):
        date = re.search(dateFormat[1], message).group()
        date = datetime.strptime(date, '%d-%m-%Y').strftime('%Y-%m-%d')
    elif(re.search(dateFormat[2], message)):
        date = re.search(dateFormat[2], message).group()
        date = datetime.strptime(date, '%d/%m/%y').strftime('%Y-%m-%d')
    elif(re.search(dateFormat[3], message)):
        date = re.search(dateFormat[3], message).group()
        date = datetime.strptime(date, '%d-%m-%y').strftime('%Y-%m-%d')
    elif(re.search(monthYearFormat, message, re.IGNORECASE)):
        date = re.search(monthYearFormat, message, re.IGNORECASE).group()
        date = datetime.strptime(date, "%B %Y").strftime('%Y-%m')
    elif(re.search(yearFormat, message)):
        date = re.search(yearFormat, message).group()
    
    return (category, location, date)

def find_stats(message):   # return the stats user asked
    t = detect_entity(message)
    date = ""
    # get the figure from Database
    if(re.match(r'\d{4}-\d+-\d+', t[2])):
        c.execute("SELECT "+t[0]+" FROM CovidData WHERE location = ? AND date = ?", t[1:3])
        date = datetime.strptime(t[2], '%Y-%m-%d').strftime('%d/%m/%Y')
    elif(re.match(r'\d{4}-\d+', t[2])):
        c.execute("SELECT SUM("+t[0]+") FROM CovidData WHERE location = ? AND strftime('%Y-%m', date) = ?", t[1:3])
        date = datetime.strptime(t[2], '%Y-%m').strftime('%B, %Y') 
    elif(re.match(r'\d{4}', t[2])):
        c.execute("SELECT SUM("+t[0]+") FROM CovidData WHERE location = ? AND strftime('%Y', date) = ?", t[1:3])
        date = t[2]
    
    res = c.fetchall()
    return (res[0][0], date)

def respondStats(message): # return the bot's respond
    t = detect_entity(message)
    s = t[0]
    s = s.replace("_", " ") # make the respond more clear
    f = find_stats(message)
    responses = "The number of %s in %s on %s is: " %(s, t[1], f[1])
    bot_response = responses + str(f[0]) + '.'
    return bot_response

@app.route("/") # render html file
def home():
    return render_template("index.html")

@app.route("/get") # print the bot's response on UI
def get_bot_response():
    try:
        message = request.args.get('msg')  # get user's message
        time.sleep(0.8)
        return respondStats(message)
    except(OperationalError, IndexError, ValueError):  #if message not in stats part
        return str(respondQnA(bot, message)) # move to Q&A part

if __name__ == "__main__":
    app.run()
