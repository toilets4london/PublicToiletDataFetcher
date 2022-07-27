# PublicToiletDataFetcher

## How we get data

Most data is obtained through one of 3 methods
- A) Scraping data from council websites
- B) Spreadsheets / csv file datasets sent in by local authorities and community groups
- C) Data extracted from the crowd-sourced OpenStreetMap dataset (see Data/query.xml for the query used)

## Address geocoding

- Some data sources come with lat / lng coords but some don't
- For those that don't I geocode the addresses
- If you add a google geocoding API key to `api_key.txt` the google geocoding API will be used for geocoding, otherwise it will default to Nominatim geocoding

## What do the web scraping scripts do? How are they used?

The aim is to extract as much detailed public toilet data from a webpage as possible, and process it into a form that is consumable by the Toilets4London REST Api.
At the moment the workflow is that I regularly run the scripts, check their output against the previous run and see whether anything has changed.
If yes, I delete the changed toilets from the API and re-POST the new ones, or if only one or two have changed, manually update the required records.
To add new toilets, I simply POST the new batch of toilets to the Api for integration into the database.

Some of the web scraping scripts are semi-manual, meaning that they require me to use Google Maps or similar to find the lat / lng coordinates for the address.
This occurs when councils do not add lat / lng coordinates to their website (for example as they do not display a map) and don't offer full, geocodable addresses (for example if the toilet is in a park).

You can see the outputs of all the scripts in the Data/ directory. These outputs are what I will use to compare when I next run the scripts to keep the API updated. Git diffs help a lot with this.

## What should I run to get the toilet data output shown in the Data/ directory?

`DataFetcher.py` has a dictionary of functions that can be called to extract data from the various sources

## Output format

- Data should be processed to end up in the following format, so that it can be uploaded to the toilets4london API

```json
  {
    "data_source": "[URL] [DATE]/ Data sent in by [ORGANISATION] on [DATE]",
    "borough": "[See Data/boroughs.txt for acceptable borough names]",
    "address": "2-6 Woodgrange Road London E7 0QH",
    "opening_hours": "7am-6pm Monday to Friday",
    "name": "The Gate Community Neighbourhood Centre and Library",
    "baby_change": true,
    "latitude": 51.5485568,
    "longitude": 0.024924,
    "wheelchair": true,
    "fee": "20p",
    "open": true
  }
```

- If the toilet is currently closed but may be open in the future, the `open` field can be set to `false`
- If fee is left out, it defaults to a free toilet
- `borough`, `latitude` and `longitude` are required fields

## Boroughs with dedicated scripts

If unchecked this means I could neither find a reliable way to extract toilet data from that council's website / another data source using a script, nor did that council send me a dataset.
This doesn't mean I have no data for that borough. It just means instead I use the generic sources listed below, manual uploads and locations suggested through the app.

- [x] City of London
- [x] Barking and Dagenham
- [x] Barnet
- [x] Bexley
- [x] Brent
- [x] Bromley
- [x] Camden
- [ ] Croydon
- [x] Ealing
- [x] Enfield
- [x] Greenwich
- [x] Hackney
- [ ] Hammersmith and Fulham
- [x] Haringey
- [ ] Harrow
- [x] Havering
- [x] Hillingdon
- [x] Hounslow
- [ ] Islington
- [x] Kensington and Chelsea
- [ ] Kingston upon Thames
- [x] Lambeth
- [x] Lewisham
- [x] Merton
- [x] Newham
- [x] Redbridge
- [x] Richmond upon Thames
- [x] Southwark
- [x] Sutton
- [ ] Tower Hamlets
- [x] Waltham Forest
- [x] Wandsworth
- [x] Westminster

## TODO

### Writing

- Islington
- Kingston upon Thames

### Updating

- Barking
- Barnet
- Camden
- Hillingdon
- Lambeth
- Lewisham
- Merton
- Newham
- Redbridge
- Richmond
- Southwark
- Sutton
- Wandsworth

## Information regarding missing boroughs (last updated 27/07/2022)

### Croydon

[Croydon council's website](https://www.croydon.gov.uk/parking-streets-and-transport/street-maintenance-repairs-and-improvements/street-cleaning/public-conveniences) says
 
> Due to ongoing concerns in relation to the COVID-19 pandemic Croydon Council are not currently in a position to introduce the planned Community Toilet Scheme across the borough.

and also 

>  Croydon Council will provide an update on the Community Toilet Scheme in due course.

### Hammersmith and Fulham, Harrow, Tower Hamlets

Couldn't find any good primary sources to scrape data from for these boroughs - let me know if you do :)

## Other data sources

- Healthmatic (public toilet contractor) sent in a spreadsheet
- Sainsbury's store locator website
- Transport for London API
- OpenStreetMap

## Credits

- All OpenStreetMap data is © OpenStreetMap contributors
- OpenStreetMap data is available under the Open Database Licence