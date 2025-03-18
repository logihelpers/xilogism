from presentation.controllers.title_buttons_controller import TitleButtonsController
from presentation.controllers.window_controller import WindowController
from presentation.controllers.sidebar_hide_controller import SideBarHideController
from presentation.controllers.active_sidebar_button_controller import ActiveSideBarButtonController
from presentation.controllers.active_file_controller import ActiveFileController

from flet import Page

def InitControllers(target: Page = None):
    WindowController(target)
    TitleButtonsController(target)
    SideBarHideController(target)
    ActiveSideBarButtonController(target)
    ActiveFileController(target)