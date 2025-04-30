from flet import *

class TutorialApp:
    def __init__(self, page: Page):
        self.page = page
        self.page.title = "Tutorial - App Navigation"
        self.page.bgcolor = "#ededed"
        self.page.horizontal_alignment = CrossAxisAlignment.CENTER
        self.page.vertical_alignment = MainAxisAlignment.START

        self.current_page = 0
        self.total_pages = 7

        self.slides = [
            self.build_main(),
            self.build_page2(),
            self.build_page3(),
            self.build_page4(),
            self.build_page5(),
            self.build_page6(),
            self.build_page7()
        ]
        self.render_page()

        self.switcher = Switcher(
            orientation=Switcher.Orientation.HORIZONTAL,
            animation_curve=AnimationCurve.EASE_IN_OUT_CUBIC,
            animation_duration=500,
            controls=[
                self.build_main(),
                self.build_page2(),
                self.build_page3(),
                self.build_page4(),
                self.build_page5(),
                self.build_page6(),
                self.build_page7()
            ]
        )

        self.title = navigator
        self.actions = [
            FilledButton(
                "Back",
                width=128,
                style=ButtonStyle(
                    color="black",
                    shape=RoundedRectangleBorder(8),
                    padding=8,
                    bgcolor="#4d191f51"
                ),
                on_click=lambda e: self.go_to_previous()
            ),
            FilledButton(
                "Next",
                width=128,
                style=ButtonStyle(
                    color="black",
                    shape=RoundedRectangleBorder(8),
                    padding=8,
                    bgcolor="#4d191f51"
                ),
                on_click=lambda e: self.go_to_next()
            ),
        ]

    def build_main(self):
        return Stack(
            controls=[
                Column(
                    expand=True,
                    controls=[
                        Container(
                            alignment=alignment.center,
                            expand=True,
                            padding=20,
                            content=Image(src="welcome.jpg", expand=True, fit=ImageFit.CONTAIN)
                        )
                    ]
                ),
                Container(
                    alignment=alignment.bottom_right,
                    padding=20,
                    content=ElevatedButton("Get Started", on_click=lambda e: self.go_to(1))
                )
            ]
        )

    def build_page2(self):
        return self.page_template("App Navigation - Find your way easily!", "appnavigation1.png", 0, 2)

    def build_page3(self):
        return self.page_template("Settings - Set it your way!", "settings.png", 1, 3)

    def build_page4(self):
        return self.page_template("Input - Type your pseudocode!", "input.png", 2, 4)

    def build_page5(self):
        return self.page_template("Logic Gates - Build your circuits!", "gates.png", 3, 5)

    def build_page6(self):
        return self.page_template("Output - See your code come alive!", "output.png", 4, 6)

    def build_page7(self):
        return Stack(
            controls=[
                Column(
                    expand=True,
                    controls=[
                        Container(
                            content=Text("Get Started!", size=24, weight=FontWeight.BOLD, color="black"),
                            alignment=alignment.top_left,
                            padding=padding.only(left=20, top=20)
                        ),
                        Container(
                            alignment=alignment.center,
                            expand=True,
                            padding=20,
                            content=Image(src="export.png", expand=True, fit=ImageFit.CONTAIN)
                        )
                    ]
                ),
                Container(
                    alignment=alignment.bottom_right,
                    padding=20,
                    content=ElevatedButton("Finish", on_click=lambda e: self.page.window_close())
                )
            ]
        )

    def page_template(self, title, image_src, back_index, next_index):
        return Stack(
            controls=[
                Column(
                    expand=True,
                    controls=[
                        Container(
                            content=Text(title, size=24, weight=FontWeight.BOLD, color="black"),
                            alignment=alignment.top_left,
                            padding=padding.only(left=20, top=20)
                        ),
                        Container(
                            alignment=alignment.center,
                            expand=True,
                            padding=20,
                            content=Image(src=image_src, expand=True, fit=ImageFit.CONTAIN)
                        )
                    ]
                ),
                Container(
                    padding=20,
                    bottom=0,
                    right=0,
                    content=Row(
                        alignment=MainAxisAlignment.END,
                        spacing=10,
                        controls=[
                            ElevatedButton("Back", on_click=lambda e: self.go_to(back_index)),
                            ElevatedButton("Next", on_click=lambda e: self.go_to(next_index))
                        ]
                    )
                )
            ]
        )

    def render_page(self):
        self.page.controls.clear()
        self.page.add(self.slides[self.current_page])
        self.page.update()

    def go_to(self, index):
        if 0 <= index < self.total_pages:
            self.current_page = index
            self.render_page()

    def go_to_previous(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.render_page()

    def go_to_next(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.render_page()

def main(page: Page):
    TutorialApp(page)

app(target=main)
