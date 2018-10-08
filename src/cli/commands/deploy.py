from commands.base import TsuCommand

class DeployCmd(TsuCommand):
    id = 'deploy'
    description = 'Manage and deploy services'

    def add_arguments(self, parser):
        parser.add_argument('-f', '--function', help="Specific function to deploy")

    def run(self, args):
        print("Deploying Tsu...")
        if args.function:
            self.execute(['sls', 'deploy', 'function', '-f', args.function])
        else:
            self.execute(['sls', 'deploy'])
