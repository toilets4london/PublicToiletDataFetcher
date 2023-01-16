import json
import pandas as pd
from Geocoder import geocode


def to_bool_list(l):
    return [str(s).lower() == 'x' for s in l]


def read_islington_data():
    df = pd.read_excel('Data/islington_raw.xlsx')
    data = {
        "Name": list(df["Name "]),
        "Location": list(df["Location"]),
        "Male": to_bool_list(list(df["Male "])),
        "Female": to_bool_list(list(df["Female"])),
        "Gender Neutral": to_bool_list(list(df["Gender Neutral"])),
        "Disabled": to_bool_list(list(df["Disabled "])),
        "Times": list(df["Times "])
    }
    return data


def islington_excel_to_json():
    data = read_islington_data()
    with open("Data/processed_data_islington_2.json", 'w') as dataFile:
        toilets = []
        for i in range(len(data["Name"])):
            latLng = geocode(data["Name"][i]+" , " +data["Location"][i]+", Islington, London")
            if latLng != "unavailable":
                toilet = {
                    'data_source': 'Islington Council sent in spreadsheet 16/01/2023',
                    'borough': 'Islington',
                    'address': data["Location"][i].replace(" ", " "),
                    'opening_hours': data["Times"][i].replace(" ", " "),
                    'name': data["Name"][i].replace(" ", " ").replace("Libary", "Library"),
                    'baby_change': False,
                    'latitude': latLng[0],
                    'longitude': latLng[1],
                    'wheelchair': data["Disabled"][i]
                }
                toilets.append(toilet)
            else:
                print(f"Error geocoding {data['Location'][i]}")
        json.dump(toilets, dataFile)


if __name__ == "__main__":
    islington_excel_to_json()
