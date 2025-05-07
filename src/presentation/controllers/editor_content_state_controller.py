from flet import *
from presentation.states.editor_content_state import EditorContentState, CodeState
from presentation.states.sidebar_hide_state import *
from presentation.states.active_file_state import ActiveFileState
from presentation.states.render_state import *
from presentation.states.new_save_state import NewSaveState
from presentation.states.auth_state import AuthState
from models.xilofile_model import XiloFile, StorageType
from services.processing_pipeline import PseudocodeParser, PythonValidator, PythonGenerator, BooleanConverter
from services.init.init_files import AppendFile

from presentation.controllers.controller import Controller, Priority
from presentation.views.editor_view import EditorView
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io
import json
from pathlib import Path

class EditorContentStateController(Controller):
    instances: dict[str, "EditorContentStateController"] = {}
    priority = Priority.NONE
    old_active: str = ""
    def __init__(self, page: Page, key: str = "New", editor_view: EditorView = None):
        self.page = page
        self.key_name = key
        EditorContentStateController.instances[key] = self

        if editor_view is None:
            self.editor_view: EditorView = self.page.session.get("editor_view")
        else:
            self.editor_view = editor_view

        self.ec_state = EditorContentState()
        self.sbh_state = SideBarHideState()
        self.render_state = RenderState()
        self.af_state = ActiveFileState()
        self.ns_state = NewSaveState()
        self.auth_state = AuthState()
        
        self.ns_state.on_change = self.save_file
        self.ec_state.on_change = self.parse_content

        self.parser = PseudocodeParser()
        self.pygen = PythonGenerator()
        self.validator = PythonValidator()
        self.boolean_converter = BooleanConverter()

        self.update_count = 0
    
    def save_file(self):
        save: bool = self.ns_state.state
        content: str = self.ec_state.content[self.key_name]
        if save:
            file_content: dict = {
                'name': self.ns_state.project_name,
                'content': content
            }

            documents_dir = Path.home() / "Documents"
            file_path = documents_dir.absolute() / (self.ns_state.filename + '.xlg')
            with open(file_path, "x") as f:
                json.dump(file_content, f, indent=4)

            try:
                self.page.open(
                    SnackBar(
                        content=Text(f"Your xilogism is now saved in {file_path}."), 
                        behavior=SnackBarBehavior.FLOATING, 
                        duration=10000,
                        show_close_icon=True,
                        margin=margin.all(12) if not self.sbh_state.state.value else margin.only(left=212, top=12, right=12, bottom=12)
                    )
                )
            except:
                pass
            
            AppendFile(file_path)

    def parse_content(self):
        active: str = self.ec_state.content[self.key_name]

        if self.old_active == active or not self.af_state.active:
            return
        
        if isinstance(self.af_state.active, str) and self.af_state.active != "New Xilogism":
            return
        elif isinstance(self.af_state.active, XiloFile) and self.af_state.active.title != self.key_name:
            return

        self.old_active = active

        if not isinstance(self.af_state.active, str) and not self.af_state.active.storage_type == StorageType.GDRIVE:
            json_file: dict = {}
            json_file['name'] = self.key_name
            json_file['content'] = active
            with open(self.af_state.active.path, "w", encoding="utf-8") as f:
                json.dump(json_file, f, indent=4)
        elif not isinstance(self.af_state.active, str) and self.af_state.active.storage_type == StorageType.GDRIVE:
            if self.update_count == 0:
                json_file: dict = {}
                json_file['name'] = self.key_name
                json_file['content'] = active

                file_stream = io.BytesIO(json.dumps(json_file).encode('utf-8'))
                media = MediaIoBaseUpload(file_stream, mimetype='application/json', resumable=True)

                file_id = self.af_state.active.path

                service = build('drive', 'v3', credentials=self.auth_state.google_creds)
                request = service.files().update(
                    fileId=file_id,
                    media_body=media
                ).execute()

                self.update_count += 1
                self.update_count = 0 if self.update_count >= 20 else self.update_count

        try:
            self.editor_view.code_editor.value = self.ec_state.content[self.key_name]
            self.editor_view.code_editor.update()
            self.editor_view.update()
        except:
            pass

        if active == "":
            self.ec_state.code_state[self.key_name] = CodeState.BLANK
            return
        try:
            output = self.parser.parse(active)
            generated = self.pygen.generate(output)
            
            errors = self.validator.validate(generated)

            if len(errors) > 0 or len(self.parser.errors) > 0:
                self.show_errors(errors + self.parser.errors)
                self.ec_state.code_state[self.key_name] = CodeState.WRONG
                return

            converted = self.boolean_converter.convert(generated)
            self.render_state.input[self.key_name] = converted

            self.ec_state.code_state[self.key_name] = CodeState.CORRECT
        except Exception as err:
            self.show_errors([str(err)])
            self.ec_state.code_state[self.key_name] = CodeState.WRONG
    
    def show_errors(self, errors: list):
        message = ""
        if len(errors) == 1:
            message = errors[0]
        else:
            message = f"{len(errors)} errors detected. Please fix immediately."

        self.page.open(
            SnackBar(
                content=Text(message), 
                behavior=SnackBarBehavior.FLOATING, 
                duration=5000,
                show_close_icon=True,
                margin=margin.all(12) if not self.sbh_state.state.value else margin.only(left=212, top=12, right=12, bottom=12)
            )
        )