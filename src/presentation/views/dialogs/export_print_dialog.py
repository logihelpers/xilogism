from flet import *
from presentation.states.dialogs_state import DialogState, Dialogs

from xilowidgets import Revealer, XDialog, Switcher

from services.singleton import Singleton

class ExportPrintDialog(XDialog):
    def __init__(self):
        super().__init__()

        self.dia_state = DialogState()

        self.content_padding = 0
        self.title_padding = 0
        self.elevation = 0
        self.clip_behavior = ClipBehavior.HARD_EDGE
        self.bgcolor = "#ededed"
        self.actions_padding = padding.all(16)
        self.action_button_padding = 0
        self.actions_overflow_button_spacing = 0
        self.open_duration = 300
        self.modal = True

        self.navigator = SegmentedButton(
            on_change=self.change_view,
            selected={"0"},
            segments=[
                Segment(
                    value="0",
                    label=Text("Export"),
                ),
                Segment(
                    value="1",
                    label=Text("Print"),
                ),
            ],
        )

        self.print_export_setting = Switcher(
            orientation=Switcher.Orientation.HORIZONTAL,
            expand = True,
            controls = [
                Container(
                    expand = True,
                    content = Row(
                        expand = True,
                        controls = [
                            Text("File Format:", expand=True),
                            DropdownM2(
                                "pdf",
                                expand = True,
                                options=[
                                    DropdownOption(
                                        "pdf",
                                        "PDF",
                                        text_style=TextStyle(size=16)
                                    ),
                                    DropdownOption(
                                        "png",
                                        "PNG",
                                        text_style=TextStyle(size=16)
                                    ),
                                    DropdownOption(
                                        "docx",
                                        "DOCX",
                                        text_style=TextStyle(size=16)
                                    ),
                                ]
                            )
                        ]
                    )
                ),
                Container(
                    expand = True,
                    content = Row(
                        expand = True,
                        controls = [
                            Text("Page Size:", expand=True),
                            DropdownM2(
                                "letter",
                                expand = True,
                                text_style=TextStyle(size=14, color="black"),
                                options=[
                                    DropdownOption(
                                        "letter",
                                        "Letter 8.5 x 14 in",
                                        text_style=TextStyle(size=12, color="black")
                                    ),
                                    DropdownOption(
                                        "folio",
                                        "Folio 8.5 x 13 in",
                                        text_style=TextStyle(size=12, color="black")
                                    ),
                                    DropdownOption(
                                        "legal",
                                        "Legal 8.5 x 14 in",
                                        text_style=TextStyle(size=12, color="black")
                                    ),
                                    DropdownOption(
                                        "a4",
                                        "A4 8.3 x 11.7 in",
                                        text_style=TextStyle(size=12, color="black")
                                    ),
                                    DropdownOption(
                                        "b4",
                                        "B4 9.8 x 13.9 in",
                                        text_style=TextStyle(size=12, color="black")
                                    ),
                                ]
                            )
                        ]
                    )
                )
            ]
        )

        self.proceed_button = FilledButton(
            "Export", 
            expand=True,
        )

        self.extra_options = Revealer(
            height=150,
            orientation=Revealer.Orientation.VERTICAL,
            content = Container(
                height=150,
                padding = padding.symmetric(8, 24),
                border = border.all(1, "#73191f51"),
                border_radius = 8,
                content = Column(
                    scroll = ScrollMode.HIDDEN,
                    controls = [
                        Row(
                            expand = True,
                            height=36,
                            controls = [
                                Text("Project Name:", expand=True),
                                TextField(
                                    hint_text="e.g. Xilogism 1",
                                    expand=True,
                                    text_size=14,
                                    content_padding=padding.symmetric(8, 12)
                                )
                            ]
                        ),
                        Row(
                            expand = True,
                            height=36,
                            controls = [
                                Text("Creator :", expand=True),
                                TextField(
                                    hint_text="e.g. User",
                                    expand=True,
                                    text_size=14,
                                    content_padding=padding.symmetric(8, 12)
                                )
                            ]
                        ),
                        Row(
                            expand = True,
                            height=36,
                            controls = [
                                Text("Date:", expand=True),
                                TextField(
                                    hint_text="e.g. 04/07/2025",
                                    expand=True,
                                    text_size=14,
                                    content_padding=padding.symmetric(8, 12)
                                )
                            ]
                        )
                    ]
                )
            )
        )

        self.main_options = Container(
            expand=True,
            padding=padding.symmetric(8, 0),
            content = Column(
                expand = True,
                controls = [
                    self.print_export_setting,
                    Row(
                        controls = [
                            Text("Margin:", expand=True),
                            Row(
                                expand = True,
                                controls = [
                                    Checkbox("", value=True),
                                    TextField(hint_text="e.g. 1.00", expand = True)
                                ]
                            )
                        ]
                    ),
                    Row(
                        controls = [
                            Text("Title Block:", expand=True),
                            Row(
                                expand=True,
                                alignment=MainAxisAlignment.START,
                                controls = [
                                    Switch("", value=True, on_change = self.hide)
                                ]
                            )
                        ],
                        alignment=MainAxisAlignment.START
                    ),
                    self.extra_options,
                    Container(
                        padding = padding.symmetric(0, 8),
                        content = Row(
                            controls = [
                                self.proceed_button,
                                FilledButton(
                                    "Cancel", 
                                    expand=True,
                                    bgcolor="#73ff0000",
                                    on_click=lambda e: setattr(self.dia_state, 'state', Dialogs.CLOSE)
                                )
                            ],
                            alignment=MainAxisAlignment.START
                        )
                    )
                ]
            )
        )

        self.content=Container(
            padding = 8,
            height=500,
            width=720,
            expand=True,
            content = Column(
                horizontal_alignment=CrossAxisAlignment.STRETCH,
                controls=[
                    Container(
                        padding = padding.only(left=16, bottom=0, right=16, top=16),
                        expand=True,
                        content = Row(
                            expand=True,
                            spacing = 0,
                            controls = [
                                Column(
                                    expand = True,
                                    spacing = 16,
                                    controls = [
                                        Text("Export Xilogism", size=24, weight=FontWeight.BOLD),
                                        Container(
                                            content = Text(""),
                                            width = 300,
                                            expand=True,
                                            border_radius=8,
                                            border=border.all(1, "black"),
                                            bgcolor="white",
                                        )
                                    ]
                                ),
                                Container(
                                    expand = True,
                                    padding = padding.only(top = 48),
                                    content = Column(
                                        expand=True,
                                        horizontal_alignment=CrossAxisAlignment.CENTER,
                                        controls = [
                                            self.navigator,
                                            self.main_options
                                        ]
                                    )
                                )
                            ]
                        )
                    )
                ]
            )
        )
    
    def hide(self, event: ControlEvent):
        self.extra_options.content_hidden = not self.extra_options.content_hidden
        self.extra_options.update()
    
    def change_view(self, event: ControlEvent):
        active = int(event.data[2])
        self.print_export_setting.switch(active)
        segment: SegmentedButton = event.control
        self.proceed_button.text = segment.segments[active].label.value
        self.proceed_button.update()
    
