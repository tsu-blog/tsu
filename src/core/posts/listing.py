import datetime
import json

def handler(event, context):
    # TODO implement
    import boto3
    client = boto3.client('s3')

    s3 = boto3.resource('s3')
    bucket = s3.Bucket('tsu-posts')
    contents_dict_list = []
    for post_summary in bucket.objects.all():
        post_bucket_name = post_summary.bucket_name
        post_key = post_summary.key
        post = client.get_object(Bucket=post_bucket_name,Key=post_key)
        contents = post['Body'].read()
        contents_dict = json.loads(contents)
        contents_dict_list.append(contents_dict)
        print(contents_dict)
    return contents_dict_list

    # Someday....
    # posts = s3.readPosts()

    # return [
    #     {
    #         "id": 2,
    #         "title": "Post about something",
    #         "body": "This is my body content",
    #         "created_at": datetime.datetime.now().isoformat(),
    #         "updated_at": datetime.datetime.now().isoformat(),
    #         "created_by": "Emily"
    #     },
    #     {
    #         "id": 1,
    #         "title": "Post about another thing",
    #         "body": "你好世界",
    #         "created_at": datetime.datetime.now().isoformat(),
    #         "updated_at": datetime.datetime.now().isoformat(),
    #         "created_by": "Robert"
    #     }
    #]
