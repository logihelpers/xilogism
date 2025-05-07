from flet import *
from utils.singleton import Singleton
from xilowidgets import XDialog, Switcher

from presentation.states.new_save_state import NewSaveState
from presentation.states.dialogs_state import Dialogs, DialogState
import asyncio

class OnboardingDialog(XDialog, metaclass = Singleton):
    current_index: int = 0
    def __init__(self):
        super().__init__()

        self.dia_state = DialogState()
        self.ns_state = NewSaveState()

        self.elevation = 0
        self.content_padding = 8
        self.title_padding = 0
        self.clip_behavior = ClipBehavior.HARD_EDGE
        self.bgcolor = "#ededed"
        self.actions_padding = padding.all(16)
        self.action_button_padding = 0
        self.actions_overflow_button_spacing = 0
        self.open_duration = 300
        self.modal = True

        self.previous_button = FilledButton(
            "Close", 
            width=128,
            bgcolor="#4d191f51",
            color="black",
            style=ButtonStyle(
                shape=RoundedRectangleBorder(8),
                padding=8
            ),
            on_click = self.go_previous
        )

        self.next_button = FilledButton(
            "Next", 
            width=128,
            bgcolor="#4d191f51",
            color="black",
            style=ButtonStyle(
                shape=RoundedRectangleBorder(8),
                padding=8
            ),
            on_click = self.go_next
        )

        self.actions=[
            self.previous_button,
            self.next_button
        ]
        self.actions_alignment=MainAxisAlignment.SPACE_BETWEEN

        self.switcher = Switcher(
            controls = [
                OnboardingPage(
                    title_text = "Start Page – Choose Your Action",
                    image_file = "appnavigation.png",
                    description = "The Xilogism app is designed for smooth, simple navigation.\n\n"
                        "From the sidebar on the left, you can start a new project, open an existing one, or quickly jump into your recent files. "
                        "You can also pin important projects to keep them right where you need them and even link to your Google Drive for easy file management.\n\n"
                        "When you land on the Start Page, you’ll see two main options:\n"
                        "• Create My Xilogism: Start building a circuit from scratch using easy pseudocode format.\n"
                        "• Open Existing: Load a previous project and pick up right where you left off."
                ),
                OnboardingPage(
                    title_text="Settings – Set It Your Way!",
                    image_file="settings.png",
                    description="You can adjust the look of your Xilogism app to match your style. You can switch between dark mode and light mode, "
                        "and even choose your preferred accent color to make the app feel just right for you.\n\n"
                        "Try it: Go to the Settings and switch between dark and light mode. Then, pick a different color theme from the color options available.\n\n"
                        "Apply and you’ll instantly see your app’s appearance change — making your workspace more comfortable and personal while you work on your logic projects."
                ),
                OnboardingPage(
                    title_text="Input – Type Your Pseudocode!",
                    image_file="input.png",
                    description="This section is where you enter your pseudocode or logic statements. This is the starting point for converting your code into a digital circuit.\n\n"
                        "Try it: Type a simple logic statement into the input box like A AND B.\n\n"
                        "As you proceed, Xilogism will take that input and start preparing it for visual translation in the next steps.",
                ),
                OnboardingPage(
                    title_text="Logic Gates – Build Your Circuits!",
                    image_file="gates.jpg",
                    description="In Xilogism, you’ll use basic logic gates to turn your pseudocode into real circuit diagrams. Each gate represents a simple logical function "
                        "that you’ll combine to build more complex systems.\n\n"
                        "Try it: When creating your Xilogism, you’ll select and connect these gates to match the logic you describe in your pseudocode.\n\n"
                        "These basic building blocks are all you need to create powerful, functional digital circuits!"
                ),
                OnboardingPage(
                    title_text="Output – See Your Code Come Alive!",
                    image_file="output.png",
                    description="In this section, you can see the conversion of your code into a circuit diagram. As you code, the diagram updates to show your logic in action.\n\n"
                        "Try it: Enter or adjust your pseudocode in the Input section. The Output will automatically display the generated circuit diagram.\n\n"
                        "This helps you check if your logic is correct and working as expected. You can make changes anytime before exporting your work."
                ),
                OnboardingPage(
                    title_text="Export – Save Your Creation!",
                    image_file="export.png",
                    description="Once you're happy with your circuit diagram, use the Export section to save your files for future use or for uploading to other platforms.\n\n"
                        "Try it: Tap the Export option and select your desired file format, like .PDF or .png for your circuit diagram.\n\n"
                        "Now your project is saved and ready to share, simulate, or build upon wherever and whenever you need it!"
                )
            ],
            orientation=Switcher.Orientation.HORIZONTAL,
            animation_duration=500,
            animation_curve=AnimationCurve.EASE_IN_OUT_CIRC
        )

        self.content = Container(
            padding = 8,
            height=480,
            width=960,
            expand=True,
            content = Column(
                expand=True,
                horizontal_alignment=CrossAxisAlignment.STRETCH,
                spacing=0,
                controls=[
                    self.switcher
                ]
            )
        )
    
    def go_previous(self, _):
        if self.current_index == 0:
            self.dia_state.state = Dialogs.CLOSE
            self.current_index = 0
        else:
            self.previous_button.text = "Close" if self.current_index == 1 else "Previous"
            self.previous_button.update()
            self.next_button.text = "Next" if self.current_index <= (len(self.switcher.controls) - 1) else "Finish"
            self.next_button.update()

            self.current_index = self.current_index - 1
            self.switcher.switch(self.current_index)

    async def go_next(self, _):
        if self.current_index == len(self.switcher.controls) - 1:
            self.dia_state.state = Dialogs.CLOSE
            await asyncio.sleep(0.1)
            self.current_index = 0
        else:
            self.next_button.text = "Finish" if self.current_index == (len(self.switcher.controls) - 2) else "Next"
            self.next_button.update()
            self.previous_button.text = "Previous" if self.current_index >= 0 else "Close"
            self.previous_button.update()

            self.current_index = self.current_index + 1
            self.switcher.switch(self.current_index)

class OnboardingPage(Column):
    def __init__(self, title_text: str, image_file: str, description: str):
        super().__init__()

        self.expand = True
        self.scroll = ScrollMode.AUTO
        self.controls = [
            Container(
                expand = True,
                content=Text(title_text, size=24, weight=FontWeight.BOLD, color="black"),
                alignment=alignment.top_left,
                padding=padding.only(left=16, top=16)
            ),
            Container(
                expand=True,
                padding=padding.symmetric(horizontal=16, vertical=8),
                content=Row(
                    expand=True,
                    spacing=30,
                    controls=[
                        Container(
                            expand=True,
                            content=Image(
                                src=image_file,
                                fit=ImageFit.FILL,
                                width=400,
                                height=240,
                            ),
                            height=400
                        ),
                        Container(
                            expand=True,
                            content=Column(
                                alignment=MainAxisAlignment.CENTER,
                                expand=True,
                                scroll=ScrollMode.AUTO,
                                controls=[
                                    Text(
                                        description,
                                        size=16,
                                        text_align=TextAlign.JUSTIFY,
                                        color="black",
                                        expand=True
                                    )
                                ]
                            )
                        )
                    ]
                )
            )
        ]