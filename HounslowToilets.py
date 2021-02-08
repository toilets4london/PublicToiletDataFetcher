import requests
from bs4 import BeautifulSoup
import json
import re

url = "https://maps.hounslow.gov.uk/map/Aurora.svc/GetRecordsByPoint?sessionId=c2faa26a-20ea-49dc-967e-a6f68327d0ac&x=515467.8421180836&y=178364.07866495367&radius=100000"

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def read_data():
    with open("Data/hounslow_raw.json") as dataFile:
        jsonData = json.loads(dataFile.read())
        htmlData = jsonData['Html']
        lines = htmlData.split("\n")
        lines = [cleanhtml(l).replace("\r", "") for l in lines]
    for line in lines:
        print(line)

read_data()