from .commandfactory import CommandFactory
from .flowvalidationexception import FlowValidationException
from .system import System
import json

class Flow:

    def __init__(self):
        self.parse()

    def parse(self):
        self.load_json()
        self.init_step_list()
        self.init_system_list()
        
        for step_raw in self.json_format["steps"]:
            fsd = FlowStepData()
            fsd.raw = step_raw
            fsd.id = self.generate_unique_id()
            self.steps.append(CommandFactory.create(fsd))

        for alias, config in self.json_format["jira_systems"].items():
            self.systems[alias] = System(alias, config)

        print("INFO - flow parsed successfully.")
    
    def init_step_list(self):
        if not hasattr(self, "steps"):
            self.steps = list()
        
        return self.steps

    def init_system_list(self):
        if not hasattr(self, "systems"):
            self.systems = dict()
        
        return self.systems

    def load_json(self):
        if not hasattr(self, "json_format"):
            with open('params/flow.json') as c:
                self.json_format = json.load(c)
        
        return self.json_format

    def execute(self):
        self.init_systems()
        for step in self.steps:
            self.execute_step(step)
        return

    def execute_step(self, step):
        requirements = step.get_requirement_dict()

        for key, value in requirements["systems"].items():

            requirements["systems"][key] = self.systems[value]

        step.execute(requirements)

    def init_systems(self):
        for name, system in self.systems.items():
            system.start_session()
    
    def validate(self):
        try:
            self.validate_config()
            self.validate_connections()
        except FlowValidationException as e:
            print("ERROR- Validation error: " + str(e))
            return
        print("INFO - flow validated successfully.")

    def validate_config(self):
        for step in self.steps:
            step.validate_config()
            step.validate_systems()

    def validate_connections(self):
        # ...
        return
    
    def generate_unique_id(self):
        if hasattr(self, "seq"):
            self.seq = self.seq+1
        else:
            self.seq = 1
        return self.seq

class FlowStepData:
    def set_raw(self, raw):
        self.raw = raw
    def set_id(self, id):
        self.id = id
    
    def raw(self):
        if hasattr(self, "raw"):
            return self.raw
        else:
            self.raw = dict()
            return self.raw
    def id(self):
        if hasattr(self, "id"):
            return self.id
        else:
            self.id = -1
            return self.id

        


