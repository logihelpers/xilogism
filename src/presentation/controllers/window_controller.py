from presentation.views.window_view import WindowView
from flet import Page

class WindowController:
    def __init__(self, page: Page):
        self.page = page

        window = WindowView()
        page.add(window)

        self.page.session.set("window", window)
        self.page.session.set("sidebar", window.sidebar)