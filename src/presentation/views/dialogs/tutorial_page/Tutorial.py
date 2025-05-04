from flet import *

class TutorialApp:
    def __init__(self, page: Page):
        self.page = page
        self.page.title = "Tutorial Page"
        self.page.bgcolor = "#ededed"
        self.page.horizontal_alignment = CrossAxisAlignment.CENTER
        self.page.vertical_alignment = MainAxisAlignment.CENTER

        self.current_page = 0
        self.total_pages = 7 

        logo = "logo.png"

        self.slides = [
            Column(
                expand=True,
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                        spacing=30,
                        controls=[
                            Column(
                                alignment=MainAxisAlignment.CENTER,
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                                spacing=10,
                                controls=[
                                    Text("Welcome to Xilogism", size=52, weight=FontWeight.BOLD, italic=True, color="black"),
                                    Text("Code to Circuits, Xilogized!", size=25, color="black87")
                                ]
                            ),
                            Image(
                                src=logo,
                                width=120,
                                height=120,
                                fit=ImageFit.CONTAIN
                            )
                        ]
                    )
                ]
            ),

            self.build_page("Start Page – Choose Your Action",
                            "The Xilogism app is designed for smooth, simple navigation.\n\n"
                            "From the sidebar on the left, you can start a new project, open an existing one, or quickly jump into your recent files. "
                            "You can also pin important projects to keep them right where you need them and even link to your Google Drive for easy file management.\n\n"
                            "When you land on the Start Page, you’ll see two main options:\n"
                            "• Create My Xilogism: Start building a circuit from scratch using easy pseudocode format.\n"
                            "• Open Existing: Load a previous project and pick up right where you left off.",
                            "appnavigation.png"),

            self.build_page("Settings – Set It Your Way!",
                            "You can adjust the look of your Xilogism app to match your style. You can switch between dark mode and light mode, "
                            "and even choose your preferred accent color to make the app feel just right for you.\n\n"
                            "Try it: Go to the Settings and switch between dark and light mode. Then, pick a different color theme from the color options available.\n\n"
                            "Apply and you’ll instantly see your app’s appearance change — making your workspace more comfortable and personal while you work on your logic projects.",
                            "settings.png"),

            self.build_page("Input – Type Your Pseudocode!",
                            "This section is where you enter your pseudocode or logic statements. This is the starting point for converting your code into a digital circuit.\n\n"
                            "Try it: Type a simple logic statement into the input box like A AND B.\n\n"
                            "As you proceed, Xilogism will take that input and start preparing it for visual translation in the next steps.",
                            "input.png"),

            self.build_page("Logic Gates – Build Your Circuits!",
                            "In Xilogism, you’ll use basic logic gates to turn your pseudocode into real circuit diagrams. Each gate represents a simple logical function "
                            "that you’ll combine to build more complex systems.\n\n"
                            "Try it: When creating your Xilogism, you’ll select and connect these gates to match the logic you describe in your pseudocode.\n\n"
                            "These basic building blocks are all you need to create powerful, functional digital circuits!",
                            "gates.jpg"),

            self.build_page("Output – See Your Code Come Alive!",
                            "In this section, you can see the conversion of your code into a circuit diagram. As you code, the diagram updates to show your logic in action.\n\n"
                            "Try it: Enter or adjust your pseudocode in the Input section. The Output will automatically display the generated circuit diagram.\n\n"
                            "This helps you check if your logic is correct and working as expected. You can make changes anytime before exporting your work.",
                            "output.png"),

            self.build_page("Export – Save Your Creation!",
                            "Once you're happy with your circuit diagram, use the Export section to save your files for future use or for uploading to other platforms.\n\n"
                            "Try it: Tap the Export option and select your desired file format, like .PDF or .png for your circuit diagram.\n\n"
                            "Now your project is saved and ready to share, simulate, or build upon wherever and whenever you need it!",
                            "export.png")
        ]

        self.back_button = ElevatedButton("Back", on_click=self.go_back)
        self.next_button = ElevatedButton("Get Started", on_click=self.go_next)

        self.button_row = Row(
            alignment=MainAxisAlignment.END,
            spacing=10,
            controls=[self.next_button]
        )

        self.indicator_row = Row(
            alignment=MainAxisAlignment.CENTER,
            spacing=7
        )

        self.content_column = Column(
            expand=True,
            controls=[
                Divider(height=1), 
                self.slides[self.current_page],
                Container(
                    content=self.indicator_row,
                    alignment=alignment.center,
                    padding=20
                ),
                Divider(height=1), 
                Container(
                    alignment=alignment.bottom_right,
                    padding=padding.only(right=20, bottom=20),
                    content=self.button_row
                )
            ]
        )

        self.page.add(self.content_column)
        self.update_buttons()
        self.update_indicators()

    def build_page(self, title_text, description, image_file):
        return Column(
            expand=True,
            controls=[
                Container(
                    content=Text(title_text, size=24, weight=FontWeight.BOLD, color="black"),
                    alignment=alignment.top_left,
                    padding=padding.only(left=20, top=20)
                ),
                Container(
                    expand=True,
                    padding=padding.symmetric(horizontal=20, vertical=10),
                    content=Row(
                        expand=True,
                        spacing=30,
                        controls=[
                            Container(
                                expand=1,
                                content=Image(
                                    src=image_file,
                                    expand=True,
                                    fit=ImageFit.CONTAIN
                                )
                            ),
                            Container(
                                expand=1,
                                content=Column(
                                    alignment=MainAxisAlignment.CENTER,
                                    controls=[
                                        Text(
                                            description,
                                            size=16,
                                            text_align=TextAlign.JUSTIFY,
                                            color="black"
                                        )
                                    ]
                                )
                            )
                        ]
                    )
                )
            ]
        )

    def update_buttons(self):
        self.button_row.controls.clear()
        if self.current_page == 0:
            self.next_button.text = "Get Started"
            self.button_row.controls.append(self.next_button)
        elif self.current_page == self.total_pages - 1:
            self.next_button.text = "Finish"
            self.button_row.controls.append(self.back_button)
            self.button_row.controls.append(self.next_button)
        else:
            self.next_button.text = "Next"
            self.button_row.controls.append(self.back_button)
            self.button_row.controls.append(self.next_button)
        self.page.update()

    def update_indicators(self):
        self.indicator_row.controls.clear()
        for i in range(self.total_pages):
            self.indicator_row.controls.append(
                Container(
                    width=12,
                    height=12,
                    bgcolor="black" if i == self.current_page else "#cccccc",
                    border_radius=6,
                    margin=margin.symmetric(horizontal=2)
                )
            )

    def render_page(self):
        self.content_column.controls[1] = self.slides[self.current_page]
        self.update_buttons()
        self.update_indicators()
        self.page.update()

    def go_to(self, index):
        if 0 <= index < self.total_pages:
            self.current_page = index
            self.render_page()

    def go_back(self, e):
        self.go_to(self.current_page - 1)

    def go_next(self, e):
        if self.current_page == self.total_pages - 1:
            self.page.window_close()
        else:
            self.go_to(self.current_page + 1)

def main(page: Page):
    TutorialApp(page)

app(target=main)
