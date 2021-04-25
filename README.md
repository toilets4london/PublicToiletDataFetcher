# PublicToiletDataFetcher

## How we get data

Most data is obtained through one of 3 methods
- A) Scraping data from council websites
- B) Spreadsheets / csv file datasets sent in by local authorities and community groups
- C) Data extracted from the crowd-sourced OpenStreetMap dataset (see Data/query.xml for the query used)

## What do the web scraping scripts do? How are they used?

The aim is to extract as much detailed public toilet data from a webpage as possible, and process it into a form that is consumable by the Toilets4London REST Api.
At the moment the workflow is that I regularly run the scripts, check their output against the previous run and see whether anything has changed.
If yes, I delete the changed toilets from the API and re-POST the new ones, or if only one or two have changed, manually update the required records.
To add new toilets, I simply POST the new batch of toilets to the Api for integration into the database.

Some of the web scraping scripts are semi-manual, meaning that they require me to use Google Maps or similar to find the lat / lng coordinates for the address.
This occurs when councils do not add lat / lng coordinates to their website (for example as they do not display a map) and don't offer full, geocodable addresses (for example if the toilet is in a park)

You can see the outputs of all the scripts in the Data/ directory. These outputs are what I will use to compare when I next run the scripts to keep the Api updated.

## What should I run to get the toilet data output shown in the Data/ directory?

Look at DataPipeline.py for a list of functions that can be called, one from each datasource-specific file, that extract toilets from the datasource and saves the extracted data to the Data/ directory.

## URLs not scraped yet

- https://new.enfield.gov.uk/services/leisure-and-culture/community-toilet-scheme/

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

## Why is there so much code repetition? Why are there so many for loops?

Because the only aim of these scripts is to be run occasionally to extract data on toilets in London. Almost no thought has been given to code quality. This is not an example of how to write clean Python data processing code 😉.