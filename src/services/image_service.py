import datetime
import json
import boto3
from src.util.config import ConfigValues
import requests
import os
import hashlib
client = boto3.client('s3')

def get_image(url):
    """Load a single post by ID"""
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(ConfigValues.CDN_BUCKET)
    key = hashlib.sha256(url.encode('utf-8')).hexdigest()
    image_s3_path = os.path.join('static/', 'images/', 'gphoto_cache/', key)
    print("Trying", url, image_s3_path)

    try:
        file = bucket.Object(image_s3_path).get()
        print("Found file", image_s3_path)
    except Exception as e:
        print("Requesting image", url, image_s3_path)
        # We don't have the file, try downloading
        r = requests.get(url, stream=True)
        if r.status_code != 200:
            raise Exception("Image download failed")

        bucket.upload_fileobj(
            r.raw,
            image_s3_path,
            ExtraArgs={'ACL':'public-read', 'ContentType': 'image/jpeg'}
        )
        file = bucket.Object(image_s3_path).get()
        print("Image uploaded", url, image_s3_path)

    return file['Body'].read(), 'image/jpeg'
