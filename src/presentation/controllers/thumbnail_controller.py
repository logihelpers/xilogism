from presentation.states.render_state import RenderState
from flet import Page
import io
import base64
import os
import numpy as np
from PIL import Image

from presentation.controllers.controller import *

class ThumbnailController(Controller):
    priority = Priority.NONE
    def __init__(self, page: Page):
        self.page = page
        self.r_state = RenderState()
        self.r_state.on_image_change = self.update_thumbnails
    
    def update_thumbnails(self, image_dict: dict):
        key_name, image = image_dict.popitem()

        if key_name == "New":
            return

        image_data = base64.b64decode(image)
        image_stream = io.BytesIO(image_data)

        try:
            image_stream.seek(0)
            img = Image.open(image_stream)
            if img.mode != "RGBA":
                img = img.convert("RGBA")
        except Exception as e:
            raise ValueError(f"Error loading image: {e}")

        img_array = np.array(img)

        alpha = img_array[:, :, 3]
        non_transparent = np.where(alpha > 0)
        if len(non_transparent[0]) == 0:
            raise ValueError("No non-transparent content found")
        y_min, y_max = np.min(non_transparent[0]), np.max(non_transparent[0])
        x_min, x_max = np.min(non_transparent[1]), np.max(non_transparent[1])

        content = img.crop((x_min, y_min, x_max + 1, y_max + 1))
        content_width, content_height = content.size

        img_width, img_height = img.size
        final_img = Image.new("RGBA", (img_width, img_height), (0, 0, 0, 0))

        paste_x = (img_width - content_width) // 2
        paste_y = (img_height - content_height) // 2

        final_img.paste(content, (paste_x, paste_y))

        save_path = "thumbnails"
        os.makedirs(save_path, exist_ok=True)
        filename = os.path.join(save_path, f"thumbnail_{key_name}.png")
        final_img.save(filename, format="PNG")