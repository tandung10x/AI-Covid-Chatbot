import requests
import os

def DownloadFile():
    if os.path.exists("CovidData.sqlite"):
        os.remove("CovidData.sqlite")

    URL = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
    r = requests.get(URL, allow_redirects=False)
    open('CovidData.csv', 'wb').write(r.content)

    os.system("csvs-to-sqlite CovidData.csv CovidData.sqlite")
    #time.sleep(3600)