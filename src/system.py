from .jiraapi import JiraAPI

class System:

    def __init__(self, alias, config):
        self.alias = alias
        self.config = config

    def get_config(self, alias):
        if alias in self.config:
        	return self.config[alias]
        else:
        	return None

    def start_session(self):
    	self._session = JiraAPI.create_session(self)

    def session(self):
    	return self._session


