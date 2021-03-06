# AI-POWERED COVID CHATBOT
A chatbot can communicate with users through voice and text to do two specific tasks: 
1. Checking if users having COVID-19.
2. Answering real-time statistics and FAQs related to COVID-19 in all countries.
<img src="https://user-images.githubusercontent.com/85373307/156719455-689e6736-de63-444e-9cb5-7672f6d2e5df.png" width="420" />

## INSTALLATION: 
Running this to install required packages:
- pip install chatterbot
- pip install -U spacy
- python -m spacy download en_core_web_md
- pip install csvs-to-sqlite
- pip install Flask

After that, start with running file CovidStats.py, then open file app.html to run the chatbot.

## DEMO VIDEO: 
https://youtu.be/mD8OkazB7L8

## NOTATION:
In Covid Checking section:
For two chatbot's questions: "How old are you?" and "Now measure your temperature, tell me the interval.", please answer only a number.

## SUMMARY RESPONSIBILITY:
- *CovidCheck*: To do the task 1
- *data*: Including the list of Q&As and the COVID-19 real-time dataset maintained by *Our World in Data* (update everyday). More information about the dataset: https://github.com/owid/covid-19-data/tree/master/public/data
- *static*: Including the css file used in the entire project and images
- *templates*: The html file used in the task 2
- *CovidStats.py*: To answer the COVID-19 statistics
- *GetDataFile.py*: To automatically download the COVID-19 dataset (csv) to the data folder and convert it to sqlite
- *QnA.py*: To answer FAQs related to COVID-19

