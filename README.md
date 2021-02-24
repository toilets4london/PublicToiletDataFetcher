# PublicToiletDataFetcher

## How we get data

Most data is obtained through one of 3 methods
- A) Scraping data from council websites
- B) Spreadsheets / csv file datasets sent in by local authorities and community groups
- C) Data extracted from the crowd-sourced OpenStreetMap dataset (see Data/query.xml for the query used)

## URLs not scraped yet 

### Commercial

The following URL should be scraped for Sainsbury's toilets
- https://stores.sainsburys.co.uk/api/v1/stores/?fields=slfe-list-2.21&api_client_id=slfe&lat=51.579676&lon=-0.11116759999999999&limit=100&store_type=main%2Clocal&sort=by_distance&within=15&facility=Toilets&page=1

### Community toilet schemes

- https://new.enfield.gov.uk/services/leisure-and-culture/community-toilet-scheme/
- https://www.ealing.gov.uk/info/201153/street_care_and_cleaning/200/public_toilets/4
- https://www.merton.gov.uk/streets-parking-transport/community-toilet-scheme
- https://www.walthamforest.gov.uk/content/public-toilets
  
### Public toilets

- https://www.royalgreenwich.gov.uk/info/200258/parking_transport_and_streets/810/find_a_public_toilet_in_greenwich
- https://www.bexley.gov.uk/services/parking-transport-and-streets/public-toilets/reporting-issues-public-toilets

## Processing

- Data should be processed to end up in the following format, so that it can be uploaded to the toilets4london API

```json
  {
    "data_source": "Extracted from [URL] on [DATE]/ Data sent in by [COUNCIL] on [DATE]",
    "borough": "[See Data/boroughs.txt for acceptable borough names]",
    "address": "2-6 Woodgrange Road London E7 0QH",
    "opening_hours": "7am-6pm Monday to Friday",
    "name": "The Gate Community Neighbourhood Centre and Library",
    "baby_change": true,
    "latitude": 51.5485568,
    "longitude": 0.024924,
    "wheelchair": true,
    "covid": "Some text confirming how the toilet is affected by covid restrictions / lockdown (if needed)",
    "fee": "20p",
    "open": true
  }
```

- If the toilet is currently closed but may be open in the future, the `open` field can be set to `false`
- If fee is left out, it defaults to a free toilet
- `borough`, `latitude` and `longitude` are required fields

## Credits

- All OpenStreetMap data is © OpenStreetMap contributors
- OpenStreetMap data is available under the Open Database Licence

