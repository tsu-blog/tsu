import os
from src.util.config import ConfigValues

from jinja2 import Environment
from jinja2 import FileSystemLoader

def render(template, data):
    # Load the template
    templates_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..',  'ui', 'templates')
    active_template_dir = os.path.join(templates_dir, ConfigValues.TEMPLATE)
    env = Environment(loader=FileSystemLoader(active_template_dir))
    template = env.get_template(template)

    # Add in some default keys to our data
    data.update({
        'cdn_base': ConfigValues.CDN_BASE,
        'cache_buster': ConfigValues.DEPLOYMENT_ID,
    })

    return template.render(**data)