class ExportTab(Tab):
    def __init__(self, on_cancel = None):
        super().__init__() 
        self.text = "Export"
        self.expand = True

        self.extra_info = Revealer(
            expand = True,
            orientation=Revealer.Orientation.VERTICAL,
            content = Container(
                expand = True,
                padding = padding.symmetric(8, 24),
                border = border.all(1, "#73191f51"),
                border_radius = 8,
                content = Column(
                    expand = True,
                    scroll = ScrollMode.HIDDEN,
                    controls = [
                        Row(
                            expand = True,
                            height=36,
                            controls = [
                                Text("Project Name:", expand=True),
                                TextField(
                                    hint_text="e.g. Xilogism 1",
                                    expand=True,
                                    text_size=14,
                                    content_padding=padding.symmetric(8, 12)
                                )
                            ]
                        ),
                        Row(
                            expand = True,
                            height=36,
                            controls = [
                                Text("Creator :", expand=True),
                                TextField(
                                    hint_text="e.g. User",
                                    expand=True,
                                    text_size=14,
                                    content_padding=padding.symmetric(8, 12)
                                )
                            ]
                        ),
                        Row(
                            expand = True,
                            height=36,
                            controls = [
                                Text("Date:", expand=True),
                                TextField(
                                    hint_text="e.g. 04/07/2025",
                                    expand=True,
                                    text_size=14,
                                    content_padding=padding.symmetric(8, 12)
                                )
                            ]
                        )
                    ]
                )
            )
        )

        self.content = Container(
            padding=padding.symmetric(8, 0),
            content = Column(
                expand = True,
                controls = [
                    Row(
                        controls = [
                            Text("File Format:", expand=True),
                            DropdownM2(
                                "pdf",
                                expand = True,
                                options=[
                                    DropdownOption(
                                        "pdf",
                                        "PDF",
                                        text_style=TextStyle(size=16)
                                    ),
                                    DropdownOption(
                                        "png",
                                        "PNG",
                                        text_style=TextStyle(size=16)
                                    ),
                                    DropdownOption(
                                        "docx",
                                        "DOCX",
                                        text_style=TextStyle(size=16)
                                    ),
                                ]
                            )
                        ]
                    ),
                    Row(
                        controls = [
                            Text("Margin:", expand=True),
                            Row(
                                expand = True,
                                controls = [
                                    Checkbox("", value=True),
                                    TextField(hint_text="e.g. 1.00", expand = True)
                                ]
                            )
                        ]
                    ),
                    Row(
                        controls = [
                            Text("Title Block:", expand=True),
                            Row(
                                expand=True,
                                alignment=MainAxisAlignment.START,
                                controls = [
                                    Switch("", value=True, on_change = self.hide)
                                ]
                            )
                        ],
                        alignment=MainAxisAlignment.START
                    ),
                    self.extra_info,
                    Container(
                        padding = padding.symmetric(0, 8),
                        content = Row(
                            controls = [
                                FilledButton(
                                    "Export", 
                                    expand=True,

                                ),
                                FilledButton(
                                    "Cancel", 
                                    expand=True,
                                    bgcolor="#73ff0000",
                                    on_click=lambda e: on_cancel()
                                )
                            ],
                            alignment=MainAxisAlignment.START
                        )
                    )
                ]
            )
        )
    
    def hide(self, event: ControlEvent):
        self.extra_info.content_hidden = not self.extra_info.content_hidden
        self.extra_info.update()

