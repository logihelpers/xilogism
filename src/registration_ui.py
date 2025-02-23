import flet as ft

def main(page: ft.Page):
    page.title = "Register"
    page.bgcolor = "#FFFFFF"  # Background color

    FIELD_WIDTH = 300  # Standard width for text fields and buttons
    FIELD_RADIUS = 100  # Rounded corners for all elements

    # Define the default font style with Inter
    inter_font_style = ft.TextStyle(font_family="Inter")

    # Custom Text Field Style
    def custom_textfield(label, icon, is_password=False):
        return ft.TextField(
            label=label,
            prefix_icon=icon,
            bgcolor="white",
            color='black',  # Text color inside the field
            border_radius=FIELD_RADIUS,
            border_color="#B2B2B2",
            content_padding=ft.Padding(15, 10, 10, 10),
            password=is_password,
            width=FIELD_WIDTH,
            label_style=ft.TextStyle(color='black', font_family="Inter"),  # Black label color and Inter font
        )

    # Custom Button Style
    def custom_button(text, icon=None, bgcolor="#1D2357", text_color="white"):
        return ft.ElevatedButton(
            text,
            icon=icon,
            bgcolor=bgcolor,
            color=text_color,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=FIELD_RADIUS),
                padding=ft.Padding(15, 15, 15, 15),  # Consistent padding
                text_style=ft.TextStyle(font_family="Inter")  # Apply Inter font to button text
            ),
            width=FIELD_WIDTH
        )

    # Registration Form UI
    form_container = ft.Container(
        content=ft.Column(
            [
                # Top User Icon (Left-Aligned)
                ft.Row(
                    [ft.Image(
                        src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
                        width=90,
                        height=90,
                    )],
                    alignment=ft.MainAxisAlignment.START  # Left alignment
                ),
                
                # Title & Subtitle (Left-Aligned)
                ft.Text("Register", size=40, weight=ft.FontWeight.BOLD, color="#1D2357", text_align=ft.TextAlign.LEFT, style=inter_font_style),
                ft.Container(
                    content=ft.Text("Create your account", weight=ft.FontWeight.BOLD, size=14, color="black", text_align=ft.TextAlign.LEFT, style=inter_font_style),
                    margin=ft.Margin(top=5, left=0, right=0, bottom=0),  # Adjust margin here
                ),
                
                # Register Button
                custom_button("SIGN UP WITH GOOGLE"),

                # Input Fields
                custom_textfield("Name", ft.Icons.PERSON),
                custom_textfield("Email", ft.Icons.EMAIL),
                custom_textfield("Password", ft.Icons.LOCK, is_password=True),
                
                # Register Button
                custom_button("REGISTER"),
                
                # Sign In Link
                ft.Row(
                    [
                        ft.TextButton(
                            "Already have an account? Sign In",
                            style=ft.ButtonStyle(
                                color="#1D2357",  # Apply hex color
                                text_style=ft.TextStyle(
                                    decoration=ft.TextDecoration.UNDERLINE,  # Underline text
                                    weight=ft.FontWeight.BOLD,  # Make text bold
                                    font_family="Inter"  # Use Inter font for the link
                                ),
                            ),
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER  # Keep it centered
                )
            ],
            spacing=10,  # Uniform spacing
            alignment=ft.MainAxisAlignment.START,  # Aligns everything to the left
            horizontal_alignment=ft.CrossAxisAlignment.START,  # Aligns text fields properly
        ),
        padding=30,
        border_radius=15,
        bgcolor="lightgray",
        width=350,
    )

    page.add(form_container)

    # Set window size explicitly after adding components
    page.window.width = 350
    page.window.height = 600
    page.window.resizable = False  # Optional: to prevent window resizing
    page.update()

# Run as a standalone app
ft.app(target=main, view=ft.AppView.FLET_APP)
