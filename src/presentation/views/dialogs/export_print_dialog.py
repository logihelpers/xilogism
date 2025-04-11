from flet import *
from presentation.states.dialogs_state import DialogState, Dialogs

from xilowidgets import Revealer

from services.singleton import Singleton

class ExportPrintDialog(AlertDialog):
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

        self.modal = True
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
                                    content = Tabs(
                                        expand = True,
                                        selected_index=0,
                                        animation_duration=250,
                                        indicator_tab_size = True,
                                        scrollable = False,
                                        tab_alignment=TabAlignment.FILL,
                                        tabs = [
                                            ExportTab(on_cancel=lambda: setattr(self.dia_state, 'state', Dialogs.CLOSE)),
                                            PrintTab(on_cancel=lambda: setattr(self.dia_state, 'state', Dialogs.CLOSE))
                                        ]
                                    )
                                )
                            ]
                        )
                    )
                ]
            )
        )
    
class ExportTab(Tab):
    def __init__(self, on_cancel = None):
        super().__init__() 
        self.text = "Export"
        self.expand = True
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
                                    Switch("", value=True)
                                ]
                            )
                        ],
                        alignment=MainAxisAlignment.START
                    ),
                    Container(
                        expand = True,
                        padding = padding.symmetric(8, 24),
                        border = border.all(1, "#73191f51"),
                        border_radius = 8,
                        content = Revealer(
                            expand = True,
                            orientation=Revealer.Orientation.VERTICAL,
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
                    ),
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

class PrintTab(Tab):
    def __init__(self, on_cancel = None):
        super().__init__()

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
                                    Switch("", value=True)
                                ]
                            )
                        ],
                        alignment=MainAxisAlignment.START
                    ),
                    Container(
                        expand = True,
                        padding = padding.symmetric(8, 24),
                        border = border.all(1, "#73191f51"),
                        border_radius = 8,
                        content = Revealer(
                            expand = True,
                            orientation=Revealer.Orientation.VERTICAL,
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
                    ),
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