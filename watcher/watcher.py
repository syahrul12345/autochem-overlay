import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import build
import time

class Watcher:
    DIRECTORY_TO_WATCH = 'C:/Program Files/Micromeritics/MicroActive for Autochem II 2920/data/excel/'

    def __init__(self):
        self.observer = Observer()

    def run(self):
        print('Running watchdog')
        print('Initialzie datbase builder script')
        # let's run build.py in case any files were missed
        build.buildDatabase()
        print('intial build end')
        print('Obsrving Excel directory for newly completed sample data....')
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print ("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            time.sleep(3)
            build.buildDatabase()
            print ("Received created event")

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            time.sleep(3)
            build.buildDatabase()
            print ("Received modified event")


if __name__ == '__main__':
    w = Watcher()
    w.run()