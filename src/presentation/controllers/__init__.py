from presentation.controllers.title_buttons_controller import TitleButtonsController
from presentation.controllers.window_controller import WindowController
from presentation.controllers.sidebar_hide_controller import SideBarHideController
from presentation.controllers.active_sidebar_button_controller import ActiveSideBarButtonController
from presentation.controllers.active_file_controller import ActiveFileController
from presentation.controllers.editor_view_fonts_controller import EditorViewFontsController
from presentation.controllers.settings_navigator_controller import SettingsNavigatorController
from presentation.controllers.dialog_state_controller import DialogStateController
from presentation.controllers.editor_content_state_controller import EditorContentStateController
from presentation.controllers.dark_mode_controller import DarkModeController

from flet import Page

def InitControllers(target: Page = None):
    WindowController(target)
    TitleButtonsController(target)
    SideBarHideController(target)
    ActiveSideBarButtonController(target)
    ActiveFileController(target)
    EditorViewFontsController(target)
    SettingsNavigatorController(target)
    DialogStateController(target)
    EditorContentStateController(target)
    DarkModeController(target)