from flet import *
from presentation.states.language_state import LanguageState
from presentation.states.accent_color_state import AccentColorState
from presentation.states.dark_mode_state import *

class SideBarTitle(Container):
    refs: dict = dict()
    widget_scale: float = 1.0
    def __init__(self, title: str, is_home: bool = False, on_menu_clicked = None):
        super().__init__()

        self.lang_state = LanguageState()
        self.lang_state.on_lang_updated = self.update_lang
        self.dm_state = DarkModeState()
        self.ac_state = AccentColorState()
        self.ac_state.on_colors_updated = self.update_colors

        self.settings_more = Image(
            src="/icons_light/settings_more.png",
            width=16 * self.widget_scale,
            height=16 * self.widget_scale
        )

        self.title = title
        self.is_home = is_home
        self.content = Row(
            controls = [
                Text(self.title, weight=FontWeight.W_700, color="black", size=14 * self.widget_scale, no_wrap=False, expand=True),
                Container(
                    content=PopupMenuButton(
                        content = self.settings_more,
                        items = [
                            PopupMenuItem(
                                icon = Icons.HIDE_SOURCE,
                                text = "Hide Group"
                            ),
                            PopupMenuItem(
                                icon = Icons.RESTART_ALT,
                                text = "Reload"
                            )
                        ],
                        icon_color="black"
                    ),
                    offset=transform.Offset(-0.5, 0),
                    bgcolor="#00191f51",
                    visible = not self.is_home,
                    shape=BoxShape.CIRCLE,
                    on_hover=self._on_title_hover
                )
            ],
            alignment=MainAxisAlignment.SPACE_BETWEEN
        )
        self.padding = padding.only(
            8 * self.widget_scale, 
            12 * self.widget_scale, 
            8 * self.widget_scale, 
            8 * self.widget_scale
        )

        SideBarTitle.refs[self.title] = self
    
    def _on_title_hover(self, event: ControlEvent):
        colors = self.ac_state.color_values
        control: SideBarTitle = event.control
        control.bgcolor = colors["button_bgcolor"] if event.data == "true" else colors["sidebar_color"]
        control.update()
    
    def update_lang(self):
        lang_values = self.lang_state.lang_values
        popup_menu = self.content.controls[1].content
        popup_menu.items[0].text = lang_values["hide_group"]
        popup_menu.items[1].text = lang_values["reload"]
        self.update()
    
    def update_colors(self):
        colors = self.ac_state.color_values
        dark_mode = self.dm_state.active == DarkModeScheme.DARK
        self.content.controls[0].color = colors["text_color"]  # Text
        self.content.controls[1].bgcolor = colors["button_bgcolor"]  # Container
        self.content.controls[1].content.icon_color = colors["text_color"]  # PopupMenuButton icon
        
        self.settings_more.src = "/icons_light/settings_more.png" if not dark_mode else "/icons_dark/settings_more.png"

        self.update()