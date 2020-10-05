import DataFetcher
import JsonParser
import PublicToiletCSVParser
import RichmondToilets
import SuttonToilets

# DataFetcher.get_data()
# DataFetcher.get_broader_data()
# JsonParser.write_filtered_json_osm("Data/processed_data.json")
# PublicToiletCSVParser.camden_csv_to_json()
# RichmondToilets.get_data()
# RichmondToilets.generate_clean_data_richmond("Data/processed_data_richmond.json")

SuttonToilets.sutton_excel_to_json()
