import datetime
import json
import boto3
from src.util.config import ConfigValues

client = boto3.client('s3')

def list_posts():
    """Pulls all posts in our posts bucket, no limits or paging implemented yet"""
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(ConfigValues.POSTS_BUCKET)

    contents_dict_list = []
    for post_summary in bucket.objects.all():
        post = client.get_object(Bucket=post_summary.bucket_name, Key=post_summary.key)

        contents = post['Body'].read()
        post = _load_post(contents)

        # Only show posts in the listing if they are published
        if post.get('status', 'published') == 'published':
            contents_dict_list.append(post)

    return sorted(contents_dict_list, key=lambda p: p['created_at'], reverse=True)

def get_post(id):
    """Load a single post by ID"""
    s3 = boto3.resource('s3')
    post = s3.Object(ConfigValues.POSTS_BUCKET, f'{id}.json')
    contents = post.get()['Body'].read()
    return _load_post(contents)

def _load_post(post_str):
    """Internal method that turns a post from a json string into a python object"""
    post = json.loads(post_str.decode('utf-8'))
    post['created_at'] = datetime.datetime.strptime(post['created_at'], "%Y-%m-%d %H:%M:%S")

    return post
