import subprocess
import os

class TsuCommand(object):
    id = 'default'
    description = 'Command description'

    def register_subcommand(self, subparsers):
        parser = subparsers.add_parser(self.id, description=self.description, help=self.description)
        self.add_arguments(parser)
        parser.set_defaults(command=self.run)

    def add_arguments(self, parser):
        pass

    def run(self, args):
        raise NotImplementedError()

    def execute(self, *args, **kwargs):
        """Execute the provided command using the subprocess module"""
        return subprocess.run(*args, **kwargs)

    def path(self, path):
        """Returns an absolute path given a path that is relative to the Tsu root directory"""
        return os.path.normpath( # Resolve the ../../ into a direct absolute path
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)), # The dir of our current file (eg /something/arbitrary/src/cli)
                '..', # up 2 levels
                '..',
                path # Then add the requested apth
            )
        )
