from src.cli.base import TsuCommand

class ConfigCmd(TsuCommand):
    id = 'config'
    description = 'Manage the app configuration'

    def add_arguments(self, parser):
        parser.add_argument('fake', help="Fake parameter as a test")
        parser.add_argument('-option', help="TODO!")

    def run(self, args):
        print("Config...", args)
