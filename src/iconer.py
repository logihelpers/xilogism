import flet as ft
import math
import flet.canvas as cv
import asyncio

import base64
from PIL import Image
from io import BytesIO
from ui.widgets.logic_circuit.canvas import LogicCanvas

async def main(page: ft.Page):
    page.window.height = 540
    page.window.width = 540
    page.bgcolor = "#ededed"
    page.padding = 0

    def save(event):
        img_data = base64.b64decode(event.data)
        img = Image.open(BytesIO(img_data))

        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Get the bounding box of non-transparent content
        alpha = img.split()[3]  # Get alpha channel
        bbox = alpha.getbbox()  # Returns (left, upper, right, lower) of non-transparent area
        
        if bbox:
            # Crop to content
            content = img.crop(bbox)
            
            # Get original dimensions
            width, height = img.size
            
            # Calculate new position to center the content
            content_width = bbox[2] - bbox[0]
            content_height = bbox[3] - bbox[1]
            
            left = (width - content_width) // 2
            top = (height - content_height) // 2
            
            # Create new transparent image
            centered_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            
            # Paste content in centered position
            centered_img.paste(content, (left, top))
    
            centered_img.save("ss.png", "PNG")

    canvas = LogicCanvas()
    canvas.on_capture = save
    canvas.expand = True
    stroke_paint = ft.Paint(stroke_width=20, style=ft.PaintingStyle.STROKE)

    canvas.shapes = [
        cv.Path(
            elements=[
                cv.Path.MoveTo(100, 150),
                cv.Path.ArcTo(
                    150, 150, math.pi / 2, 3*math.pi / 4
                ),
                cv.Path.ArcTo(
                    50, 150, math.pi / 2, 3*math.pi / 4
                ),
                cv.Path.ArcTo(
                    200, 150, math.pi / 2, 3*math.pi / 4
                ),
                cv.Path.LineTo(
                    275, 400
                ),
                cv.Path.ArcTo(
                    425, 400, math.pi / 2, 3*math.pi / 4, clockwise=False
                ),
                cv.Path.ArcTo(
                    325, 400, math.pi / 2, 3*math.pi / 4, clockwise=False
                ),
                cv.Path.ArcTo(
                    375, 400, math.pi / 2, 3*math.pi / 4, clockwise=False
                ),
                cv.Path.MoveTo(
                    208.5, 275
                ),
                cv.Path.LineTo(
                    188.5, 218.50
                ),
                cv.Path.MoveTo(
                    208.5, 275
                ),
                cv.Path.LineTo(
                    228.5, 331.5
                ),
                cv.Path.MoveTo(
                    248.5, 200
                ),
                cv.Path.LineTo(
                    288.5, 313
                ),
                cv.Path.MoveTo(
                    268.5, 256.5
                ),
                cv.Path.LineTo(
                    450, 200
                ),
                cv.Path.MoveTo(
                    208.5, 275
                ),
                cv.Path.LineTo(
                    27, 331.5
                ),
            ],
            paint=stroke_paint
        )
    ]

    page.add(canvas)

    await asyncio.sleep(1)

    canvas.capture(500, 500)



ft.app(target=main)