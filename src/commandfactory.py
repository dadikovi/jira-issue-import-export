import json
from .commands import JqlToKeyListCommand

class CommandFactory:

    @staticmethod
    def create(fsd):
        if fsd.raw["name"] == JqlToKeyListCommand.get_name():
            cmd = JqlToKeyListCommand()
            cmd.fill_data(fsd)
            return cmd


