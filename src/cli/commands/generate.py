from commands.base import TsuCommand
from gphotospy import authorize
from gphotospy.album import Album
from gphotospy.media import Media
from src.util.config import ConfigValues
import os
from jinja2 import Environment
from jinja2 import FileSystemLoader

class GenerateCmd(TsuCommand):
    id = 'generate'
    description = 'Generate a new post from a Google Photos album'

    def add_arguments(self, parser):
        parser.add_argument('name', help="Name of the Google Photos album")

    def run(self, args):
        album_name = args.name
        post_id = album_name.lower().replace(' ','-')
        print("Reading Album...", album_name)

        try:
            service = authorize.init("gphoto_oauth.json")
            album_manager = Album(service)

        except Exception as e:
            try:
                os.remove(self.path('photoslibrary_v1.token'))
            except:
                pass
            service = authorize.init("gphoto_oauth.json")
            album_manager = Album(service)

        print("Getting a list of albums...")
        album_iterator = album_manager.list()
        album = None
        for a in album_iterator:
            # print(a.get('id'), a.get('title'))
            if a.get('title') == album_name:
                album = a
                break

        if album is None:
            print("Failed to find album by name")
            return

        media_manager = Media(service)
        search_iterator = media_manager.search_album(album.get('id'))
        images = []
        for img in search_iterator:
            width = int(img.get('mediaMetadata').get('width'))
            height = int(img.get('mediaMetadata').get('height'))
            if width >= height:
                target_width = 2048 if width > 2048 else width
                target_height = int((target_width/width)*height)
                thumbnail_target_width = 512 if width > 512 else width
                thumbnail_target_height = int((thumbnail_target_width/width)*height)
            else:
                target_height = 2048 if height > 2048 else height
                target_width = int((target_height/height)*width)
                thumbnail_target_height = 512 if height > 512 else height
                thumbnail_target_width = int((thumbnail_target_height/height)*width)

            images.append({
                "id": img.get('id'),
                "url": ConfigValues.CDN_BASE + "/image?l=" + img.get('baseUrl')+'=w'+str(target_width),
                "width": target_width,
                "height": target_height,
                "thumbnail_url": ConfigValues.CDN_BASE + "/image?l=" + img.get('baseUrl')+'=w'+str(thumbnail_target_width),
                "thumbnail_width": thumbnail_target_width,
                "thumbnail_height": thumbnail_target_height,
                "caption": img.get('description',''),
                "aspect_ratio": width / height
            })

        data = {
            "id": post_id,
            "title": album_name,
            "cover_image": images[0]['thumbnail_url'],
            "images": images,
        }

        # Load the template
        env = Environment(loader=FileSystemLoader([self.path('src/templates/photo')]))
        template = env.get_template('google-photos-template.md')

        content = template.render(**data)

        try:
            with open(self.path(f'posts/{post_id}.md'), 'r') as fh:
                # If there is existing content, read and merge it in to our new generated gallery
                existing_content = fh.read()
                if '<div id="gallery">' in existing_content:
                    intro = existing_content.split('<div id="gallery">')[0]
                    gallery = content.split('<div id="gallery">')[1]
                    content = intro + '<div id="gallery">' + gallery
        except FileNotFoundError as e:
            pass # File not found, skip

        with open(self.path(f'posts/{post_id}.md'), 'w') as fh:
            fh.write(content)
