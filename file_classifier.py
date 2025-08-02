from pathlib import Path
from shutil import move
from os import scandir, rename

from watchdog.events import FileSystemEventHandler , LoggingEventHandler
from watchdog.observers import Observer
import logging
import time
import sys

downloads_directory = Path.home() / "Downloads"

folder_categories = {
    "pdf": "PDFs",
    "image": "Images",
    "zip" : "Zipped Folders",
    "audio" : "Audio",
    "text" : "Text"
}

destination_paths = {}

def createClassifierFolders():
    for ext, folder in folder_categories.items():
        folder_path = downloads_directory / folder
        destination_paths[ext] = folder_path
        if not folder_path.exists():
            folder_path.mkdir()

def move_file(dest, entry, name):
    if (dest/name).exists():
        print("it is real")
    move(entry, dest)

class MoveHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with scandir(downloads_directory) as entries:
            for entry in entries:
                name = entry.name
    
    def check_text_files(entry, name: str):
        if name.endswith(".txt") or name.endswith(".txt".upper()):
            move_file(destination_paths["text"], entry, name)
            logging.info(f"Moved text file: {name}")


def main():
     if  not downloads_directory.exists():
        print("Downloads directory not found!")
        return
     createClassifierFolders()
     logging.basicConfig(level=logging.INFO,
                         format='%(asctime)s - %(message)s',
                         datefmt='%Y-%m-%d %H:%M:%S')
     path = downloads_directory
     event_handler = MoveHandler()
     observer = Observer()
     observer.schedule(event_handler, str(path))
     observer.start()

     try:
        while True:
            time.sleep(5)
     except KeyboardInterrupt:
         observer.stop()
     observer.join()






if __name__ == "__main__":
    main()
