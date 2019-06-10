import datetime
import json
import boto3
client = boto3.client('s3')

# Handler loops through files in the s3 posts bucket. It collects Bucket Name and Key data in order to read the post body. It then converts the post body to JSON and appends the JSON dictionary to a running list of post contents.
def list_posts():
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('tsu-posts')

    contents_dict_list = []
    for post_summary in bucket.objects.all():
        post_bucket_name = post_summary.bucket_name
        post_key = post_summary.key
        post = client.get_object(Bucket=post_bucket_name,Key=post_key)

        contents = post['Body'].read()
        contents_dict = json.loads(contents)
        # This modifies the 'updated_at' key in the post to the 'last_modified' date of the s3 file.
        contents_dict['updated_at'] = post_summary.last_modified.isoformat()

        contents_dict_list.append(contents_dict)

    return contents_dict_list
