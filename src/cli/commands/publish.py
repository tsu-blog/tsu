from commands.base import TsuCommand

class PublishCmd(TsuCommand):
    id = 'publish'
    description = 'Upload and publish a new post'

    def add_arguments(self, parser):
        parser.add_argument('path', help="File path of new post to be uploaded")

    def run(self, args):
        print("Publish...")
        print(args.path)
