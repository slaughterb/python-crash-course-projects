from pygal.maps.world import COUNTRIES

class Countries:

    def __init__(self):
        self.country_data = []

    def print_countries(self):
        ''' prints out each of the country codes
        along side each of the country names'''
        for code in sorted(COUNTRIES.keys()):
            print(code, COUNTRIES[code])

    def get_code(self, country):
        ''' return the country code pygal associates with the
        country's actual name'''
        for country_code, country_name in COUNTRIES.items():
            if country_name == country:
                return country_code
        return None