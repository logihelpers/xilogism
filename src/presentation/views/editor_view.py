from flet import *
from math import pi

from presentation.states.active_sidebar_button_state import ActiveSideBarButtonState

from codeeditor import CodeEditor, EditorTheme
from xilocanvas import Xilocanvas
from slidablepanel import SlidablePanel

class EditorView(Container):
    widget_scale: float = 1.0
    old_scale: float = 1.0
    font_size = 16
    font_family = "Iosevka"
    current_text = ""
    def __init__(self):
        super().__init__()
        self.widget_scale = 1.0

        self.padding = padding.all(16)
        self.expand = True
    
    def build(self):
        super().build()

        self.hidden_options = SlidablePanel(
            content_hidden=True,
            content_width=64,
            visible=False,
            content=Container(
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

        self.font_family_chooser = DropdownM2(
            on_change=self.change_font,
            value=self.font_family,
            border_radius=8,
            width=160,
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
                    key="Fira Code",
                    content=Text("Fira Code", style=TextStyle(font_family="Fira Code")),
                ),
                DropdownOption(
                    key="Roboto Mono",
                    content=Text("Roboto Mono", style=TextStyle(font_family="Roboto Mono"))
                ),
                DropdownOption(
                    "IBM Plex Mono",
                    content=Text("IBM Plex Mono", style=TextStyle(font_family="IBM Plex Mono"))
                ),
                DropdownOption(
                    "Source Code Pro",
                    content=Text("Source Code Pro", style=TextStyle(font_family="Source Code Pro"))
                ),
                DropdownOption(
                    "JetBrains Mono",
                    content=Text("JetBrains Mono", style=TextStyle(font_family="JetBrains Mono"))
                ),
                DropdownOption(
                    "Fantasque Sans Mono",
                    content=Text("Fantasque Sans Mono", style=TextStyle(font_family="Fantasque Sans Mono"))
                ),
                DropdownOption(
                    "Inconsolata",
                    content=Text("Inconsolata", style=TextStyle(font_family="Inconsolata"))
                ),
                DropdownOption(
                    "Space Mono",
                    content=Text("Space Mono", style=TextStyle(font_family="Space Mono"))
                ),
                DropdownOption(
                    "Hasklig",
                    content=Text("Hasklig", style=TextStyle(font_family="Hasklig"))
                ),
                DropdownOption(
                    "Iosevka",
                    content=Text("Iosevka", style=TextStyle(font_family="Iosevka"))
                )
            ]
        )

        self.font_size_tf = Container(
            border=border.all(1, "black"),
            bgcolor="#1a191f51",
            border_radius=8,
            content=Row(
                spacing=0,
                controls=[
                    TextField(
                        input_filter=NumbersOnlyInputFilter(),
                        value=self.font_size,
                        border=0,
                        border_color="#00000000",
                        width=36,
                        content_padding=padding.only(left=8, right=8),
                        cursor_color=Colors.BLACK,
                        on_submit=self.resize_font
                    ),
                    VerticalDivider(1, color="black"),
                    Column(
                        expand=True,
                        spacing = 0,
                        controls=[
                            Container(
                                expand=True,
                                width=24,
                                content=Image(
                                    src="/icons_light/arrow_down.png",
                                    width=12,
                                    height=12,
                                    rotate=Rotate(angle=pi)
                                ),
                                on_click=self.increase_font_size
                            ),
                            Container(
                                expand=True,
                                width=24,
                                content=Image(
                                    src="/icons_light/arrow_down.png",
                                    width=12,
                                    height=12,
                                ),
                                border=border.only(top=BorderSide(1, "black")),
                                on_click=self.decrease_font_size
                            )
                        ]
                    )
                ]
            )
        )

        self.undo_redo_button_group = Container(
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
                            src="/icons_light/undo.png",
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
                            src="/icons_light/redo.png",
                            width=16,
                            height=16
                        )
                    ),
                ]
            )
        )

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

        self.content = Row(
            expand=True,
            controls=[
                Container(
                    expand=True,
                    content=Column(
                        horizontal_alignment=CrossAxisAlignment.STRETCH,
                        expand=True,
                        controls=[
                            Row(
                                height=32,
                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    Row(
                                        controls=[
                                            self.hidden_options,
                                            self.font_family_chooser,
                                            self.font_size_tf
                                        ]
                                    ),
                                    self.undo_redo_button_group
                                ]
                            ),
                            Container(
                                theme_mode=ThemeMode.LIGHT,
                                expand=True,
                                content=Row(
                                    expand=True,
                                    vertical_alignment=CrossAxisAlignment.STRETCH,
                                    controls=[
                                        CodeEditor(
                                            value=self.current_text,
                                            expand=True,
                                            editor_theme=EditorTheme.DEFAULT,
                                            gutter_width=64,
                                            font_family=self.font_family,
                                            font_size=self.font_size,
                                            on_change=self.change,
                                        )
                                    ]
                                ),
                                border=border.all(1, "#6b6b6b"),
                                border_radius=8,
                                clip_behavior=ClipBehavior.ANTI_ALIAS_WITH_SAVE_LAYER
                            )
                        ]
                    )
                ),
                Container(
                    expand=True,
                    content=Column(
                        controls=[
                            Row(
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
                            ),
                            Container(
                                expand=True,
                                content=Row(
                                    expand=True,
                                    vertical_alignment=CrossAxisAlignment.STRETCH,
                                    controls=[
                                        Stack(
                                            expand=True,
                                            controls=[
                                                Xilocanvas(
                                                    expand=True,
                                                ),
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
                                        )
                                    ]
                                ),
                                border=border.all(1, "#6b6b6b"),
                                border_radius=8,
                                padding=2,
                                bgcolor="#d9d9d9"
                            )
                        ]
                    )
                )
            ]
        )
    
    def increase_font_size(self, event):
        self.font_size += 1
        self.current_text = self.recuro
        self.build()
        self.update()
    
    def resize_font(self, event):
        self.font_size = int(event.data)
        self.current_text = self.recuro
        self.build()
        self.update()
    
    def decrease_font_size(self, event):
        self.font_size -= 1
        self.current_text = self.recuro
        self.build()
        self.update()
    
    def change_font(self, event):
        self.font_family = event.data
        self.current_text = self.recuro
        self.build()
        self.update()
    
    def change(self, event):
        self.recuro = event.data