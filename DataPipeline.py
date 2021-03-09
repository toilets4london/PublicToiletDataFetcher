import OpenStreetMapToilets
import CamdenToilets
import RichmondToilets
import SuttonToilets
import RedbridgeToilets
import LewishamToilets
import LambethToilets
import HealthmaticToilets
import KensingtonChelseaToilets
import BromleyToilets
import NewhamToilets
import BarnetToilets2
import WestminsterToilets
import BrentToilets
import HaringeyToilets
import SouthwarkToilets
import HounslowToilets
import WandsworthToilets2
import TransportForLondonToilets
import SainsburysToilets
import WalthamForestToilets


# HOW THIS FILE WORKS: Just uncomment the relevant line of code to extract those toilets. The output will appear in the
# Data/ directory as a nicely formatted json ready to post / upload to the Toilets4London API or use for any purpose
# Some scripts have geocoding or reverse geocoding built in and so take a while to run as they use an open geocoding API
# The OpenStreetMap toilets overlap with the other sources - Toilets4London always prefers council data sources to
# OpenStreetMap and Manual uploads whenever possible as these are easier to keep updated

# OpenStreetMapToilets.get_openstreetmap_data()
# OpenStreetMapToilets.write_filtered_json()
# CamdenToilets.camden_csv_to_json()
# RichmondToilets.get_richmond_data()
# RichmondToilets.write_cleaned_data_richmond()
# SuttonToilets.sutton_excel_to_json()
# RedbridgeToilets.redbridge_excel_to_json()
# LewishamToilets.lewisham_excel_to_json()
# LambethToilets.lambeth_excel_to_json()
# HealthmaticToilets.healthmatic_excel_to_json()
# KensingtonChelseaToilets.kensington_data_to_json()
# BromleyToilets.extract_bromley_json()
# NewhamToilets.extract_all_newham_toilets()
# BarnetToilets2.barnet_libraries_csv_to_json()
# WestminsterToilets.westminster_csv_to_json()
# BrentToilets.get_all_brent_toilets()
# HaringeyToilets.get_haringey_data()
# SouthwarkToilets.get_southwark_data()
# HounslowToilets.get_hounslow_toilets()
# WandsworthToilets2.process_wandsworth_data()
# TransportForLondonToilets.get_tfl_toilets()
# LewishamToilets.lewisham_json_api_to_filtered_json()
# SainsburysToilets.get_all_london_toilets_sainsburys()
WalthamForestToilets.extract_waltham_forest_data()