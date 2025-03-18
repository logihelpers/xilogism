from presentation.controllers.title_buttons_controller import TitleButtonsController
from presentation.controllers.window_controller import WindowController
from presentation.controllers.sidebar_hide_controller import SideBarHideController

from flet import Page

def InitControllers(target: Page = None):
    WindowController(target)
    TitleButtonsController(target)
    SideBarHideController(target)