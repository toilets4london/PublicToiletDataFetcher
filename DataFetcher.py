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
import tfltoilets2
import TransportForLondonToilets
import SainsburysToilets
import WalthamForestToilets
import GreenwichToilets
import HillingdonToilets
import MertonToilets
import EalingToilets
import EnfieldToilets
import CityOfLondonToilets
import BarkingToilets
import BexleyToilets
import HackneyToilets
import HaveringToilets
import KingstonToilets
import IslingtonToilets


def osm():
    OpenStreetMapToilets.get_openstreetmap_data()
    OpenStreetMapToilets.write_filtered_json()


def barnet():
    BarnetToilets.get_all_barnet_toilets()
    BarnetToilets2.barnet_libraries_csv_to_json()


def lewisham():
    LewishamToilets.lewisham_excel_to_json()
    LewishamToilets.lewisham_json_api_to_filtered_json()


def tfl():
    tfltoilets2.get_data()
    TransportForLondonToilets.get_tfl_toilets()


class DataFetcher():

    def __init__(self):
        self.method_dict = {"City of London": CityOfLondonToilets.get_city_toilets,
                            "Barking and Dagenham": BarkingToilets.get_barking_data_from_csv,
                            "Barnet": barnet,
                            "Bexley": BexleyToilets.extract_bexley_data,
                            "Brent": BrentToilets.get_brent_toilets,
                            "Bromley": BromleyToilets.get_bromley_toilets,
                            "Camden": CamdenToilets.camden_csv_to_json,
                            "Croydon": [],
                            "Ealing": EalingToilets.get_ealing_data,
                            "Enfield": EnfieldToilets.enfield_data_to_json,
                            "Greenwich": GreenwichToilets.extract_greenwich_data,
                            "Hackney": HackneyToilets.get_hackney_data,
                            "Hammersmith and Fulham": [],
                            "Haringey": HaringeyToilets.get_haringey_data,
                            "Harrow": [],
                            "Havering": HaveringToilets.get_havering_toilets,
                            "Hillingdon": HillingdonToilets.hillingdon_csv_to_json,
                            "Hounslow": HounslowToilets.get_hounslow_toilets,
                            "Islington": IslingtonToilets.get_islington_data,
                            "Kensington and Chelsea": KensingtonChelseaToilets.kensington_data_to_json,
                            "Kingston upon Thames": KingstonToilets.get_kingston_data,
                            "Lambeth": LambethToilets.lambeth_excel_to_json,
                            "Lewisham": lewisham,
                            "Merton": MertonToilets.process_merton_data,
                            "Newham": NewhamToilets.extract_all_newham_toilets,
                            "Redbridge": RedbridgeToilets.redbridge_excel_to_json,
                            "Richmond upon Thames": RichmondToilets.get_data(),
                            "Southwark": SouthwarkToilets.get_toilets_from_csv,
                            "Sutton": SuttonToilets.sutton_excel_to_json,
                            "Tower Hamlets": [],
                            "Waltham Forest": WalthamForestToilets.extract_waltham_forest_data,
                            "Wandsworth": WandsworthToilets2.process_wandsworth_data,
                            "Westminster": WestminsterToilets.get_westminster_toilets,
                            "OpenStreetMap": osm,
                            "Healthmatic": HealthmaticToilets.healthmatic_excel_to_json,
                            "TFL": tfl,
                            "Sainsburys": SainsburysToilets.get_all_london_toilets_sainsburys}

    def fetch(self, data_source):
        if not self.method_dict.get(data_source, []):
            print(f"Data source {data_source} does not exist")
            return
        method = self.method_dict[data_source]
        method()


if __name__ == "__main__":
    fetcher = DataFetcher()
    fetcher.fetch("Lewisham")