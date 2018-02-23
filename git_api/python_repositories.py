import requests
import pygal
from pygal.style import LightColorizedStyle
from pygal.style import LightenStyle

class Repositories():
    '''
    class containing the data representation of a series of
    repositories requested via a git API call. This class
    takes a url parameter for their API, gathers the json,
    then visualizes the yielded data, sorted by # watchers
    '''

    def __init__(self, url):
        self.url = url
        # dictionary containing json response from API call
        self.response_data = self.load_data()
        self.response_list = self.response_data["items"]
        self.get_call_information()
        self.print_first_n_repositories(5)



    def print_repository(self, repository_dict):
        ''' takes a repository from the list of API
        responses and prints information about the
        particular project '''
        try:
            print("\nREPOSITORY INFORMATION:")
            print("Name: " + repository_dict["name"])
            print("Owner: " + repository_dict["owner"]["login"])
            print("Repository: " + repository_dict["owner"]["html_url"])
            print("Description: " + repository_dict["description"])
            print("Watchers: " + str(repository_dict["watchers"]))
        except TypeError:
            print("ERROR: Repository returned NoneType.")

    def print_first_n_repositories(self, n):
        ''' prints the first n resulting repositories resulting from an
        API call; relies on print_repository as a helper function. Requires
        that the API response has at least n repositories'''
        try:
            print("*" * (38 + len(str(n))))
            print("*INFORMATION FOR FIRST " + str(n) + " REPOSITORIES:*")
            print("*" * (38 + len(str(n))))
            for repo in range(n):
                self.print_repository(self.response_list[repo])
        except TypeError:
            print("ERROR: Repository returned NoneType.")

    def load_data(self):
        ''' intends to load json information from API request '''
        self.request_data = requests.get(self.url)
        return self.request_data.json()

    def get_call_information(self):
        ''' prints general results from API call '''
        print("Status: " + str(self.request_data.status_code))
        print("Total repositories: " + str(self.response_data["total_count"]))
        print("Responses returned: " + str(len(self.response_list)))
        print()

    def visualize(self):
        ''' visualize the repository name/watchers data using pygal '''
        names = []
        watchers = []
        for repository in self.response_list:
            names.append(repository["name"])
            watchers.append(repository["watchers"])
        graph_style = LightenStyle("#333366", base_style=LightColorizedStyle)

        configuration = pygal.Config()
        configuration.x_label_rotation = 45
        configuration.show_legend = False
        configuration.title_font_size = 25
        configuration.label_font_size = 15
        configuration.major_label_font_size = 18
        configuration.truncate_label = 15
        configuration.show_y_guides = False
        configuration.width = 800

        graph = pygal.Bar(configuration, style=graph_style)


        graph.title = "Most Watched Python Projects on GitHub"
        graph.x_labels = names
        graph.add("", watchers)
        graph.render_to_file("python_repositories.svg")


if __name__ == "__main__":
    url = "https://api.github.com/search/repositories?q=language:python&sort=stars"
    python_repos = Repositories(url)
    python_repos.visualize()