class PrintTab(Tab):
    def __init__(self, on_cancel = None):
        super().__init__()

        self.extra_info = Revealer(
            expand = True,
            orientation=Revealer.Orientation.VERTICAL,
            content = Container(
                expand = True,
                padding = padding.symmetric(8, 24),
                border = border.all(1, "#73191f51"),
                border_radius = 8,
                content = Column(
                    expand = True,
                    scroll = ScrollMode.HIDDEN,
                    controls = [
                        Row(
                            expand = True,
                            height=36,
                            controls = [
                                Text("Project Name:", expand=True),
                                TextField(
                                    hint_text="e.g. Xilogism 1",
                                    expand=True,
                                    text_size=14,
                                    content_padding=padding.symmetric(8, 12)
                                )
                            ]
                        ),
                        Row(
                            expand = True,
                            height=36,
                            controls = [
                                Text("Creator :", expand=True),
                                TextField(
                                    hint_text="e.g. User",
                                    expand=True,
                                    text_size=14,
                                    content_padding=padding.symmetric(8, 12)
                                )
                            ]
                        ),
                        Row(
                            expand = True,
                            height=36,
                            controls = [
                                Text("Date:", expand=True),
                                TextField(
                                    hint_text="e.g. 04/07/2025",
                                    expand=True,
                                    text_size=14,
                                    content_padding=padding.symmetric(8, 12)
                                )
                            ]
                        )
                    ]
                )
            )
        )

        self.text = "Print"
        self.expand = True
        self.content = Container(
            padding=padding.symmetric(8, 0),
            content = Column(
                expand = True,
                controls = [
                    Row(
                        controls = [
                            Text("Page Size:", expand=True),
                            DropdownM2(
                                "letter",
                                expand = True,
                                text_style=TextStyle(size=14, color="black"),
                                options=[
                                    DropdownOption(
                                        "letter",
                                        "Letter 8.5 x 14 in",
                                        text_style=TextStyle(size=12, color="black")
                                    ),
                                    DropdownOption(
                                        "folio",
                                        "Folio 8.5 x 13 in",
                                        text_style=TextStyle(size=12, color="black")
                                    ),
                                    DropdownOption(
                                        "legal",
                                        "Legal 8.5 x 14 in",
                                        text_style=TextStyle(size=12, color="black")
                                    ),
                                    DropdownOption(
                                        "a4",
                                        "A4 8.3 x 11.7 in",
                                        text_style=TextStyle(size=12, color="black")
                                    ),
                                    DropdownOption(
                                        "b4",
                                        "B4 9.8 x 13.9 in",
                                        text_style=TextStyle(size=12, color="black")
                                    ),
                                ]
                            )
                        ]
                    ),
                    Row(
                        controls = [
                            Text("Margin:", expand=True),
                            Row(
                                expand = True,
                                controls = [
                                    Checkbox("", value=True),
                                    TextField(hint_text="e.g. 1.00", expand = True)
                                ]
                            )
                        ]
                    ),
                    Row(
                        controls = [
                            Text("Title Block:", expand=True),
                            Row(
                                expand=True,
                                alignment=MainAxisAlignment.START,
                                controls = [
                                    Switch("", value=True, on_change=self.hide)
                                ]
                            )
                        ],
                        alignment=MainAxisAlignment.START
                    ),
                    self.extra_info,
                    Container(
                        padding = padding.symmetric(0, 8),
                        content = Row(
                            controls = [
                                FilledButton(
                                    "Print", 
                                    expand=True,

                                ),
                                FilledButton(
                                    "Cancel", 
                                    expand=True,
                                    bgcolor="#73ff0000",
                                    on_click=lambda e: on_cancel()
                                )
                            ],
                            alignment=MainAxisAlignment.START
                        )
                    )
                ]
            )
        )
    
    def hide(self, event: ControlEvent):
        self.extra_info.content_hidden = not self.extra_info.content_hidden
        self.extra_info.update()