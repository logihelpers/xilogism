from flet import Page, SnackBar, Text
from presentation.controllers.auth_controller import AuthController

async def autologin(page: Page):
    auth_controller = AuthController(page)
    logged_in = auth_controller.restore_session()
    if logged_in:
        page.open(SnackBar(Text("Automatically logged in!")))
    else:
        page.open(SnackBar(Text("Can't login automatically. Try manually!")))

def InitLogin(page: Page):
    page.open(SnackBar(Text("Logging in...")))
    page.run_task(autologin, page)