import markdown2
import datetime
import json

from commands.base import TsuCommand

class PublishCmd(TsuCommand):
    id = 'publish'
    description = 'Upload and publish a new post'

    def add_arguments(self, parser):
        parser.add_argument('path', help="File path of new post to be uploaded")

    def run(self, args):
        with open(args.path, 'r') as fh:
            contents = fh.read()

        html = markdown2.markdown(contents, extras=['metadata','fenced-code-blocks','footnotes','header-ids','tables'])
        data = {
            **html.metadata,
            'created_at': datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'body': html
        }

        with open(f"example-posts/{data['id']}.json", 'w+') as fh:
            fh.write(json.dumps(data))
