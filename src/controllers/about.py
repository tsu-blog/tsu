from src.util import templates

def handler(event, context):
    html = templates.render('about.html', {})
    
    return {
        'statusCode': 200,
        'body': html,
        'headers': {
            'Content-Type': "text/html"
        }
    }
