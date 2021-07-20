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
import BarnetToilets
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
import GreenwichToilets
import HillingdonToilets
import MertonToilets
import EalingToilets
import EnfieldToilets


# HOW THIS FILE WORKS: Just uncomment the relevant line of code to extract those toilets. The output will appear in
# the Data/ directory as a nicely formatted json ready to post / upload to the Toilets4London API (unless it requires
# manual coordinate inputting) or use for any purpose. Some scripts have geocoding or reverse geocoding built in and
# so take a while to run as they use an open geocoding API. The OpenStreetMap toilets overlap with the other sources -
# Toilets4London always prefers council data sources to OpenStreetMap and Manual uploads whenever possible as these
# are easier to keep updated and are more reliable.

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
# BarnetToilets.get_all_barnet_toilets()
# BarnetToilets2.barnet_libraries_csv_to_json()
# WestminsterToilets.get_westminster_toilets()
# BrentToilets.get_all_brent_toilets()
# HaringeyToilets.get_haringey_data()
# SouthwarkToilets.get_southwark_data()
# HounslowToilets.get_hounslow_toilets()
# WandsworthToilets2.process_wandsworth_data()
# TransportForLondonToilets.get_tfl_toilets()
# LewishamToilets.lewisham_json_api_to_filtered_json()
# SainsburysToilets.get_all_london_toilets_sainsburys()
# WalthamForestToilets.extract_waltham_forest_data()
# GreenwichToilets.extract_greenwich_data()
# HillingdonToilets.hillingdon_csv_to_json()
# MertonToilets.process_merton_data()
# EalingToilets.get_ealing_data()
# EnfieldToilets.enfield_data_to_json()