from commands.base import TsuCommand

class InitCmd(TsuCommand):
    id = 'init'
    description = 'Initialize Tsu and its dependencies - you shouldn\'t need to call this directly'

    def run(self, args):
        print("Initializing Tsu")

        print("- Setting up Virtual Environment")
        self.execute(['python3', '-m', 'venv', self.path('venv')])

        print("- Installing requirements")
        self.execute([self.path('venv/bin/pip'), 'install', '-r', self.path('requirements.txt')])
