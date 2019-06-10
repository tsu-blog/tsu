import os
from jinja2 import Environment
from jinja2 import FileSystemLoader

def render(template, data):
    templates_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..',  'ui', 'templates')

    # TODO make this configurable
    active_template = os.path.join(templates_dir, 'tsu-night')

    env = Environment(loader=FileSystemLoader(active_template))

    template = env.get_template(template)
    return template.render(**data)
