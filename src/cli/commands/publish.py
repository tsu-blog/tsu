import markdown2
import datetime
import json
import boto3
from io import BytesIO
import yaml

from commands.base import TsuCommand

class PublishCmd(TsuCommand):
    id = 'publish'
    description = 'Upload and publish a new post'

    def add_arguments(self, parser):
        parser.add_argument('path', help="File path of new post to be uploaded")

    def run(self, args):
        print("Formatting post...")
        with open(args.path, 'r', encoding='utf-8') as fh:
            contents = fh.read()

        html = markdown2.markdown(contents, extras=['metadata','fenced-code-blocks','footnotes','header-ids','tables'])
        data = {
            **html.metadata,
            'created_at': datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'body': html
        }

        # Upload the post to S3
        print("Uploading post to S3...")
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(self.get_bucket(args.stage))
        bucket.upload_fileobj(BytesIO(json.dumps(data).encode('utf-8')), f"{data['id']}.json")

    def get_bucket(self, stage):
        with open(self.path("config.yml"), 'r') as fh:
            data = yaml.safe_load(fh)

        if stage in data:
            config = data[stage]
        else:
            config = data['default']
            stage = 'dev'

        return f"tsu-{config['domain']}-{stage}-posts"
