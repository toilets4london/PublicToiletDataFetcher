"""
Unfortunately this data is probably very unreliable
Comes from a 2014 request for public information
https://www.whatdotheyknow.com/request/information_regarding_public_toi_4
No more recent info found on Barking and Dagenham website
"""

import pandas as pd
import json
from Helpers import ENtoLL84


def get_barking_data_from_csv():
    data = pd.read_csv("Data/barking_raw.csv").to_dict(orient="records")
    toilets = []
    for d in data:
        lng, lat = ENtoLL84(d['Grid Ref X'], d['Grid Ref Y '])
        toilets.append({
            "latitude": lat,
            "longitude": lng,
            "address": f'{d["Location "]} {d["Postcode"]}',
            "wheelchair": "y" in d["Accessible "].lower(),
            "baby_change": "y" in d["Baby Change"].lower(),
            "fee": "" if d["Charge Amount"] == "none" else d["Charge Amount"],
            "opening_hours": f'{d["OpeningHours"]}; {"Radar key accessible" if "y" in d["Radar Key "].lower() else ""}',
            "borough": "Barking and Dagenham",
            "data_source": "2014 Freedom of Info request (very old I know - please report toilet if inaccurate)"
        })
    with open("Data/processed_data_barking.json", "w") as jsonfile:
        json.dump(toilets, jsonfile)


if __name__ == "__main__":
    get_barking_data_from_csv()
