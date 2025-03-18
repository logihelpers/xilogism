import flet as ft
from presentation.views.dialogs.registration_dialog import RegistrationDialog

class SideBar(ft.Container):
    widget_scale: float = 1.0
    old_scale: float = 1.0
    def __init__(self):
        super().__init__(
            animate_offset=200,
            animate=ft.animation.Animation(200, ft.AnimationCurve.LINEAR),
        )
        self.active = "Start"        
        self.bgcolor = "#d9d9d9"
        self.width = 180 * self.widget_scale
        self.offset = ft.transform.Offset(0, 0)
        self.padding = ft.padding.all(0)
        self.margin = ft.margin.all(0)
        self.border=ft.border.only(right=ft.BorderSide(1, color="#6d6d6d"))

        top_column = ft.Column(
            controls = [
                ft.WindowDragArea(
                    content=ft.Container(
                        border=ft.border.only(bottom=ft.BorderSide(1, "#6b6b6b")),
                        padding=ft.padding.all(16 * self.widget_scale),
                        content=ft.FilledButton(
                            bgcolor="#00191f51",
                            content = ft.Row(
                                controls=[
                                    ft.Image(
                                        src="icons_light/guest_user.png",
                                        width=24 * self.widget_scale,
                                        height=24 * self.widget_scale
                                    ),
                                    ft.Text("Guest User", weight=ft.FontWeight.W_700, color="black", size=18 * self.widget_scale)
                                ]
                            ),
                            on_click=self.open
                        )
                    )
                ),
                ft.Column(
                    controls = [
                        SideBar.Title("Home", is_home=True),
                        SideBar.Button("icons_light/start.png", "Start", on_button_press=self.new),
                        SideBar.Button("icons_light/new.png", "New Xilogism", on_button_press=self.new),
                        SideBar.Button("icons_light/open.png", "Open Xilogism"),
                        SideBar.Title("Pinned"),
                        SideBar.Button("icons_light/logo.png", "Xilogism 1"),
                        SideBar.Button("icons_light/logo.png", "Logic Circuit 1"),
                        SideBar.Button("icons_light/logo.png", "Xilogism 2"),
                        SideBar.Title("Recent Files"),
                        SideBar.Button("icons_light/logo.png", "LCD - Lab 1"),
                        SideBar.Button("icons_light/logo.png", "LCD - Lab 2"),
                        SideBar.Button("icons_light/logo.png", "FMSS - CIRCUIT"),
                        SideBar.Title("Google Drive"),
                    ],
                    expand=True,
                    spacing=0,
                    scroll=True
                )
            ],
            expand=True,
            spacing=0
        )
        
        self.content = top_column
    
    def open(self, event):
        dialog = RegistrationDialog()
        self.page.open(dialog)
    
    def new(self):
        pass

    def scale_all(self, scale: float):
        if abs(scale - self.old_scale) > 0.05:
            self.widget_scale = scale
            self.build()
            self.update()

            SideBar.Title.scale_all(scale)
            SideBar.Button.scale_all(scale)

            self.old_scale = scale

    class Title(ft.Container):
        refs: dict = dict()
        widget_scale: float = 1.0
        def __init__(self, title: str, is_home: bool = False):
            super().__init__()
            self.title = title
            self.is_home = is_home

        def build(self):
            self.content = ft.Row(
                controls = [
                    ft.Text(self.title, weight=ft.FontWeight.W_700, color="black", size=14 * self.widget_scale),
                    ft.Container(
                        content=ft.Image(
                            src="/icons_light/settings_more.png",
                            width=16 * self.widget_scale,
                            height=16 * self.widget_scale
                        ),
                        bgcolor="#00191f51",
                        visible = not self.is_home,
                        shape=ft.BoxShape.CIRCLE,
                        on_hover=self.__on_title_hover
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
            self.padding = ft.padding.only(
                8 * self.widget_scale, 
                12 * self.widget_scale, 
                8 * self.widget_scale, 
                8 * self.widget_scale
            )

            SideBar.Title.refs[self.title] = self

            super().build()
        
        def __on_title_hover(self, event: ft.ControlEvent):
            event.control.bgcolor = "#4d191f51" if event.data == "true" else "#d9d9d9"
            event.control.update()
        
        @staticmethod
        def scale_all(scale: float):
            button: SideBar.Title = None
            for name, button in SideBar.Title.refs.items():
                button.widget_scale = scale
                button.build()
                button.update()

    class Button(ft.FilledButton):
        refs: dict = dict()
        active: bool = False
        widget_scale: float = 1.0
        def __init__(self, path: str, label: str, on_button_press = None):
            super().__init__()
            self.label = label
            self.path = path
            self.tooltip = path

            self.on_hover = self.__hover
            self.on_click = self.__on_button_press
            self.on_button_press = on_button_press
        
        def __hover(self, event: ft.ControlEvent):
            if event.control.active:
                return

            event.control.bgcolor = "#4d191f51" if event.data == "true" else "#d9d9d9"
            event.control.update()
        
        def build(self):
            self.style = ft.ButtonStyle(
                shape=ft.ContinuousRectangleBorder()
            )
            
            self.bgcolor = "#d9d9d9"

            self.content = ft.Container(
                content = ft.Row(
                    controls=[
                        ft.Image(
                            src=self.path,
                            width=16 * self.widget_scale,
                            height=16 * self.widget_scale
                        ),
                        ft.Text(self.label, weight=ft.FontWeight.W_500, color="black", size=14 * self.widget_scale)
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=ft.padding.symmetric(8 * self.widget_scale, 16 * self.widget_scale)
            )

            SideBar.Button.refs[self.label] = self

            if self.label == "Start":
                SideBar.Button.refs["Start"].active = True
                SideBar.Button.refs["Start"].bgcolor = "#4d191f51"
            
            super().build()
        
        def __on_button_press(self, event: ft.ControlEvent):
            name: str = ""
            widget: SideBar.Button = None
            for name, widget in SideBar.Button.refs.items():
                if name == self.label:
                    widget.bgcolor = "#4d191f51"
                    widget.active = True
                    widget.update()
                else:
                    if widget.bgcolor == "#d9d9d9":
                        continue

                    widget.bgcolor = "#d9d9d9"
                    widget.active = False
                    widget.update()
            
            self.on_button_press()
        
        def on_button_press(self):
            pass

        @staticmethod
        def scale_all(scale: float):
            button: SideBar.Button = None
            for name, button in SideBar.Button.refs.items():
                button.widget_scale = scale
                button.build()
                button.update()