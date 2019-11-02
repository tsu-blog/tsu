import markdown2
import datetime
import json
import boto3
from io import BytesIO
import yaml
import re
import os

from PIL import Image
from resizeimage import resizeimage

from commands.base import TsuCommand

class PublishCmd(TsuCommand):
    id = 'publish'
    description = 'Upload and publish a new post'

    def add_arguments(self, parser):
        parser.add_argument('path', help="File path of new post to be uploaded")

    def run(self, args):
        post_dir = os.path.dirname(os.path.realpath(args.path))

        s3 = boto3.resource('s3')
        cdn_bucket = s3.Bucket(self.get_cdn_bucket(args.stage))

        with open(args.path, 'r', encoding='utf-8') as fh:
            contents = fh.read()

        print("Uploading images...")
        contents = self.replace_images(contents, post_dir, cdn_bucket)

        print("Formatting post...")
        html = markdown2.markdown(contents, extras=['metadata','fenced-code-blocks','footnotes','header-ids','tables'])

        # Use post publish time if defined
        created_at = datetime.datetime.utcnow()
        if 'published' in html.metadata:
            created_at = datetime.datetime.strptime(html.metadata['published'], '%Y-%m-%d %H:%M')

        data = {
            **html.metadata,
            'created_at': created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'body': html
        }

        # Upload the post to S3
        print("Uploading post to S3...")
        bucket = s3.Bucket(self.get_posts_bucket(args.stage))
        bucket.upload_fileobj(BytesIO(json.dumps(data).encode('utf-8')), f"{data['id']}.json")

    def replace_images(self, markdown, post_dir, cdn_bucket):
        # Finds all matches for ![{alt}](./{img})({css})
        for alt, image, maxwidth in re.findall('\!\[(.*?)\]\((\.\/.+?)\)(?:\(maxwidth\=(.+?)\))?', markdown):
            images = self.upload_image_to_s3(image, post_dir, cdn_bucket)
            img_full = None
            srcset = []
            for image_path, size in images:
                if size is None:
                    img_full = image_path
                else:
                    srcset.append(f'{image_path} {size}w')
            srcset = ', '.join(srcset)

            maxwidth_val = maxwidth if len(maxwidth) > 0 else '100%'
            image_tag = f'<p style="text-align: center"><a href="{img_full}"><img src="{img_full}" alt="{alt}" srcset="{srcset}" sizes="(max-width: 480px) 100%, (max-width: 900px) 80vw, {maxwidth_val}"/></a></p>'
            if len(maxwidth) > 0:
                markdown = markdown.replace(f'![{alt}]({image})(maxwidth={maxwidth})', image_tag)
            else:
                markdown = markdown.replace(f'![{alt}]({image})', image_tag)

        return markdown

    def upload_image_to_s3(self, image_path, relative_dir, cdn_bucket, sizes=[None,320,640,1280]):
        images = []
        image_path = image_path.replace('./', '')

        with open(os.path.normpath(os.path.join(relative_dir, image_path)), 'r+b') as f:
            with Image.open(f) as image:
                for size in sizes:
                    # If size is None then we are keeping the original resolution
                    image_sized_path = os.path.join('static/','images/', image_path)
                    image_sized = image

                    if size is not None:
                        image_sized = resizeimage.resize_width(image, size, validate=False)
                        parts = image_sized_path.split('.')
                        parts[-2] = f'{parts[-2]}-{size}'
                        image_sized_path = '.'.join(parts)

                    print(">", image_sized_path)

                    # Save the image to a byte array and upload to S3
                    imgByteArr = BytesIO()
                    image_sized.save(imgByteArr, image.format)
                    imgByteArr.seek(0)

                    cdn_bucket.upload_fileobj(imgByteArr, image_sized_path, ExtraArgs={'ACL':'public-read', 'ContentType': Image.MIME[image_sized.format]})
                    images.append((f'/{image_sized_path}', size))

        return images

    def get_posts_bucket(self, stage):
        return f"{self.get_bucket_base(stage)}-posts"

    def get_cdn_bucket(self, stage):
        return f"{self.get_bucket_base(stage)}-static"

    def get_bucket_base(self, stage):
        with open(self.path("config.yml"), 'r') as fh:
            data = yaml.safe_load(fh)

        if stage in data:
            config = data[stage]
        else:
            config = data['default']

        return f"tsu-{config['domain']}-{config['name']}"
