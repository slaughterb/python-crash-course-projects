import json
from countries import Countries
import pygal
from pygal.style import RotateStyle
from pygal.style import LightColorizedStyle

class Populations:

    def __init__(self, file_path):
        self.file_path = file_path
        self.population_data = []
        self.json_data = []
        self.countries = Countries()
        ''' store a dictionary of each country population '''
        self.country_populations = {}


    def get_category(self, population):
        ''' return a category associated with the magnitude
        of a country's population. Note that the world display categories
        are partitioned into populations of under 10 million, under 100 million,
        under a billion, and over a billion. '''
        if population >= 1000000000:
            return 0
        elif population >= 100000000:
            return 1
        elif population >= 10000000:
            return 2
        else:
            return 3

    def get_contents(self):
        ''' get the contents of the loaded data, with
         country and population separated by colon '''
        for population_dictionary in self.json_data:
            if population_dictionary["Year"] == "2010":
                country_name = population_dictionary["Country Name"]
                population = int(float(population_dictionary["Value"]))
                category = self.get_category(population)
                country_code = self.countries.get_code(country_name)
                if country_code:
                    print(country_code + ": " + str(population))
                    self.country_populations[country_code] = (population, category)
                else:
                    print("ERROR: " + country_name)
                self.population_data.append(country_name + " : " + str(population))
        return self.population_data


    def load_contents(self):
        ''' load the contents of the json information
        into a list and print the population for each country '''
        with open(self.file_path) as open_file:
            self.json_data = json.load(open_file)

    def render_contents(self):
        ''' map the population values in accordance with population.
        the 2-tuple values of country populations contains a value representing the
        population category for each country'''
        world_map_style = RotateStyle("#336699")
        world_map = pygal.maps.world.World(style=world_map_style, base_style=LightColorizedStyle)
        world_map.title = "World Population in 2010, by Country"
        world_map.add("0-10 million", {k : v[0] for k,v in self.country_populations.items() if v[1] == 3})
        world_map.add("10 million - 100 million", {k : v[0] for k,v in self.country_populations.items() if v[1] == 2})
        world_map.add("Over 100 million", {k : v[0] for k,v in self.country_populations.items() if v[1] == 1})
        world_map.add("Over a billion", {k : v[0] for k,v in self.country_populations.items() if v[1] == 0})



        world_map.render_to_file("world_population.svg")



if __name__ == "__main__":
    file_path = "population_data.json"
    world_populations = Populations(file_path)
    world_populations.load_contents()
    data_content = world_populations.get_contents()
    world_populations.render_contents()
    print(data_content)
