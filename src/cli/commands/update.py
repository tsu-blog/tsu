from commands.base import TsuCommand
import os

class UpdateCmd(TsuCommand):
    id = 'update'
    description = 'Updates Tsu to the latest version'

    def run(self, args):
        print("Updating Tsu...")

        self.execute(['git', 'fetch', 'upstream', 'master'], cwd=self.path('.'))
        self.execute(['git', 'merge', 'upstream/master', '--no-edit'], cwd=self.path('.'))
