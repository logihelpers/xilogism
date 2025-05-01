from flet import *
from xilowidgets import Revealer, Editor, EditorTheme

from presentation.views.widgets.settings.settings_image_button import SettingsImageButton
from presentation.views.widgets.settings.accent_color_button import AccentColorButton
from presentation.states.dark_mode_state import DarkModeState
from presentation.states.editor_theme_state import EditorThemeState
from presentation.states.custom_background_state import CustomBackgroundState
from presentation.states.accent_color_state import AccentColorState, AccentColors

class AppearanceSettings(Column):
    THEME_BUTTON_SCALE: float = 1
    def __init__(self):
        super().__init__()

        self.dm_state = DarkModeState()
        self.et_state = EditorThemeState()
        self.ac_state = AccentColorState()
        self.cb_state = CustomBackgroundState()

        self.scroll=ScrollMode.ALWAYS
        self.expand=True
        self.spacing = 16

        self.dark_mode_options = Revealer(
            orientation=Revealer.Orientation.VERTICAL,
            content_length=200,
            content = Row(
                spacing = 24,
                controls = [
                    SettingsImageButton("/screenshot_light.png", "Default", "theme_mode", on_button_press=self.switch_dark_mode),
                    SettingsImageButton("/screenshot_dark.png", "Dark", "theme_mode", on_button_press=self.switch_dark_mode)
                ]
            )
        )

        self.editor_sample = Editor(
            value="Hi, from Xilogism!!!\n\nฅ՞•ﻌ•՞ฅ\n\n",
            gutter_width=48,
            font_family="Inter",
            font_size=14,
            editor_theme=EditorTheme.OBSIDIAN
        )

        self._source_path = Text("Source Path:", visible=False, weight=FontWeight.W_600)
        self.current_path_text = Container(Text("", size=12), padding=padding.only(left=16), visible=False)
        self.background_preview = Container(
            expand = True,
            width=200,
            height=180,
            border=border.all(1, "black"),
            clip_behavior=ClipBehavior.ANTI_ALIAS,
            border_radius=8,
            bgcolor="#ededed"
        )

        self.pick_files_dialog = FilePicker(
            on_result=self.custom_background_picked,
        )

        self.use_default_button = FilledButton(
            style=ButtonStyle(
                bgcolor="#1a191f51",
                shape=RoundedRectangleBorder(16),
                side=BorderSide(1, "#1a191f51"),
                color="black"
            ),
            text="Use Default",
            expand=True,
            disabled=True,
            on_click=self.default_bg
        )

        self.controls=[
            Text("Dark Mode", weight=FontWeight.BOLD),
            Column(
                spacing = 0,
                controls = [
                    self.dark_mode_options,
                    Container(
                        content = Switch(
                            label="Follow System Dark Mode Settings:      ", 
                            label_position=LabelPosition.LEFT,
                            on_change=self.hide_panel
                        ),
                        padding=padding.only(top = 8)
                    )
                ]
            ),
            Text("Accent Color", weight=FontWeight.BOLD),
            Row(
                controls=[AccentColorButton(color, on_button_press=self.switch_accent) for color in AccentColors]
            ),
            Text("Editor Theme", weight=FontWeight.BOLD),
            Row(
                vertical_alignment=CrossAxisAlignment.START,
                alignment=MainAxisAlignment.CENTER,
                controls = [
                    Container(
                        expand = True,
                        width=200,
                        height=180,
                        border=border.all(1, "black"),
                        clip_behavior=ClipBehavior.ANTI_ALIAS,
                        border_radius=8,
                        content = Container(
                            border_radius=8,
                            content = Row(
                                expand = True,
                                controls = [
                                    self.editor_sample
                                ]
                            )
                        )
                    ),
                    Container(
                        expand = True,
                        margin = margin.only(right=16),
                        border_radius = 8,
                        content = ListView(
                            expand = True,
                            controls = [ThemeButton(theme, theme.name, self.switch_theme) for theme in EditorTheme],
                            height=180,
                            divider_thickness=1
                        ),
                        border=border.all(1, Colors.BLACK)
                    )
                ]
            ),
            Text("Custom Background", weight=FontWeight.BOLD),
            Row(
                vertical_alignment=CrossAxisAlignment.START,
                alignment=MainAxisAlignment.CENTER,
                controls = [
                    self.background_preview,
                    Container(
                        expand = True,
                        margin = margin.only(right=32),
                        content = Column(
                            expand = True,
                            horizontal_alignment=CrossAxisAlignment.STRETCH,
                            controls = [
                                self._source_path,
                                self.current_path_text,
                                Container(
                                    content = FilledButton(
                                        style=ButtonStyle(
                                            bgcolor="#36191f51",
                                            shape=RoundedRectangleBorder(16),
                                            side=BorderSide(1, "#1a191f51"),
                                            color="black"
                                        ),
                                        text="Choose Image",
                                        icon=Icons.UPLOAD_FILE,
                                        expand=True,
                                        on_click=self.pick_file,
                                        icon_color="black"
                                    ),
                                    padding=padding.symmetric(0, 16)
                                ),
                                Container(
                                    content = self.use_default_button,
                                    padding=padding.symmetric(0, 16)
                                )
                            ]
                        )
                    )
                ]
            )
        ]
    
    def did_mount(self):
        self.page.overlay.append(self.pick_files_dialog)
        self.update_bg_preview()
    
    def pick_file(self, event: ControlEvent):
        self.pick_files_dialog.pick_files(
            allowed_extensions=[
                "png",
                "jpg",
                "PNG",
                "JPEG",
                "JPG",
                "webp",
                "gif"
            ]
        )
    
    def hide_panel(self, event: ControlEvent):
        self.dark_mode_options.content_hidden = (event.data == "true")
        self.update()

        self.dm_state.follow_system_active = (event.data == "true")
                
    def switch_dark_mode(self, event: ControlEvent):
        button: SettingsImageButton = event.control

        self.dm_state.active = (button.text == "Dark")
    
    def switch_theme(self, event: ControlEvent):
        button: ThemeButton = event.control
        self.et_state.theme = button.key

        button.leading.opacity = 1
        button.leading.update()

        self.editor_sample.editor_theme = button.key
        self.editor_sample.update()
    
    def switch_accent(self, event: ControlEvent):
        button: AccentColorButton = event.control

        self.ac_state.active = button.color
    
    def custom_background_picked(self, event: FilePickerResultEvent):
        if event.files:
            path = event.files[0].path
            self.cb_state.active = path
            self._source_path.visible = True
            self.current_path_text.content.value = path
            self.current_path_text.visible = True
            self.use_default_button.disabled = False
            self.background_preview.image = DecorationImage(
                src=path,
                fit=ImageFit.FILL
            )
            self.update()
    
    def default_bg(self, event: ControlEvent):
        self.cb_state.active = None
        self._source_path.visible = False
        self.current_path_text.visible = False
        self.background_preview.image = None
        self.use_default_button.disabled = True
        self.update()
    
    def update_bg_preview(self):
        if not self.cb_state.active:
            self._source_path.visible = False
            self.current_path_text.visible = False
            self.background_preview.image = None
            self.use_default_button.disabled = True
        else:
            self._source_path.visible = True
            self.current_path_text.content.value = self.cb_state.active
            self.current_path_text.visible = True
            self.use_default_button.disabled = False
            self.background_preview.image = DecorationImage(
                src=self.cb_state.active,
                fit=ImageFit.FILL
            )
        self.update()

class ThemeButton(ListTile):
    refs: list = []
    active: bool = False
    def __init__(self, key: EditorTheme = None, name: str = None, on_button_press = None):
        super().__init__()

        self.key = key
        self.name = name

        self.leading = Icon(
            Icons.CHECK,
            color=Colors.BLACK,
            size=32,
            opacity=0
        )

        self.title = Text(name)

        self.on_click = lambda event: self.on_button_press(event)
        self.on_button_press = on_button_press

        if len(ThemeButton.refs) > 0:
            ThemeButton.refs.append(self)
        else:
            self.active = True
            
            self.leading.opacity = 1

            ThemeButton.refs.append(self)
    
    def on_button_press(self, event: ControlEvent):
        pass