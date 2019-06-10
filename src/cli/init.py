"""Initialize Tsu and its dependencies - you shouldn\'t need to call this directly"""

import shutil
import subprocess
import os

def execute(command):
    """Execute the provided command using the subprocess module"""
    command[0] = shutil.which(command[0]) # Lookup the command using PATH (windows doesn't do this by default)
    return subprocess.run(command)

def path(path):
    """Returns an absolute path given a path that is relative to the Tsu root directory"""
    return os.path.normpath( # Resolve the ../../ into a direct absolute path
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)), # The dir of our current file (eg /something/arbitrary/src/cli)
            '..', # up 2 levels
            '..',
            path # Then add the requested apth
        )
    )

if __name__ == "__main__":
    print("Initializing Tsu")

    print("- Setting up Virtual Environment")
    execute(['python3', '-m', 'venv', path('venv')])

    print("- Installing requirements")
    execute([path('venv/bin/pip'), 'install', '-r', path('requirements-dev.txt')])
