import subprocess
import os
import shutil
import platform

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

    def execute(self, command, capture_output=False, **kwargs):
        """Execute the provided command using the subprocess module"""
        command[0] = shutil.which(command[0]) # Lookup the command using PATH (windows doesn't do this by default)
        if capture_output:
            return subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs)
        else:
            return subprocess.run(command, **kwargs)

    def path(self, path):
        """Returns an absolute path given a path that is relative to the Tsu root directory"""
        return os.path.normpath( # Resolve the ../../ into a direct absolute path
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)), # The dir of our current file (eg /something/arbitrary/src/cli)
                '..', # up 3 levels
                '..',
                '..',
                path # Then add the requested apth
            )
        )

    def clear_screen(self):
        if platform.system() == 'Windows':
            self.execute(['cls'])
        else:
            self.execute(['clear'])
