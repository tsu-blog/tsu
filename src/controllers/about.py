from src.util import templates

def handler(event, context):
    return {
        'statusCode': 200,
        'body': templates.render('about.html', {
        }),
        'headers': {
            'Content-Type': "text/html"
        }
    }
