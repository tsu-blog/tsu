from src.cli.base import TsuCommand

class DeployCmd(TsuCommand):
    id = 'deploy'
    description = 'Manage and deploy services'

    def run(self, args):
        print("Deploying Tsu...")
        self.execute(['sls', 'deploy'])
