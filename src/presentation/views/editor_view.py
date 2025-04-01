from flet import *
from math import pi

from presentation.states.active_sidebar_button_state import ActiveSideBarButtonState
from presentation.views.widgets.editor_view.fontface_chooser_button import FontFaceChooserButton
from presentation.views.widgets.editor_view.font_size_textfield import FontSizeTextField

from presentation.views.widgets.editor_view.undo_redo_buttons import UndoRedoButtons

from codeeditor import CodeEditor, EditorTheme
from xilocanvas import Xilocanvas
from slidablepanel import SlidablePanel

class EditorView(Container):
    widget_scale: float = 1.0
    old_scale: float = 1.0
    font_size = 16
    font_family = "Iosevka"
    current_text = ""
    bg_dark: bool = False
    def __init__(self):
        super().__init__()
        self.widget_scale = 1.0

        self.padding = padding.all(16)
        self.expand = True

        self.hidden_options = SlidablePanel(
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

        self.code_editor = CodeEditor(
            value=self.current_text,
            expand=True,
            editor_theme=EditorTheme.DEFAULT,
            gutter_width=64,
            font_family=self.font_family,
            font_size=self.font_size,
            on_change=self.change,
        )

        self.font_size_tf = FontSizeTextField()

        self.undo_redo_button_group = UndoRedoButtons()

        self.export_button = Container(
            border=border.all(1, "black"),
            border_radius=8,
            bgcolor="#73191f51",
            height=32,
            padding=padding.symmetric(4, 8),
            content=Row(
                controls=[
                    Text(
                        value="Export",
                        weight=FontWeight.BOLD
                    ),
                    Image(
                        src="/icons_light/export.png",
                        width=16,
                        height=16
                    )
                ]
            )
        )

        self.diagram_mode = DropdownM2(
            value="Logic Diagram",
            border_radius=8,
            width=148,
            border_width=1,
            border_color="black",
            content_padding=padding.only(left=8,right=8),
            select_icon=Container(
                content = Image(
                    src="/icons_light/arrow_down.png",
                    width=16,
                    height=16
                )
            ),
            filled=True,
            bgcolor={
                ControlState.DEFAULT: "#1a191f51",
                ControlState.DISABLED: "#1a191f51",
                ControlState.DRAGGED: "#1a191f51",
                ControlState.ERROR: "#1a191f51",
                ControlState.FOCUSED: "#1a191f51",
                ControlState.HOVERED: "#1a191f51",
                ControlState.PRESSED: "#1a191f51",
                ControlState.SELECTED: "#1a191f51"
            },
            fill_color={
                ControlState.DEFAULT: "#1a191f51",
                ControlState.DISABLED: "#1a191f51",
                ControlState.DRAGGED: "#1a191f51",
                ControlState.ERROR: "#1a191f51",
                ControlState.FOCUSED: "#1a191f51",
                ControlState.HOVERED: "#1a191f51",
                ControlState.PRESSED: "#1a191f51",
                ControlState.SELECTED: "#1a191f51"
            },
            options=[
                DropdownOption(
                    key="Logic Diagram",
                    content=Text("Logic Diagram")
                ),
                DropdownOption(
                    key="Circuit Diagram",
                    content=Text("Circuit Diagram")
                )
            ]
        )

        self.canvas = Xilocanvas(
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
    
    def change(self, event):
        self.recuro = event.data