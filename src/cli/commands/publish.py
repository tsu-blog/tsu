import markdown2
import datetime
import json
import boto3
import hashlib
from io import BytesIO
import re
import os

from PIL import Image
from resizeimage import resizeimage

from commands.base import TsuCommand

class PublishCmd(TsuCommand):
    id = 'publish'
    description = 'Upload and publish a new post'
    config = None

    def add_arguments(self, parser):
        parser.add_argument('path', help="File path of new post to be uploaded")

    def run(self, args):
        post_dir = os.path.dirname(os.path.realpath(args.path))

        s3 = boto3.resource('s3')
        cdn_bucket = s3.Bucket(self.get_cdn_bucket(args.stage))
        cdn_base_url = self.get_config(args.stage, 'cdn_base')

        # Read in the contents of the blog post so we can process it
        with open(args.path, 'r', encoding='utf-8') as fh:
            contents = fh.read()

        print("Uploading images...")
        contents = self.replace_images(contents, post_dir, cdn_bucket, cdn_base_url)

        print("Formatting post into HTML...")
        html = markdown2.markdown(contents, extras=['metadata','fenced-code-blocks','footnotes','header-ids','tables'])

        if 'thumbnail' in html.metadata:
            print("Uploading thumbnail...")
            images = self.upload_image_to_s3(html.metadata['thumbnail'], post_dir, cdn_bucket, sizes=[(1200, 628)])
            path, size = images[0]
            html.metadata['thumbnail'] = f'{cdn_base_url}/{path}'

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

    def replace_images(self, markdown, post_dir, cdn_bucket, cdn_base_url):
        """Find all of the images in this post, upload to s3, and replace the tag
        with HTML version of the image"""

        # Finds all matches for ![{alt}](./{img})({css})
        for alt, image, maxwidth in re.findall('\!\[(.*?)\]\((\.\/.+?)\)(?:\(maxwidth\=(.+?)\))?', markdown):
            images = self.upload_image_to_s3(image, post_dir, cdn_bucket)

            # Pull out the full sized image url + a list of all of the resized versions
            # for our srcset
            img_full = None
            srcset_arr = []
            for image_path, size in images:
                image_url = f'{cdn_base_url}/{image_path}'

                if size == (None, None):
                    img_full = image_url
                else:
                    srcset_arr.append(f'{image_url} {size[0]}w')

            # Generate the HTML for this image
            srcset = ', '.join(srcset_arr)
            maxwidth_val = maxwidth if len(maxwidth) > 0 else '100%'
            image_tag = f'''
<p style="text-align: center">
    <a href="{img_full}">
        <img src="{img_full}" alt="{alt}" srcset="{srcset}" style="width: 100%; max-width: {maxwidth_val};"/>
    </a>
</p>
            '''

            # Replace the tag with the html for this image
            if len(maxwidth) > 0:
                markdown = markdown.replace(f'![{alt}]({image})(maxwidth={maxwidth})', image_tag)
            else:
                markdown = markdown.replace(f'![{alt}]({image})', image_tag)

        return markdown

    def upload_image_to_s3(self, image_path, relative_dir, cdn_bucket, sizes=[(None,None),(320,None),(640,None),(1280,None)]):
        """Uploads the provided image into S3 in multiple sizes if the file doesn't already exist.
        Returns an array of (path, width) tuples"""
        image_path = image_path.replace('./', '')

        with open(os.path.normpath(os.path.join(relative_dir, image_path)), 'r+b') as f:
            with Image.open(f) as image:
                image_s3_path = os.path.join('static/', 'images/', image_path)
                images = [(self.add_suffix_to_filename(image_s3_path, size[0]), size) for size in sizes]

                # If the hash of the image locally matches what is in s3, there
                # is no need to upload again so return immediately
                local_hash = self.md5_checksum(self.img_to_bytes(image))
                s3_hash = self.get_s3_etag(cdn_bucket, image_s3_path)
                if local_hash == s3_hash:
                    # Finally check that the files for all of the sizes we are going
                    # to make exist as well
                    tags = [self.get_s3_etag(cdn_bucket, path) for path, size in images]
                    if None not in tags:
                        return images

                for (path, size) in images:
                    # If size is None then we are keeping the original resolution
                    image_sized = image
                    if size != (None, None):
                        x, y = size
                        if x is not None and y is not None:
                            image_sized = resizeimage.resize_cover(image, [x, y], validate=False)
                        elif y is not None:
                            image_sized = resizeimage.resize_height(image, y, validate=False)
                        else:
                            image_sized = resizeimage.resize_width(image, x, validate=False)

                    # Save the image to a byte array and upload to S3
                    print("> Uploading", path)
                    cdn_bucket.upload_fileobj(
                        self.img_to_bytes(image_sized),
                        path,
                        ExtraArgs={'ACL':'public-read', 'ContentType': Image.MIME[image_sized.format]}
                    )

        return images

    def add_suffix_to_filename(self, path, suffix):
        """Takes in a filename string and appends the suffix before the file extension
        Eg `files/name.png` -> `files/name-{suffix}.png`
        """
        parts = path.split('.')

        if suffix is not None:
            parts[-2] = f'{parts[-2]}-{suffix}'

        return '.'.join(parts)

    def get_posts_bucket(self, stage):
        """Returns the S3 bucket that posts are stored in"""
        return f"{self.get_bucket_base(stage)}-posts"

    def get_cdn_bucket(self, stage):
        """Returns the S3 bucket that static assets (css, images, etc) are stored in"""
        return f"{self.get_bucket_base(stage)}-static"

    def get_bucket_base(self, stage):
        return f"tsu-{self.get_config(stage, 'domain')}-{self.get_config(stage, 'name')}"

    def get_s3_etag(self, bucket, s3_path):
        """Looks up the ETag value for the given S3 object (the MD5 hash of the file in S3).
        Returns None if the object is not found"""
        try:
            return bucket.Object(s3_path).e_tag[1:-1]
        except Exception as e:
            return None

    def img_to_bytes(self, image):
        """Converts the PIL Image object provided into a BytesIO object"""
        img_bytes = BytesIO()
        image.save(img_bytes, image.format)
        img_bytes.seek(0)

        return img_bytes

    def md5_checksum(self, file):
        """Calculates the MD5 checksum of the provided stream"""
        m = hashlib.md5()

        for data in iter(lambda: file.read(1024 * 1024), b''):
            m.update(data)

        return m.hexdigest()
