import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from commands.base import TsuCommand
from commands.deploy import DeployCmd

class WatchCmd(TsuCommand):
    id = 'watch'
    description = 'Watch for changes and deploy on change'

    def run(self, args):
        print("Watching for development changes... Ctrl+C to stop")
        observer = Observer()
        observer.schedule(DeployHandler(args), self.path('src'), recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

class DeployHandler(FileSystemEventHandler):
    def __init__(self, args):
        self.args = args

    def on_any_event(self, event):
        DeployCmd().run(self.args)
