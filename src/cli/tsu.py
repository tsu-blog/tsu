import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../')

import argparse
import sys
import yaml
from commands import deploy, watch, publish, update, generate
from src.util.config import ConfigValues

commands = [
    deploy.DeployCmd,
    watch.WatchCmd,
    publish.PublishCmd,
    update.UpdateCmd,
    generate.GenerateCmd
]

def load_config(args):
    with open(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'config.yml')), 'r') as fh:
        data = yaml.safe_load(fh)

    if args.stage in data:
        config = data[args.stage]
    else:
        config = data['default']

    ConfigValues.APP_NAME = config['name']
    ConfigValues.CDN_BASE = config['cdn_base']
    ConfigValues.TEMPLATE = config['template']
    ConfigValues.POSTS_BUCKET = f"tsu-{config['domain']}-{config['name']}-posts"
    ConfigValues.CDN_BUCKET = f"tsu-{config['domain']}-{config['name']}-static"
    ConfigValues.HOMEPAGE = config['homepage']
    ConfigValues.TITLE = config['title']
    ConfigValues.DESCRIPTION = config['description']
    ConfigValues.AUTHOR = config['author']
    ConfigValues.SUBSCRIBER_TABLE = f"SubscriberContactList-{config['domain']}-{config['name']}"
    ConfigValues.SUB_CONFIRM_BCC = config['sub_confirm_bcc']
    ConfigValues.CONTACT_EMAIL = config['contact_email']
    ConfigValues.CACHE_TTL = config['cache_ttl']

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Tool for managing your Tsu installation')
    parser.add_argument('-s', '--stage', choices=['prod','staging','dev'], help='Stage to run against', default='dev')
    subparsers = parser.add_subparsers(
        title="Commands",
        description="The following commands are available",
        help="Command info",
    )

    # Load up all of our commands and register them
    for commandCls in commands:
        commandCls().register_subcommand(subparsers)

    # Default to printing help if a command isn't provided
    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)


    args = parser.parse_args()

    load_config(args)

    args.command(args)
