import requests
import json
import math
import pandas
from Geocoder import reverse_geocode
from datetime import date

bfile = open("Data/boroughs.txt", "r")
BOROUGHS = bfile.read().split(", ")
bfile.close()

URL_ = "https://stores.sainsburys.co.uk/api/v1/stores/?fields=slfe-list-2.21&api_client_id=slfe&lat=51.5080&lon=0.1281&limit=25&store_type=main&sort=by_distance&within=20&facility=Toilets&page=1"


def get_sainsburys_data():
    all_data = []
    page1 = json.loads(requests.get(URL_).text)
    all_data.append(page1)
    page_meta = page1['page_meta']
    num_pages = math.ceil(page_meta['total'] / page_meta['limit'])
    for i in range(2, num_pages + 1):
        newurl = URL_.replace("page=1", "page=" + str(i))
        raw = requests.get(newurl).text
        page = json.loads(raw)
        all_data.append(page)
    print(str(len(all_data)) + " Sainsbury's branches with toilets found")
    with open("Data/sainsburys_raw.json", "w") as rawDataFile:
        json.dump(all_data, rawDataFile)
    return all_data


def get_sainsburys_data_pandas():
    pandas.set_option('display.max_columns', None)
    rawdata = requests.get(URL_).text
    jsondata = json.loads(rawdata)
    page_meta = jsondata['page_meta']
    num_pages = math.ceil(page_meta['total'] / page_meta['limit'])
    pages = pandas.json_normalize(jsondata['results'])
    for i in range(2, num_pages + 1):
        newurl = URL_.replace("page=1", "page=" + str(i))
        raw = requests.get(newurl).text
        jsonRaw = json.loads(raw)
        dataFrame = pandas.json_normalize(jsonRaw['results'])
        pages.append(dataFrame)
    return pages


def process_sainsburys_data(dataFrame):
    today = date.today()
    onlyLondon = dataFrame
    pandas.set_option('display.max_columns', None)
    onlyLondon = onlyLondon[['name', 'opening_times', 'contact.address1', 'contact.post_code', 'location.lat', 'location.lon']]
    onlyLondon = onlyLondon.rename(columns={"location.lat": "latitude", "location.lon": "longitude"})
    onlyLondon["address"] = onlyLondon["contact.address1"] + " " + onlyLondon['contact.post_code']
    usefulData = onlyLondon.drop(["contact.address1", "contact.post_code"], axis=1)
    usefulData["name"] = usefulData["name"] + " Sainsbury's"
    usefulData["data_source"] = f'Sainsburys Store Locator website {today.strftime("%d/%m/%Y")}'
    opening_hours = usefulData['opening_times'].astype(str).map(parse_opening)
    usefulData["opening_times"] = opening_hours
    usefulData = usefulData.rename(columns={"opening_times": "opening_hours"})
    result = usefulData.to_json(orient="records")
    parsed = json.loads(result)
    toilets = []
    for t in parsed:
        b = get_borough(reverse_geocode(t["latitude"], t["longitude"]))
        if b != "Other":
            t["borough"] = b
            t["wheelchair"] = True
            t["baby_change"] = True
            toilets.append(t)
    with open("Data/processed_data_sainsburys.json", "w") as sainsburysFile:
        json.dump(toilets, sainsburysFile)


def get_borough(location):
    for b in BOROUGHS:
        if b in location:
            return b
    return "Other"


DAYS = ["MON", "TUE", "WED", "THUR", "FRI", "SAT", "SUN"]


def parse_day(dayDict):
    day = DAYS[int(dayDict['day'])]
    start = dayDict['start_time']
    end = dayDict['end_time']
    return day + " " + start + "-" + end


def parse_opening(allData):
    dataDict = eval(allData)
    opening_hours_text = ""
    for day in dataDict:
        info = parse_day(day)
        opening_hours_text += info
        opening_hours_text += " , "
    return opening_hours_text[0:-2]


def get_all_london_toilets_sainsburys():
    dataFrame = get_sainsburys_data_pandas()
    process_sainsburys_data(dataFrame)


if __name__ == "__main__":
    get_all_london_toilets_sainsburys()
