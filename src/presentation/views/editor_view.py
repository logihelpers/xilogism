from flet import *
import json

from presentation.states.active_file_state import ActiveFileState, XiloFile
from presentation.states.editor_content_state import EditorContentState, CodeState
from presentation.states.editor_theme_state import EditorThemeState
from presentation.states.dialogs_state import DialogState, Dialogs
from presentation.states.language_state import LanguageState

from presentation.views.widgets.editor_view.fontface_chooser_button import FontFaceChooserButton
from presentation.views.widgets.editor_view.font_size_textfield import FontSizeTextField
from presentation.views.widgets.editor_view.diagram_mode_chooser import DiagramModeChooser
from presentation.views.widgets.editor_view.export_button import ExportButton
from presentation.views.widgets.editor_view.expand_button import ExpandButton
from presentation.views.widgets.editor_view.generate_bom_button import GenerateBOMButton

from presentation.views.widgets.circuit_components.canvas import Canvas

from presentation.views.widgets.editor_view.undo_redo_buttons import UndoRedoButtons
from presentation.states.render_state import RenderState
from presentation.states.animation_disable_state import AnimationDisableState
from presentation.states.accent_color_state import AccentColorState
from presentation.states.dark_mode_state import *
from presentation.states.active_sidebar_button_state import ActiveSideBarButtonState

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
        self.lang_state = LanguageState()
        self.lang_state.on_lang_updated = self.update_lang
        self.ad_state = AnimationDisableState()
        self.ad_state.on_change = self.update_animations
        self.ac_state = AccentColorState()
        self.dm_state = DarkModeState()
        self.asb_state = ActiveSideBarButtonState()

        self.hidden_options = Revealer(
            content_hidden=True,
            content_length=72,
            animation_duration=500,
            animation_curve=AnimationCurve.EASE_IN_OUT_CIRC,
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
                            padding = 8,
                            content=Image(
                                src="/icons_light/new.png",
                                width=16,
                                height=16
                            ),
                            on_click = lambda event: setattr(self.asb_state, 'active', "New Xilogism"),
                        ),
                        VerticalDivider(1, color="black"),
                        Container(
                            width = 32,
                            height = 32,
                            padding = 8,
                            content=Image(
                                src="/icons_light/open.png",
                                width=16,
                                height=16
                            ),
                            on_click = lambda event: setattr(self.asb_state, 'active', "Open Xilogism"),
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

        self.expand_button = ExpandButton()
        self.generate_bom_button = GenerateBOMButton()

        self.canvas = Canvas(
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

        self.code_editor_container = Container(
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

        self.viewing_mode_text = Text("Viewing Mode:", color="black")

        self.preview_bar = Row(
            height=32,
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            controls= [
                Row(
                    controls=[
                        self.viewing_mode_text,
                        self.diagram_mode,
                    ]
                ),
                self.export_button
            ]
        )

        self.preview_view = Container(
            expand=True,
            content=Stack(
                expand=True,
                controls=[
                    Row(controls = [Zoomer(self.canvas, 0.1, 100.0, expand=True)], top=0, bottom=0, right=0, left=0, expand=True),
                    Row(
                        controls = [
                            self.generate_bom_button,
                            self.expand_button
                        ],
                        top=8,
                        right=8
                    )
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
                        self.code_editor_container
                    ]
                ),
                animate_opacity=Animation(300, AnimationCurve.EASE_IN_OUT_CIRC)
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
                                self.preview_bar,
                                self.preview_view
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
        self.ac_state.on_colors_updated = self.update_colors
    
    def update_codepane_length(self, event: ControlEvent):
        if not self.code_pane.content_hidden:
            dictio = json.loads(event.data)
            self.code_pane.content_length = (int(dictio["width"]) / 2) - 10
            self.code_pane.update()
    
    def update_theme(self):
        self.code_editor.editor_theme = self.et_state.editor_theme
        self.code_editor.update()
    
    def update_status_icon(self):
        lang_values = self.lang_state.lang_values
        if not self.af_state.active:
            return
        elif self.af_state.active == "New Xilogism":
            key_name = "New"
        elif type(self.af_state.active) != XiloFile or \
            (type(self.af_state.active) == XiloFile and \
                self.af_state.active.title != self.key_name):
            return
        else:
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
                active_instance.edit_status_icon.tooltip = lang_values["blank_content_tooltip"]
            case CodeState.CORRECT:
                active_instance.edit_status_icon.image.src = "/icons_light/correct.png"
                active_instance.edit_status_icon.tooltip = lang_values["correct_content_tooltip"]
            case CodeState.WRONG:
                active_instance.edit_status_icon.image.src = "/icons_light/wrong.png"
                active_instance.edit_status_icon.tooltip = lang_values["wrong_content_tooltip"]
        
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
        self.canvas.capture(1000, 772)
        self.dia_state.state = Dialogs.EXPORT
    
    def update_content(self, event: ControlEvent):
        self.ec_state.content[self.key_name] = event.data
        self.canvas.capture(1000, 772)
    
    def capture_image(self, event: ControlEvent):
        self.render_state.image = {self.key_name: event.data}
    
    def update_colors(self):
        colors = self.ac_state.color_values
        dark_mode = self.dm_state.active == DarkModeScheme.DARK

        instance: EditorView = None
        for instance in EditorView.instances:
            instance.bgcolor = colors["bg_color"]
            instance.hidden_options.content.border = border.all(1, colors["text_color"])
            instance.hidden_options.content.bgcolor = colors["button_bgcolor"].replace("4d", "0f") if "4d" in colors["button_bgcolor"] else colors["button_bgcolor"].replace("#", "#73")
            instance.hidden_options.content.content.controls[1].color = colors["text_color"]
            instance.font_family_chooser.fill_color = colors["button_bgcolor"].replace("4d", "0f") if "4d" in colors["button_bgcolor"] else colors["button_bgcolor"].replace("#", "#73")
            instance.font_family_chooser.border_color = colors["text_color"]
            instance.edit_status_icon.border = border.all(1, colors["text_color"])
            instance.diagram_mode.fill_color = colors["button_bgcolor"].replace("4d", "0f") if "4d" in colors["button_bgcolor"] else colors["button_bgcolor"].replace("#", "#73")
            instance.diagram_mode.border_color = colors["text_color"]
            instance.code_editor_container.border = border.all(1, colors["container_border_color"])
            instance.preview_view.bgcolor = colors["sidebar_color"]
            instance.preview_view.border = border.all(1, colors["container_border_color"])
            instance.viewing_mode_text.color = colors["text_color"]
            instance.hidden_options.content.content.controls[0].content.src = "icons_light/new.png" if not dark_mode else "icons_dark/new.png"
            instance.hidden_options.content.content.controls[2].content.src = "icons_light/open.png" if not dark_mode else "icons_dark/open.png"

            instance.diagram_mode.update_colors()
            instance.expand_button.update_colors()
            instance.export_button.update_colors()
            instance.font_size_tf.update_colors()
            instance.font_family_chooser.update_colors()
            instance.generate_bom_button.update_colors()
            instance.undo_redo_button_group.update_colors()
            instance.canvas.update_color()
            instance.update()
        self.page.update()
    
    def update_animations(self):
        animate = self.ad_state.state
        self.hidden_options.animation_duration = 500 if animate else 0
        self.code_pane.animation_duration = 500 if animate else 0
        self.update()
    
    def update_lang(self):
        lang_values = self.lang_state.lang_values
        instance: EditorView = None
        for instance in EditorView.instances:
            instance.viewing_mode_text.value = lang_values["viewing_mode"]
            instance.viewing_mode_text.update()
            instance.export_button.update_lang()