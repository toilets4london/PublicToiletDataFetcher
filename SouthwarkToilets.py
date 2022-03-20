import json
import pandas as pd
from Helpers import ENtoLL84


# CSV downloaded from https://geo.southwark.gov.uk/connect/analyst/mobile/#/main?mapcfg=Southwark%20Public%20Toilets

def get_toilets_from_csv():
    df = pd.read_csv('./Data/southwark_toilets.csv')
    df = df.fillna("")
    data = df.to_dict(orient="records")
    toilets = []
    for entry in data:
        lng, lat = ENtoLL84(entry["Easting"], entry["Northing"])
        toilets.append({
            "name": entry["Name"],
            "address": entry["Location"] + " " + entry["AdditionalInfo"],
            "opening_hours": entry["OpeningTime"],
            "fee": entry["CostCharge"],
            "baby_change": "Y" in entry["BabyChangingFacilities"].upper(),
            "wheelchair": "Y" in entry["DisabledFacilities"].upper(),
            "latitude": lat,
            "longitude": lng,
            "data_source": "Downloaded from https://geo.southwark.gov.uk/ on 10/08/2021",
            "borough": "Southwark"
        })
    with open("Data/processed_data_southwark.json", "w") as jsonFile:
        json.dump(toilets, jsonFile)


if __name__ == "__main__":
    get_toilets_from_csv()