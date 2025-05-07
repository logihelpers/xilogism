from flet import Page
from data.files import Files
from pathlib import Path

def InitFiles(page: Page):
    files = Files()
    page.run_thread(retrieve_files, files)

def AppendFile(path: Path):
    files = Files()
    files.append_file(path)

def retrieve_files(files: Files):
    files.retrieve_files_local()