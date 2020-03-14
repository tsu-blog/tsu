import os
from src.util.config import ConfigValues

from jinja2 import Environment
from jinja2 import FileSystemLoader

def render(template, data):
    # Pull the path to our /custom/templates directory
    custom_template_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..',  '..', 'custom', 'templates')

    # Pull the path to the configured built-in template
    templates_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'templates')
    base_template_dir = os.path.join(templates_dir, ConfigValues.TEMPLATE)

    # Load the template
    env = Environment(loader=FileSystemLoader([custom_template_dir, base_template_dir]))
    template = env.get_template(template)

    # Add in some default keys to our data
    data.update({
        'cdn_base': ConfigValues.CDN_BASE,
        'cache_buster': ConfigValues.DEPLOYMENT_ID,
        'homepage': ConfigValues.HOMEPAGE,
        'title': ConfigValues.TITLE,
        'description': ConfigValues.DESCRIPTION,
        'author': ConfigValues.AUTHOR
    })

    return template.render(**data)
