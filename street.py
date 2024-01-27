from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
from OSMPythonTools.nominatim import Nominatim
import sys
from countrygroups import EUROPEAN_UNION
sys.path.append("..")

nominatim = Nominatim()
overpass = Overpass()

class BuildingAddresses():

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



    def scrape(self, country):
        cities = self.get_cities(country)


if __name__ == '__main__':
    building = BuildingAddresses()
    for country_name in EUROPEAN_UNION.names:
        if country_name.strip() in ['Austria', 'Belgium', 'Bulgaria', 'Croatia']:
            continue
        building.scrape(country_name)
