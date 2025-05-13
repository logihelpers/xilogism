from flet import *
from xilowidgets import Revealer, Editor, EditorTheme

from presentation.views.widgets.settings.settings_image_button import SettingsImageButton
from presentation.views.widgets.settings.accent_color_button import AccentColorButton
from presentation.states.dark_mode_state import DarkModeState, DarkModeScheme
from presentation.states.editor_theme_state import EditorThemeState
from presentation.states.custom_background_state import CustomBackgroundState
from presentation.states.accent_color_state import AccentColorState, AccentColors, DarkAccentColors
from presentation.states.animation_disable_state import AnimationDisableState
from presentation.states.language_state import LanguageState

class AppearanceSettings(Column):
    THEME_BUTTON_SCALE: float = 1
    def __init__(self):
        super().__init__()

        self.dm_state = DarkModeState()
        self.et_state = EditorThemeState()
        self.ac_state = AccentColorState()
        self.cb_state = CustomBackgroundState()
        self.ad_state = AnimationDisableState()
        self.ad_state.on_change = self.update_animations
        self.lang_state = LanguageState()

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

        self.choose_image_button = FilledButton(
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
                                    content = self.choose_image_button,
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
        self.lang_state.on_lang_updated = self.update_lang
        self.page.overlay.append(self.pick_files_dialog)
        self.update_bg_preview()
        self.update_accent_buttons()
        self.ac_state.on_colors_updated = self.update_colors
        self.update_colors()
    
    def update_colors(self):
        dark_mode = self.dm_state.active == DarkModeScheme.DARK
        colors = self.ac_state.color_values
        self.use_default_button.style.color = "white" if dark_mode else "black"
        self.choose_image_button.style.color = "white" if dark_mode else "black"
        self.choose_image_button.icon_color = "white" if dark_mode else "black"
        self.use_default_button.style.bgcolor = colors["button_bgcolor"].replace("4d", "1a") if dark_mode else colors["button_bgcolor"]
        self.use_default_button.style.side = BorderSide(1, colors["button_bgcolor"].replace("4d", "1a"))
        self.choose_image_button.style.bgcolor = colors["button_bgcolor"].replace("4d", "1a") if dark_mode else colors["button_bgcolor"].replace("4d", "36")
        self.choose_image_button.style.side = BorderSide(1, colors["button_bgcolor"].replace("4d", "1a"))
        self.controls[5].controls[0].border = border.all(1, "white" if dark_mode else "black")
        self.controls[5].controls[1].border = border.all(1, "white" if dark_mode else "black")
        
        button: AccentColorButton = None
        for button in AccentColorButton.refs:
            if button.color == self.ac_state.active:
                button.active = True
                button.main_content.border=border.all(2, colors["text_color"])
                button.main_content.content.value = "✓"
                button.main_content.content.color = colors["text_color"]
                button.name_text.weight = FontWeight.W_600
            else:
                button.active = False
                button.main_content.content.value = ""
            
            button.update()
        
        self.update()
    
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
        dark_mode = DarkModeScheme(button.text == "Dark")

        self.dm_state.active = dark_mode
        self.update_accent_buttons()

    def update_accent_buttons(self):
        dark_mode = self.dm_state.active
        if dark_mode == DarkModeScheme.LIGHT:
            button: AccentColorButton = None
            for index, button in enumerate(self.controls[3].controls):
                button.main_content.bgcolor = list(AccentColors)[index].value
                button.update()
        else:
            button: AccentColorButton = None
            for index, button in enumerate(self.controls[3].controls):
                button.main_content.bgcolor = list(DarkAccentColors)[index].value
                button.update()
    
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
    
    def update_animations(self):
        try:
            self.dark_mode_options.animation_duration = 500 if self.ad_state.state else 0
            self.dark_mode_options.update()
        except:
            pass

    def update_lang(self):
        lang_values = self.lang_state.lang_values
        self.controls[0].value = lang_values["dark_mode_title"]
        self.controls[1].controls[1].content.label = lang_values["follow_system_label"]
        self.controls[2].value = lang_values["accent_color_title"]
        self.controls[4].value = lang_values["editor_theme_title"]
        self.controls[6].value = lang_values["custom_background_title"]
        self.controls[7].controls[1].content.controls[0].value = lang_values["source_path"]
        self.controls[7].controls[1].content.controls[2].content.text = lang_values["choose_image_button"]
        self.controls[7].controls[1].content.controls[3].content.text = lang_values["use_default_button"]
        self.dark_mode_options.content.controls[0].label.value = lang_values["default_theme"]
        self.dark_mode_options.content.controls[1].label.value = lang_values["dark_theme"]
        self.update()

class ThemeButton(ListTile):
    refs: list = []
    active: bool = False
    def __init__(self, key: EditorTheme = None, name: str = None, on_button_press = None):
        super().__init__()

        self.key = key
        self.name = name

        self.dm_state = DarkModeState()

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

    def did_mount(self):
        super().did_mount()
        self.dm_state.on_change = self.update_colors
        self.update_colors()
    
    def update_colors(self):
        dark_mode = self.dm_state.active == DarkModeScheme.DARK
        self.leading.color = "white" if dark_mode else "black"
        self.update()