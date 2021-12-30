import requests
import os

def DownloadFile():
    # delete the old database
    if os.path.exists("data/CovidData.sqlite"):
        os.remove("data/CovidData.sqlite")

    # download the csv file
    URL = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
    r = requests.get(URL, allow_redirects=False)
    open('data/CovidData.csv', 'wb').write(r.content)

    # convert the csv file to sqlite file (already install csvs-to-sqlite)
    os.system("csvs-to-sqlite data/CovidData.csv data/CovidData.sqlite")
    #time.sleep(3600)
