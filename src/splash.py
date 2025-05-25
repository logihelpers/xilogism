import tkinter as tk
import tkinter.font as tkfont
from PIL import Image, ImageDraw, ImageTk
import sys
import subprocess

def center_window(root, width, height):
    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # Calculate position
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")

def create_rounded_rectangle(width, height, radius, bg_color):
    # Create a transparent image
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    # Draw rounded rectangle
    draw.rounded_rectangle(
        (0, 0, width, height),
        radius=radius,
        fill=bg_color
    )
    return ImageTk.PhotoImage(image)

class XilogismLoadingUI:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg="white")  # Set white as transparent color
        self.root.overrideredirect(True)  # Remove titlebar
        self.root.resizable(False, False)
        self.root.attributes('-transparentcolor', 'white')  # Make white transparent

        # Set window size
        self.window_width = 680
        self.window_height = 300
        center_window(self.root, self.window_width, self.window_height)

        # Load Inter font dynamically
        try:
            # Register Inter font file
            inter_font_path = "src/assets/fonts/Inter.ttf"  # Update to your font file path
            self.inter_bold = tkfont.Font(family="Inter", size=72, weight="bold")
            self.inter_regular = tkfont.Font(family="Inter", size=16)
            self.inter_regular_2 = tkfont.Font(family="Inter", size=14)
        except Exception:
            # Fallback to Helvetica if Inter font fails to load
            self.inter_bold = tkfont.Font(family="Helvetica", size=72, weight="bold")
            self.inter_regular = tkfont.Font(family="Helvetica", size=16)

        # Create canvas for rounded background
        self.canvas = tk.Canvas(
            self.root,
            width=self.window_width,
            height=self.window_height,
            bg="white",
            highlightthickness=0
        )
        self.canvas.place(x=0, y=0)

        # Add rounded rectangle background
        self.bg_image = create_rounded_rectangle(
            self.window_width, self.window_height, 20, "#f5f5f5"
        )
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # Load and display local image
        try:
            image = Image.open("src/assets/icon.png").resize((200, 200), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(image)
            self.image_label = tk.Label(self.root, image=self.photo, bg="#f5f5f5")
            self.image_label.image = self.photo  # Keep reference
            self.image_label.place(x=20, y=50)
        except FileNotFoundError:
            # Fallback to gray placeholder if image not found
            self.image_placeholder = tk.Canvas(
                self.root,
                width=200,
                height=200,
                bg="#d3d3d3",
                highlightthickness=0
            )
            self.image_placeholder.create_rectangle(0, 0, 200, 200, fill="#d3d3d3", outline="")
            self.image_placeholder.place(x=100, y=50)

        # Text column
        self.title_label = tk.Label(
            self.root,
            text="Xilogism",
            font=self.inter_bold,  # Use dynamically loaded Inter font
            bg="#f5f5f5",
            fg="#191f51"
        )
        self.title_label.place(x=450, y=80, anchor="center")

        self.subtitle_label = tk.Label(
            self.root,
            text="Code to Circuits? Xilogized!",
            font=self.inter_regular,
            bg="#f5f5f5",
            fg="black"
        )
        self.subtitle_label.place(x=450, y=160, anchor="center")

        # Progress ring (rotating arc)
        self.progress_canvas = tk.Canvas(
            self.root,
            width=16,
            height=16,
            bg="#f5f5f5",
            highlightthickness=0
        )
        self.progress_canvas.place(x=120, y=280, anchor="center")
        self.angle = 0
        self.arc = self.progress_canvas.create_arc(
            2, 2, 14, 14,
            start=0,
            extent=90,
            outline="#4169e1",
            width=2,
            style=tk.ARC
        )

        # Loading text
        self.loading_label = tk.Label(
            self.root,
            text="Please wait while we set a few things up for you.",
            font=self.inter_regular_2,
            bg="#f5f5f5",
            fg="black"
        )
        self.loading_label.place(x=140, y=280, anchor="w")

        self.flet_process = subprocess.Popen(
            [sys.executable, "src/main.py"],  # Update to your Flet script path
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,  # Line-buffered
            universal_newlines=True
        )

        # Start animation and monitor Flet process
        self.animate()
        self.root.after(10000, self.root.destroy)
    
    def check_flet_completion(self):
        # Non-blocking read of stdout
        try:
            # Read one line from stdout
            line = self.flet_process.stdout.readline()
            if "App Launched!" in line:  # Check for completion message
                self.root.destroy()
                return
        except:
            pass
        # Check if process terminated
        if self.flet_process.poll() is not None:
            self.root.destroy()
            return
        # Schedule next check (every 100ms)
        self.root.after(100, self.check_flet_completion)

    def animate(self):
        # Update arc angle
        self.angle = (self.angle + 10) % 360
        self.progress_canvas.itemconfig(self.arc, start=self.angle)
        # Schedule next update (every 50ms)
        self.root.after(50, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    app = XilogismLoadingUI(root)
    root.mainloop()