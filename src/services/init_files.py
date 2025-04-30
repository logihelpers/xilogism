from flet import Page
from data.files import Files
import asyncio

def InitFiles(page: Page):
    files = Files()
    page.run_thread(retrieve_files, files)

def retrieve_files(files: Files):
    files.retrieve_files_local()