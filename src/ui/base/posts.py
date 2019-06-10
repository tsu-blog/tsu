import json
import datetime
from src.util import service_mesh, templates

def handler(event, context):
    api_response = service_mesh.call('api-posts')

    return {
        'statusCode': 200,
        'body': templates.render('posts.html', {
            'posts': api_response['posts'],
            'time': datetime.datetime.utcnow().isoformat()
        }),
        'headers': {
            'Content-Type': "text/html"
        }
    }
