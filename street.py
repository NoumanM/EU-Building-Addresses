import csv

from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
from OSMPythonTools.nominatim import Nominatim
import sys
from countrygroups import EUROPEAN_UNION
import datetime
import string
sys.path.append("..")

nominatim = Nominatim()
overpass = Overpass()

class BuildingAddresses():
    def __init__(self):
        self.csv_file_name = 'eu-addresses.csv'

    def get_cities(self, country):
        cities = []
        try:
            areaId = nominatim.query(country)
        except:
            return
        try:
            query = overpassQueryBuilder(area=areaId, elementType='node', selector='"place"="city"')
            result = overpass.query(query)
            for j in result.elements():
                try:
                    cities.append(j.tags()['name'])
                except:
                    continue
        except:
            pass
        try:
            query = overpassQueryBuilder(area=areaId, elementType='node', selector='"place"="town"')
            result = overpass.query(query)
            for j in result.elements():
                try:
                    cities.append(j.tags()['name'])
                except:
                    continue
        except:
            pass
        try:
            query = overpassQueryBuilder(area=areaId, elementType='node', selector='"place"="village"')
            result = overpass.query(query)
            for j in result.elements():
                try:
                    cities.append(j.tags()['name'])
                except:
                    continue
        except:
            pass

        return cities

    def get_buildings(self, city, country):
        result = None
        try:
            areaId = nominatim.query(f'{city}, {country}')
        except:
            return
        print(city.capitalize())
        for i in range(3):
            try:
                query = overpassQueryBuilder(area=areaId, elementType='node',
                                             selector=f'"addr:city"~"{string.capwords(city)}"')
                result = overpass.query(query)
            except:
                continue

        if result is None:
            return
        print('Addresses found: ', result.countElements())
        final_data = []
        for j in result.elements():
            # print(j.tags())
            one_address = j.tags()
            try:
                complete_address = one_address['addr:street'] + " " + one_address['addr:housenumber'] + ", " + \
                                   one_address[
                                       'addr:postcode'] + " " + one_address['addr:city']
            except:
                continue

            final_data.append({"address": complete_address, "city": city, "postal": one_address['addr:postcode'],
                               "street": one_address['addr:street'], "country": country,
                               "country_code": self.verify_key_value('addr:country', one_address),
                               "municipality": self.verify_key_value('addr:municipality', one_address),
                               "created_at": str(datetime.date.today()), "updated_at": str(datetime.date.today()),
                               "status": "active"})

        # Open the CSV file in write mode
        with open(self.csv_file_name, 'w', newline='') as csvfile:
            fieldnames = final_data[0].keys()
            csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # Write the header row
            csv_writer.writeheader()
            csv_writer.writerows(final_data)

    def verify_key_value(self, key, address_dict):
        if key in address_dict.keys():
            value = address_dict[key]
        else:
            value = ''
        return value

    def scrape(self, country):
        cities = self.get_cities(country)
        for city in cities:
            self.get_buildings(city, country)

if __name__ == '__main__':
    building = BuildingAddresses()
    for country_name in EUROPEAN_UNION.names:
        building.scrape(country_name)
