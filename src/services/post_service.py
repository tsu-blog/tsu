import datetime
import json
import boto3
import botocore
from concurrent import futures
from src.util.config import ConfigValues

client = boto3.client('s3', config=botocore.config.Config(max_pool_connections=10))

def list_posts():
    """Pulls all posts in our posts bucket, no limits or paging implemented yet"""
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(ConfigValues.POSTS_BUCKET)

    def get_data(s3_client, obj):
        post = s3_client.get_object(Bucket=obj.bucket_name, Key=obj.key)
        contents = post['Body'].read()
        return _load_post(contents)

    with futures.ThreadPoolExecutor(5) as executor:
        post_futures = [executor.submit(get_data, client, obj) for obj in bucket.objects.all()]

    contents_dict_list = []
    for future in futures.as_completed(post_futures):
        post = future.result()

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
