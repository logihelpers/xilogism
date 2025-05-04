from flet import *
import json

from presentation.states.active_file_state import ActiveFileState, XiloFile
from presentation.states.editor_content_state import EditorContentState, CodeState
from presentation.states.editor_theme_state import EditorThemeState
from presentation.states.dialogs_state import DialogState, Dialogs

from presentation.views.widgets.editor_view.fontface_chooser_button import FontFaceChooserButton
from presentation.views.widgets.editor_view.font_size_textfield import FontSizeTextField
from presentation.views.widgets.editor_view.diagram_mode_chooser import DiagramModeChooser
from presentation.views.widgets.editor_view.export_button import ExportButton
from presentation.views.widgets.editor_view.expand_button import ExpandButton

from presentation.views.widgets.logic_circuit.canvas import LogicCanvas

from presentation.views.widgets.editor_view.undo_redo_buttons import UndoRedoButtons
from presentation.states.render_state import RenderState

from xilowidgets import Editor, Revealer, Zoomer
from flet_layoutbuilder import LayoutBuilder

class EditorView(Container):
    widget_scale: float = 1.0
    old_scale: float = 1.0
    font_size = 16
    font_family = "Iosevka"
    instances: list = []
    def __init__(self, key_name: str):
        super().__init__()
        self.widget_scale = 1.0
        self.key_name = key_name
        
        self.padding = padding.all(16)
        self.expand = True

        self.ec_state = EditorContentState()
        self.et_state = EditorThemeState()
        self.render_state = RenderState()
        self.dia_state = DialogState()
        self.af_state = ActiveFileState()

        self.hidden_options = Revealer(
            content_hidden=True,
            content_length=72,
            content=Container(
                margin=margin.only(right = 8),
                border=border.all(1, "black"),
                bgcolor="#1a191f51",
                border_radius=8,
                content=Row(
                    spacing=0,
                    controls=[
                        Container(
                            width = 32,
                            height = 32,
                            padding = 4,
                            content=Image(
                                src="/icons_light/new.png",
                                width=16,
                                height=16
                            )
                        ),
                        VerticalDivider(1, color="black"),
                        Container(
                            width = 32,
                            height = 32,
                            padding = 4,
                            content=Image(
                                src="/icons_light/open.png",
                                width=16,
                                height=16
                            )
                        ),
                    ]
                )
            )
        )

        self.font_family_chooser = FontFaceChooserButton()

        self.code_editor = Editor(
            value=self.ec_state.content[self.key_name],
            expand=True,
            editor_theme=self.et_state.editor_theme,
            gutter_width=64,
            font_family=self.font_family,
            font_size=self.font_size,
            on_change=self.update_content
        )

        self.edit_status_icon = Container(
            shape=BoxShape.CIRCLE,
            border=border.all(1, "black"),
            width=32,
            height=32,
            padding=8,
            image=DecorationImage(
                "/icons_light/blank.png",
            ),
            tooltip="Content is currently blank..."
        )

        self.font_size_tf = FontSizeTextField()

        self.undo_redo_button_group = UndoRedoButtons()

        self.export_button = ExportButton()
        self.export_button.on_click = self.update_dialog

        self.diagram_mode = DiagramModeChooser()

        self.expand_button = ExpandButton(
            top=8,
            right=8
        )

        self.canvas = LogicCanvas(
            expand=True,
        )
        self.canvas.height = 1000
        self.canvas.width = 1000
        self.canvas.on_capture = self.capture_image

        toolbar = Row(
            height = 32,
            spacing = 0,
            controls = [
                self.hidden_options,
                Row(
                    expand = True,
                    height=32,
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        Row(
                            controls=[
                                self.font_family_chooser,
                                self.font_size_tf
                            ]
                        ),
                        Row(
                            controls = [
                                self.edit_status_icon,
                                self.undo_redo_button_group
                            ]
                        )
                    ]
                )
            ]
        )

        code_editor_container = Container(
            theme_mode=ThemeMode.LIGHT,
            expand=True,
            content=Container(
                Row(
                    expand=True,
                    vertical_alignment=CrossAxisAlignment.STRETCH,
                    controls=[
                        self.code_editor
                    ]
                ),
                border_radius=8
            ),
            border=border.all(1, "#6b6b6b"),
            border_radius=8,
            padding = 0,
            clip_behavior=ClipBehavior.ANTI_ALIAS
        )

        preview_bar = Row(
            height=32,
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            controls= [
                Row(
                    controls=[
                        Text("Viewing Mode:", color="black"),
                        self.diagram_mode,
                    ]
                ),
                self.export_button
            ]
        )

        preview_view = Container(
            expand=True,
            content=Stack(
                expand=True,
                controls=[
                    Row(controls = [Zoomer(self.canvas, 0.1, 100.0, expand=True)], top=0, bottom=0, right=0, left=0, expand=True),
                    self.expand_button
                ]
            ),
            border=border.all(1, "#6b6b6b"),
            border_radius=8,
            padding=2,
            bgcolor="#d9d9d9"
        )

        self.code_pane = Revealer(
            content_length=384.6,
            content_fill=True,
            content=Container(
                Column(
                    horizontal_alignment=CrossAxisAlignment.STRETCH,
                    expand=True,
                    controls=[
                        toolbar,
                        code_editor_container
                    ]
                ),
                animate_opacity=animation.Animation(300, AnimationCurve.EASE_IN_OUT_CIRC)
            ),
            animation_duration=500,
            animation_curve=AnimationCurve.EASE_IN_OUT_CIRC
        )

        self.content = LayoutBuilder(
            content = Row(
                expand=True,
                controls=[
                    self.code_pane,
                    Container(
                        expand=True,
                        content=Column(
                            controls=[
                                preview_bar,
                                preview_view
                            ]
                        ),
                    )
                ]
            ),
            update_size_on_init=True,
            alignment=alignment.center,
            on_change=self.update_codepane_length
        )

        if self not in EditorView.instances:
            EditorView.instances.append(self)
    
    def did_mount(self):
        super().did_mount()

        self.ec_state.on_code_state_change = self.update_status_icon
        self.et_state.on_theme_change = self.update_theme
        self.render_state.on_output_change = self.update_canvas
    
    def update_codepane_length(self, event: ControlEvent):
        if not self.code_pane.content_hidden:
            dictio = json.loads(event.data)
            self.code_pane.content_length = (int(dictio["width"]) / 2) - 10
            self.code_pane.update()
    
    def update_theme(self):
        self.code_editor.editor_theme = self.et_state.editor_theme
        self.code_editor.update()
    
    def update_status_icon(self):
        if not self.af_state.active or type(self.af_state.active) != XiloFile or (type(self.af_state.active) == XiloFile and self.af_state.active.title != self.key_name):
            return
        
        key_name = self.af_state.active.title

        active_instance: EditorView = None
        instance: EditorView = None
        for instance in EditorView.instances:
            if instance.key_name == key_name:
                active_instance = instance
                break

        match active_instance.ec_state.code_state[key_name]:
            case CodeState.BLANK:
                active_instance.edit_status_icon.image.src = "/icons_light/blank.png"
                active_instance.edit_status_icon.tooltip = "Content is currently blank..."
            case CodeState.CORRECT:
                active_instance.edit_status_icon.image.src = "/icons_light/correct.png"
                active_instance.edit_status_icon.tooltip = "Content is correct..."
            case CodeState.WRONG:
                active_instance.edit_status_icon.image.src = "/icons_light/wrong.png"
                active_instance.edit_status_icon.tooltip = "Content is containing errors..."
        
        active_instance.edit_status_icon.update()
  
    def update_canvas(self, output_dict: dict):
        if len(output_dict.items()) <= 0:
            return

        key_name, output_dict = output_dict.popitem()

        active_instance: EditorView = None
        instance: EditorView = None
        for instance in EditorView.instances:
            if instance.key_name == key_name:
                active_instance = instance
                break

        active_instance.canvas.clear()

        [active_instance.canvas.add_to_canvas(gate) for gate in output_dict]
        active_instance.canvas.update()
    
    def update_dialog(self, event: ControlEvent):
        self.canvas.capture(600, 600)
        self.dia_state.state = Dialogs.EXPORT
    
    def update_content(self, event: ControlEvent):
        self.ec_state.content[self.key_name] = event.data
    
    def capture_image(self, event: ControlEvent):
        self.render_state.image[self.key_name] = event.data