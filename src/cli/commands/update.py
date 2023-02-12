from commands.base import TsuCommand
import os

class UpdateCmd(TsuCommand):
    id = 'update'
    description = 'Updates Tsu to the latest version'

    def run(self, args):
        print("Updating Tsu...")

        self.execute(['git', 'remote', 'add', 'upstream', 'git@github.com:tsu-blog/tsu.git'], cwd=self.path('.'))
        self.execute(['git', 'fetch', 'upstream', 'master'], cwd=self.path('.'))
        self.execute(['git', 'merge', 'upstream/master', '--no-edit'], cwd=self.path('.'))

        print("- Installing requirements")
        # Selecting venv looks a little different in windows
        if os.name == 'nt':
            self.execute([self.path('venv/Scripts/pip.exe'), 'install', '-r', self.path('requirements-dev.txt')])
            self.execute([self.path('venv/Scripts/pip.exe'), 'install', '-r', self.path('requirements.txt')])
        else:
            self.execute([self.path('venv/bin/pip'), 'install', '-r', self.path('requirements-dev.txt')])
            self.execute([self.path('venv/bin/pip'), 'install', '-r', self.path('requirements.txt')])

        print("- Installing NodeJS requirements")
        self.execute(['npm', 'install'], cwd=self.path('.'))
