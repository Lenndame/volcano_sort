""" 
Lese die Datei active_volcanos.csv ein und filtere
die Einträge nach Land (zb. Italy).
Die gefilterten Einträge kommen in eine entsprechende
json-Datei (zb. data/volcanos_italy.json).
Es sollen nur Vulkane berücksichtigt werden, für die gilt:
risk != NULL

Die Json-Einträge sollen enthalten:
Name des Vulkans
Risiko
Latitude
Longitude
Country
Region

die Json-Keys sollen folgende Namen haben:
name, risk, lat, long, country, region

zb. als Array von Objekten

[
    {
        "name": "Farallon de Pajaros",
        "latitude": "20.538000000000000",
        "longitude": "144.895999999999000",
        "risk": "1",
        "country": "United States",
        "region": "Japan, Taiwan, Marianas"
    },
    {..},


]
"""

import csv
from pathlib import Path
import json

def load_volcanos(filename):
    with open(Path(__file__).parent / filename, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=",")
        result = list(reader)
        result = [row for row in result if all(key in row for key in ["V_Name", "Country", "Region", "Latitude", "Longitude", "risk"])]
        # required_keys = ["V_Name", "Country", "Region", "Latitude", "Longitude", "risk"]
        # valid_rows = []
        # for row in result:
        #   is_valid = True
        #   for key in required_keys:
        #       if key not in row:
        #           is_valid = False
        #           break
        #   if is_valid:
        #     valid_rows.append(row)
    return result


def filter_volcanos(reader_sort, filter_country):
    result = list(filter(lambda e: e["Country"] in filter_country, reader_sort))
    result = list(filter(lambda e: e["risk"] != "Null", result))
    return result


def format_volcanos(volcanos):
    for volcano in volcanos:
        volcano.update({
            "name": volcano.pop("V_Name"),
            "risk": volcano["risk"],
            "lat": volcano.pop("Latitude"),
            "long": volcano.pop("Longitude"),
            "country": volcano.pop("Country"),
            "region": volcano.pop("Region")
        })
    return volcanos


def save_volcanos_to_file(filename_name, liste_filtered):
    with open(Path(__file__).parent / filename_name, mode="w", newline="", encoding="utf-8") as f:
        json.dump(liste_filtered, f)


def main():
    country_input = input("Nach welchem Land filtern?: ").split(",")
    save_volcanos_to_file(f"volcanos_{'-'.join(country_input)}.json", format_volcanos(filter_volcanos(load_volcanos("active_volcanos.csv"), country_input)))
    

main()
