import json
import datetime
from .system import System

class Configuration:

    def __init__(self):
        self.systems = dict()
        self.init_config()
        self.init_mappings()

    def init_config(self):
        with open('params/config.json') as c:
            self.config = json.load(c)

    def system(self, alias):
        if alias not in self.systems:
            self.systems[alias] = System(alias, self.config["jira_systems"][alias])
        return self.systems[alias]

    def result_path(self):
        if not hasattr(self, 'resultpath'):
            self.resultpath = 'result/'+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")       
        return self.resultpath

    # THIS PART OF CODE SHOULD BE REFACTORED:

    def init_mappings(self):
        if not hasattr(self, 'mappings'):
            self.mappings = dict()
            self.mappings["fields"] = Configuration.init_mapping("fields")
            self.mappings["priority"] = Configuration.init_mapping("priority")
            self.mappings["defaults"] = Configuration.init_mapping("defaults")
            self.mappings["fixversion"] = Configuration.init_mapping("fixversion")
            self.mappings["projectcode"] = Configuration.init_mapping("projectcode")
            self.mappings["costitem"] = Configuration.init_mapping("costitem")

    def init_mapping(type):
        "This method returns the Mapping from the property file."
        with open('params/'+type+'.properties.txt', 'r') as f:
            mapping = []
            for line in f:
                key,value=line.split("=")
                if not (not line or line.startswith("#")):
                    mapping.append([key.rstrip(), value.rstrip()])
        return mapping

    def get_mapping(self, key):
        return self.mappings[key]




