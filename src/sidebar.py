import flet as ft

class SideBar(ft.Container):
    def __init__(self):
        super().__init__()
        self.bgcolor = "#d9d9d9"
        self.width = 180
        self.padding = ft.padding.all(16)
        self.margin = ft.margin.all(0)

        self.new_button = SideBarButton(ft.Icons.OPEN_IN_NEW, "New File")

        top_column = ft.Column(
            controls = [
                self.new_button,
                SideBarButton(ft.Icons.FILE_OPEN, "Open")
            ],
            expand=True,
            spacing=16
        )
        
        self.content = ft.Column(
            controls = [
                top_column,
                SideBarButton(ft.Icons.SETTINGS, "Preferences")
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )


class SideBarButton(ft.ElevatedButton):
    def __init__(self, icon: ft.Icons, label: str, bgcolor: str = "#191f51", color: str = ft.Colors.WHITE):
        super().__init__()
        self.bgcolor = bgcolor
        self.height = 48
        self.content = ft.Container(
            content = ft.Row(
                controls=[
                    ft.Icon(icon, color=color, size=24),
                    ft.Text(label, style=ft.TextStyle(color=color))
                ]
            ),
            padding=8
        )