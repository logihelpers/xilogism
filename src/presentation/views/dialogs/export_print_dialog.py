from flet import *
from presentation.states.dialogs_state import DialogState, Dialogs
from presentation.states.render_state import RenderState
from presentation.states.export_state import ExportState, FileFormat
from presentation.states.animation_disable_state import AnimationDisableState
from presentation.states.language_state import LanguageState
from presentation.states.accent_color_state import AccentColorState
from presentation.states.active_file_state import ActiveFileState

from xilowidgets import Revealer, XDialog, Switcher, XDropdown

class ExportPrintDialog(XDialog):
    def __init__(self):
        super().__init__()

        self.dia_state = DialogState()
        self.export_state = ExportState()
        self.r_state = RenderState()
        self.r_state.on_image_change = self.update_preview
        self.ad_state = AnimationDisableState()
        self.ad_state.on_change = self.update_animations
        self.lang_state = LanguageState()
        self.ac_state = AccentColorState()
        self.af_state = ActiveFileState()

        self.content_padding = 0
        self.title_padding = 0
        self.elevation = 0
        self.clip_behavior = ClipBehavior.HARD_EDGE
        self.bgcolor = "#ededed"
        self.actions_padding = padding.all(16)
        self.action_button_padding = 0
        self.actions_overflow_button_spacing = 0
        self.open_duration = 300 if self.ad_state.state else 0
        self.modal = True

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
                            XDropdown(
                                "pdf",
                                # expand = True,
                                filled = True,
                                width = 256,
                                height = 48,
                                dense = True,
                                collapsed = True,
                                content_padding=padding.only(left=8),
                                options=[
                                    DropdownOption(
                                        _format,
                                        _format.upper(),
                                        style=ButtonStyle(
                                            text_style=TextStyle(size=16),
                                            bgcolor="#00000000"
                                        )
                                    ) for _format in ["pdf", "png", "docx", "raw_png"]
                                    # ),
                                    # DropdownOption(
                                    #     "png",
                                    #     "PNG",
                                    #     text_style=TextStyle(size=16)
                                    # ),
                                    # DropdownOption(
                                    #     "docx",
                                    #     "DOCX",
                                    #     text_style=TextStyle(size=16)
                                    # ),
                                    # DropdownOption(
                                    #     "raw_png",
                                    #     "RAW_PNG",
                                    #     text_style=TextStyle(size=16)
                                    # ),
                                ],
                                on_change = self.update_format
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
                            XDropdown(
                                "letter",
                                expand = True,
                                text_style=TextStyle(size=14, color="black"),
                                options=[
                                    # DropdownOption(
                                    #     "letter",
                                    #     "Letter 8.5 x 14 in",
                                    #     text_style=TextStyle(size=12, color="black")
                                    # ),
                                    # DropdownOption(
                                    #     "folio",
                                    #     "Folio 8.5 x 13 in",
                                    #     text_style=TextStyle(size=12, color="black")
                                    # ),
                                    # DropdownOption(
                                    #     "legal",
                                    #     "Legal 8.5 x 14 in",
                                    #     text_style=TextStyle(size=12, color="black")
                                    # ),
                                    # DropdownOption(
                                    #     "a4",
                                    #     "A4 8.3 x 11.7 in",
                                    #     text_style=TextStyle(size=12, color="black")
                                    # ),
                                    # DropdownOption(
                                    #     "b4",
                                    #     "B4 9.8 x 13.9 in",
                                    #     text_style=TextStyle(size=12, color="black")
                                    # ),
                                ]
                            )
                        ]
                    )
                )
            ]
        )

        self.export_button = FilledButton(
            "Export",
            key="Export",
            expand=True,
            disabled=True,
            on_click= lambda e: self.export_state.export() if e.control.key == "Export" else print("HAHA")
        )

        self.print_button = FilledButton(
            "Print",
            key="Print",
            expand=True,
            disabled=True,
            on_click= lambda e: self.export_state.print() if e.control.key == "Print" else print("HAHA")
        )

        self.project_name_tf = TextField(
            hint_text="e.g. Xilogism 1",
            expand=True,
            text_size=14,
            content_padding=padding.symmetric(8, 12),
            on_change= self.update_fields
        )

        self.creator_tf = TextField(
            hint_text="e.g. User",
            expand=True,
            text_size=14,
            content_padding=padding.symmetric(8, 12),
            on_change= self.update_fields
        )

        self.date_tf = TextField(
            hint_text="e.g. 04/07/2025",
            expand=True,
            text_size=14,
            content_padding=padding.symmetric(8, 12),
            on_change= self.update_fields
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
                                self.project_name_tf
                            ]
                        ),
                        Row(
                            expand = True,
                            height=36,
                            controls = [
                                Text("Creator :", expand=True),
                                self.creator_tf
                            ]
                        ),
                        Row(
                            expand = True,
                            height=36,
                            controls = [
                                Text("Date:", expand=True),
                                self.date_tf
                            ]
                        )
                    ]
                )
            )
        )

        self.margin_switch = Switch("", value=True, on_change = self.update_margin)
        self.titleblock_switch = Switch("", value=True, on_change = self.update_titleblock)

        self.cancel_button = FilledButton(
            "Cancel", 
            expand=True,
            bgcolor="#73ff0000",
            on_click=lambda e: setattr(self.dia_state, 'state', Dialogs.CLOSE)
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
                                    self.margin_switch
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
                                    self.titleblock_switch
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
                                self.export_button,
                                self.print_button,
                                self.cancel_button
                            ],
                            alignment=MainAxisAlignment.START
                        )
                    )
                ]
            )
        )

        self.preview_image = Image(
            width=360,
            height=240
        )

        self.content=Container(
            padding = 8,
            height=500,
            width=1024,
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
                                            content = self.preview_image,
                                            width = 420,
                                            height = 300,
                                            margin = margin.only(top=48),
                                            border_radius=8,
                                            border=border.all(1, "black"),
                                            alignment=alignment.center,
                                            image=DecorationImage(
                                                src="export_sample_bg.png"
                                            )
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
    
    def update_animations(self):
        animate = self.ad_state.state
        self.open_duration = 300 if animate else 0
        self.print_export_setting.animation_duration = 300 if animate else 25
        self.extra_options.animation_duration = 500 if animate else 0
        self.update()
    
    def update_titleblock(self, event: ControlEvent):
        self.export_state.titleblock_enable = (event.data == "true")

        if event.data == "true" and all([self.project_name_tf.value != "", self.creator_tf.value != "", self.date_tf.value != ""]):
            self.export_button.disabled = False
            self.print_button.disabled = False
        elif event.data == "false":
            self.export_button.disabled = False
            self.print_button.disabled = False
        else:
            self.export_button.disabled = True
            self.print_button.disabled = True

        self.print_button.update()
        self.export_button.update()

        self.extra_options.content_hidden = not self.extra_options.content_hidden
        self.extra_options.update()
    
    def update_preview(self, image_dict: dict):
        if image_dict == {}:
            image_str = self.r_state.image[self.af_state.active.title]
        else:
            image_str = list(image_dict.values())[0]

        try:
            self.preview_image.src_base64 = image_str
            self.preview_image.update()
        except:
            pass
    
    def update_format(self, event: ControlEvent):
        match event.data:
            case "png":
                self.export_state.format = FileFormat.PNG
                self.disable_buttons(False)
                self.export_button.disabled = True
                self.print_button.disabled = True
            case "pdf":
                self.export_state.format = FileFormat.PDF
                self.disable_buttons(False)
                self.export_button.disabled = True
                self.print_button.disabled = True
            case "docx":
                self.export_state.format = FileFormat.DOCX
                self.disable_buttons(False)
                self.export_button.disabled = True
                self.print_button.disabled = True
            case "raw_png":
                self.export_state.format = FileFormat.RAW_PNG
                self.disable_buttons(True)
                self.export_button.disabled = False
                self.print_button.disabled = False

        self.print_button.update()
        self.export_button.update()
    
    def disable_buttons(self, state: bool):
        self.margin_switch.disabled = state
        self.titleblock_switch.disabled = state
        self.project_name_tf.disabled = state
        self.creator_tf.disabled = state
        self.date_tf.disabled = state

        self.update()
    
    def update_margin(self, event: ControlEvent):
        self.export_state.margin = (event.data == "true")
        self.export_button.disabled = not (event.data == "true")
        self.export_button.update()
        self.print_button.disabled = not (event.data == "true")
        self.print_button.update()
    
    def update_fields(self, event: ControlEvent):
        if all([self.project_name_tf.value != "", self.creator_tf.value != "", self.date_tf.value != ""]):
            self.export_button.disabled = False
            self.print_button.disabled = False

            self.export_state.proj_name = self.project_name_tf.value
            self.export_state.creator = self.creator_tf.value
            self.export_state.date = self.date_tf.value
        else:
            self.export_button.disabled = True
            self.print_button.disabled = True

        self.export_button.update()
        self.print_button.update()
    
    def did_mount(self):
        super().did_mount()
        self.lang_state.on_lang_updated = self.update_lang
        self.update_lang()
        self.ac_state.on_colors_updated = self.update_colors
        self.update_colors()
    
    def update_colors(self):
        colors = self.ac_state.color_values
        self.bgcolor = colors["bg_color"]
        self.content.content.controls[0].content.controls[0].controls[0].color = colors["text_color"]  # Export Xilogism
        self.content.content.controls[0].content.controls[0].controls[1].border = border.all(1, colors["border_color"])  # Preview image
        self.print_export_setting.controls[0].content.controls[0].color = colors["text_color"]  # File Format
        self.print_export_setting.controls[0].content.controls[1].text_style = TextStyle(size=16, color=colors["text_color"])  # File Format dropdown
        for option in self.print_export_setting.controls[0].content.controls[1].options:
            option.text_style = TextStyle(size=16, color=colors["text_color"])
        self.print_export_setting.controls[1].content.controls[0].color = colors["text_color"]  # Page Size
        self.print_export_setting.controls[1].content.controls[1].text_style = TextStyle(size=14, color=colors["text_color"])  # Page Size dropdown
        for option in self.print_export_setting.controls[1].content.controls[1].options:
            option.text_style = TextStyle(size=12, color=colors["text_color"])
        self.main_options.content.controls[1].controls[0].color = colors["text_color"]  # Margin
        self.main_options.content.controls[2].controls[0].color = colors["text_color"]  # Title Block
        self.extra_options.content.border = border.all(1, colors["border_color"])  # Extra options border
        self.extra_options.content.content.controls[0].controls[0].color = colors["text_color"]  # Project Name
        self.extra_options.content.content.controls[1].controls[0].color = colors["text_color"]  # Creator
        self.extra_options.content.content.controls[2].controls[0].color = colors["text_color"]  # Date
        self.project_name_tf.bgcolor = colors["field_bgcolor"]
        self.project_name_tf.border_color = colors["field_border_color"]
        self.creator_tf.bgcolor = colors["field_bgcolor"]
        self.creator_tf.border_color = colors["field_border_color"]
        self.date_tf.bgcolor = colors["field_bgcolor"]
        self.date_tf.border_color = colors["field_border_color"]
        self.export_button.style = ButtonStyle(
            bgcolor=colors["button_bgcolor"],
            side=BorderSide(1, colors["button_border_color"])
        )
        self.export_button.color = colors["text_color"]
        self.print_button.style = ButtonStyle(
            bgcolor=colors["button_bgcolor"],
            side=BorderSide(1, colors["button_border_color"])
        )
        self.print_button.color = colors["text_color"]
        self.cancel_button.style = ButtonStyle(
            bgcolor=colors["button_bgcolor"],
            side=BorderSide(1, colors["button_border_color"])
        )
        self.cancel_button.color = colors["text_color"]
        self.update()
    
    def update_lang(self):
        lang_values = self.lang_state.lang_values
        self.content.content.controls[0].content.controls[0].controls[0].value = lang_values["export_title"]
        self.print_export_setting.controls[0].content.controls[0].value = lang_values["file_format_label"]
        self.print_export_setting.controls[1].content.controls[0].value = lang_values["page_size_label"]
        self.extra_options.content.content.controls[0].controls[0].value = lang_values["project_name_label"]
        self.extra_options.content.content.controls[1].controls[0].value = lang_values["creator_label"]
        self.extra_options.content.content.controls[2].controls[0].value = lang_values["date_label"]
        self.main_options.content.controls[1].controls[0].value = lang_values["margin_label"]
        self.main_options.content.controls[2].controls[0].value = lang_values["title_block_label"]
        self.export_button.text = lang_values["export_button"]
        self.print_button.text = lang_values["print_button"]
        self.main_options.content.controls[4].content.controls[2].text = lang_values["cancel_button"]
        self.project_name_tf.hint_text = lang_values["project_name_hint"]
        self.creator_tf.hint_text = lang_values["creator_hint"]
        self.date_tf.hint_text = lang_values["date_hint"]
        # self.print_export_setting.controls[0].content.controls[1].options[0].text = lang_values["pdf_option"]
        # self.print_export_setting.controls[0].content.controls[1].options[1].text = lang_values["png_option"]
        # self.print_export_setting.controls[0].content.controls[1].options[2].text = lang_values["docx_option"]
        # self.print_export_setting.controls[0].content.controls[1].options[3].text = lang_values["raw_png_option"]
        # self.print_export_setting.controls[1].content.controls[1].options[0].text = lang_values["letter_option"]
        # self.print_export_setting.controls[1].content.controls[1].options[1].text = lang_values["folio_option"]
        # self.print_export_setting.controls[1].content.controls[1].options[2].text = lang_values["legal_option"]
        # self.print_export_setting.controls[1].content.controls[1].options[3].text = lang_values["a4_option"]
        # self.print_export_setting.controls[1].content.controls[1].options[4].text = lang_values["b4_option"]
        self.update()