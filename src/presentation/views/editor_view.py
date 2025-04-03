from flet import *
from math import pi

from presentation.states.active_sidebar_button_state import ActiveSideBarButtonState
from presentation.states.editor_content_state import EditorContentState

from presentation.views.widgets.editor_view.fontface_chooser_button import FontFaceChooserButton
from presentation.views.widgets.editor_view.font_size_textfield import FontSizeTextField
from presentation.views.widgets.editor_view.diagram_mode_chooser import DiagramModeChooser
from presentation.views.widgets.editor_view.export_button import ExportButton

from presentation.views.widgets.editor_view.undo_redo_buttons import UndoRedoButtons

from xilowidgets import Editor, EditorTheme, Drawboard, Revealer

class EditorView(Container):
    widget_scale: float = 1.0
    old_scale: float = 1.0
    font_size = 16
    font_family = "Iosevka"
    bg_dark: bool = False
    def __init__(self):
        super().__init__()
        self.widget_scale = 1.0

        self.padding = padding.all(16)
        self.expand = True

        self.ec_state = EditorContentState()

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
            value=self.ec_state.content,
            expand=True,
            editor_theme=EditorTheme.DEFAULT,
            gutter_width=64,
            font_family=self.font_family,
            font_size=self.font_size,
            on_change=lambda event: setattr(self.ec_state, 'content', event.data),
        )

        self.font_size_tf = FontSizeTextField()

        self.undo_redo_button_group = UndoRedoButtons()

        self.export_button = ExportButton()

        self.diagram_mode = DiagramModeChooser()

        self.canvas = Drawboard(
            expand=True,
            top=0,
            bottom=0,
            right=0,
            left=0
        )

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
                        self.undo_redo_button_group
                    ]
                )
            ]
        )

        code_editor_container = Container(
            theme_mode=ThemeMode.LIGHT,
            expand=True,
            content=Row(
                expand=True,
                vertical_alignment=CrossAxisAlignment.STRETCH,
                controls=[
                    self.code_editor
                ]
            ),
            border=border.all(1, "#6b6b6b"),
            border_radius=8,
            padding = 0 if self.bg_dark else 2,
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
                    self.canvas,
                    Container(
                        top=8,
                        right=8,
                        content=Image(
                            src="/icons_light/full-size.png",
                            width=16,
                            height=16
                        )
                    )
                ]
            ),
            border=border.all(1, "#6b6b6b"),
            border_radius=8,
            padding=2,
            bgcolor="#d9d9d9"
        )

        self.content = Row(
            expand=True,
            controls=[
                Container(
                    expand=True,
                    content=Column(
                        horizontal_alignment=CrossAxisAlignment.STRETCH,
                        expand=True,
                        controls=[
                            toolbar,
                            code_editor_container
                        ]
                    )
                ),
                Container(
                    expand=True,
                    content=Column(
                        controls=[
                            preview_bar,
                            preview_view
                        ]
                    )
                )
            ]
        )