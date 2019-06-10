from commands.base import TsuCommand

class DeployCmd(TsuCommand):
    id = 'deploy'
    description = 'Manage and deploy services'

    def add_arguments(self, parser):
        parser.add_argument('-f', '--function', help="Specific function to deploy")

    def run(self, args):
        print("Deploying Tsu...")
        additional_args = []
        if args.function:
            additional_args.extend(['function', '-f', args.function])

        if args.stage:
            additional_args.extend(['--stage', args.stage])

        self.execute(['sls', 'deploy', *additional_args])
