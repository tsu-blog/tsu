import sys
import time
import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from commands.base import TsuCommand
from commands.deploy import DeployCmd

class WatchCmd(TsuCommand):
    id = 'watch'
    description = 'Watch for changes and deploy on change'
    last_deploy = None

    def add_arguments(self, parser):
        parser.add_argument('-f', '--function', help="Specific function to update")

    def run(self, args):
        self.print_header()
        start_time = datetime.datetime.utcnow()

        observer = Observer()
        observer.schedule(DeployHandler(args, self), self.path('src'), recursive=True)
        observer.schedule(StaticSyncHandler(args, self), self.path('static'), recursive=True)
        observer.start()

        try:
            while True:
                # If we are not watching a single function just do small sleeps
                if not args.function:
                    time.sleep(1)
                    continue

                # If we are only watching a specific function, poll the logs
                # (this takes a few seconds so we wait to clear the screen until
                # after the logs are returned)
                output = self.execute([
                    'sls', 'logs', '-f', args.function,
                    '--startTime', start_time.strftime('%Y%m%dT%H%M%S')
                ], capture_output=True)

                self.print_header()
                print(f"- Logs for {args.function}:")
                print(output.stdout.decode("utf-8"))

        except KeyboardInterrupt:
            observer.stop()

        observer.join()

    def print_header(self):
        time_since_last_deploy = 'n/a'
        if self.last_deploy:
            total_seconds_since_last_deploy = int((datetime.datetime.now() - self.last_deploy).total_seconds())
            min_since_deploy = int(total_seconds_since_last_deploy/60)
            sec_since_deploy = total_seconds_since_last_deploy % (min_since_deploy*60) if min_since_deploy > 0 else total_seconds_since_last_deploy
            time_since_last_deploy = f"{min_since_deploy}m {sec_since_deploy}s"

        # Clear the screen so our output is always in the same place
        self.clear_screen()

        print("Watching for development changes... Ctrl+C to stop")
        print(f"Last deploy: {time_since_last_deploy}")
        print("")

class DeployHandler(FileSystemEventHandler):
    def __init__(self, args, watcher_cmd):
        self.args = args
        self.watcher_cmd = watcher_cmd

    def on_any_event(self, event):
        DeployCmd().run(self.args)
        self.watcher_cmd.last_deploy = datetime.datetime.now()

class StaticSyncHandler(FileSystemEventHandler):
    def __init__(self, args, watcher_cmd):
        self.args = args
        self.watcher_cmd = watcher_cmd

    def on_any_event(self, event):
        DeployCmd().sync_static(self.args)
