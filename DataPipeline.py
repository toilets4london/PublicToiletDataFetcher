import DataFetcher
import JsonParser
import PublicToiletCSVParser

# DataFetcher.get_data()
# DataFetcher.get_broader_data()
JsonParser.write_filtered_json_osm("Data/filtered_data.json")
PublicToiletCSVParser.camden_csv_to_json()