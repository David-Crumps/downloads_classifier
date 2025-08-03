from pathlib import Path
from shutil import move
from os import scandir, rename
from os.path import splitext, exists, join

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
    "text" : "Text",
    "document" : "Documents",
    "exe" : "Exes"
}

#Instantiated in createClassifierDirectories()
#Key is the same as the folder categories with value being the path to the directory
destination_paths = {}

image_file_types = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", "pjpeg", ".pjp", ".apng", ".png" , 
                    ".gif", ".svg", ".webp", ".bmp" ,".ico", ".cur", ".tif", ".tiff", ".avif"]

document_file_types = [".doc", ".docx", ".xls", "xlsx", ".ppt", ".pptx"]

audio_file_types = [".mp3", ".wav", ".wma"]

def createClassifierDirectories():
    for ext, folder in folder_categories.items():
        folder_path = downloads_directory / folder

        destination_paths[ext] = folder_path

        if not folder_path.exists():
            folder_path.mkdir()

def makeFileNameUnique(dest, name):
    filename, fileType = splitext(name)
    counter = 1

    while (dest/name).exists():
        name = f"{filename}({str(counter)}){fileType}"
        counter += 1
    return name

def moveFile(dest, entry, name):
    if (dest/name).exists():
        uniqueName = makeFileNameUnique(dest, name)
        oldName = dest/name
        newName = dest/uniqueName
        rename(oldName, newName)
    move(entry, dest)

class MoveHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with scandir(downloads_directory) as entries:
            for entry in entries:
                name = entry.name
                self.check_text_files(entry, name)
                self.check_pdf_files(entry, name)
                self.check_images(entry, name)
                self.check_document_files(entry, name)
                self.check_zipped_files(entry, name)
                self.check_audio_files(entry, name)
                self.check_installer_files(entry, name)
    
    def check_text_files(self, entry, name: str):
        if name.endswith(".txt") or name.endswith(".txt".upper()):
            moveFile(destination_paths["text"], entry, name)
            logging.info(f"Moved text file: {name}")

    def check_pdf_files(self, entry, name: str):
        if name.endswith(".pdf") or name.endswith(".txt".upper()):
            moveFile(destination_paths["pdf"], entry, name)
            logging.info(f"Moved pdf file: {name}")
    
    def check_images(self, entry, name: str):
        for image_file_type in image_file_types:
            if name.endswith(image_file_type) or name.endswith(image_file_type.upper()):
                moveFile(destination_paths["image"], entry, name)
                logging.info(f"Moved image file: {name}")
    
    def check_document_files(self, entry, name: str):
        for document_file_type in document_file_types:
            if name.endswith(document_file_type) or name.endswith(document_file_type.upper()):
                moveFile(destination_paths["document"], entry, name)
                logging.info(f"Moved document file: {name}")

    def check_zipped_files(self, entry, name:str):
        if name.endswith(".zip") or name.endswith(".zip".upper()):
            moveFile(destination_paths["zip"], entry, name)
            logging.info(f"Moved zipped file: {name}")

    def check_audio_files(self, entry, name:str):
        for audio_file_type in audio_file_types:
            if name.endswith(audio_file_type) or name.endswith(audio_file_type.upper()):
                moveFile(destination_paths["image"], entry, name)
                logging.info(f"Moved audio file: {name}")

    def check_installer_files(self, entry, name:str):
        if name.endswith(".exe") or name.endswith(".exe".upper()):
            moveFile(destination_paths["exe"], entry, name)
            logging.info(f"Moved exe file: {name}")


def main():
     if  not downloads_directory.exists():
        print("Downloads directory not found!")
        return
     createClassifierDirectories()
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
