from presentation.states.export_state import ExportState, FileFormat
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import base64
import io
import os
import tempfile
import docx2pdf as d2f
import pypdfium2 as pdfium
import shutil
from PIL import Image as IMG

from flet import Page, margin as mg, SnackBar, Text, SnackBarBehavior

from presentation.controllers.controller import Controller, Priority
from presentation.states.render_state import RenderState
from presentation.states.sidebar_hide_state import SideBarHideState
from presentation.states.dialogs_state import Dialogs, DialogState

class ExportController(Controller):
    priority = Priority.VIEW_BOUND
    def __init__(self, page: Page):
        self.page = page

        self.export_state = ExportState()
        self.render_state = RenderState()
        self.sbh_state = SideBarHideState()
        self.dia_state = DialogState()

        self.export_state.on_export = self.export

    def export(self):
        file_format: FileFormat = self.export_state.format
        margin: bool = self.export_state.margin
        titleblock_enable: bool = self.export_state.titleblock_enable
        proj_name: str = self.export_state.proj_name
        creator: str = self.export_state.creator
        date: str = self.export_state.date

        output_filename = ""

        match file_format:
            case FileFormat.PDF:
                output_filename = self.export_to_file(margin, titleblock_enable, proj_name, creator, date, 1)
            case FileFormat.PNG:
                output_filename = self.export_to_file(margin, titleblock_enable, proj_name, creator, date, 2)
            case FileFormat.DOCX:
                output_filename = self.export_to_file(margin, titleblock_enable, proj_name, creator, date)
            case FileFormat.RAW_PNG:
                output_filename = self.export_to_png()

        if output_filename != "":
            self.dia_state.state = Dialogs.CLOSE

            self.page.open(
                SnackBar(
                    content=Text(f"Successfully exported to {output_filename}!"), 
                    behavior=SnackBarBehavior.FLOATING, 
                    duration=5000,
                    show_close_icon=True,
                    margin=mg.all(12) if not self.sbh_state.state.value else mg.only(left=212, top=12, right=12, bottom=12),
                    action="Open",
                    on_action=lambda e: os.startfile(output_filename)
                )
            )
    
    def export_to_file(self, margin: bool, titleblock_enable: bool, proj_name: str, creator: str, date: str, is_pdf = 0):
        image_data = base64.b64decode(self.render_state.image)
        image_stream = io.BytesIO(image_data)
        
        doc: Document = None
        if margin and titleblock_enable:
            doc = Document("src/assets/full.docx")

            table = doc.tables[0]

            # Insert image in merged cell 0,0 and 0,1
            image_cell = table.cell(0, 0)
            paragraph = image_cell.paragraphs[0]
            run = paragraph.add_run()
            run.add_picture(image_stream, width=Inches(5))
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

            # Fill title, creator, and date
            table.cell(1, 0).text = table.cell(1, 0).text.replace('{TITLE}', proj_name)
            table.cell(1, 1).text = table.cell(1, 1).text.replace('{CREATOR}', creator)
            table.cell(2, 1).text = table.cell(2, 1).text.replace('{DATE}', date)
        elif not margin and titleblock_enable:
            doc = Document("src/assets/no_margin.docx")

            paragraph = doc.add_paragraph()
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = paragraph.add_run()
            run.add_picture(image_stream, width=Inches(5))

            # Footer table handling
            section = doc.sections[0]
            footer = section.footer
            table = footer.tables[0]

            table.cell(0, 0).text = table.cell(0, 0).text.replace('{TITLE}', proj_name)
            table.cell(0, 1).text = table.cell(0, 1).text.replace('{CREATOR}', creator)
            table.cell(1, 1).text = table.cell(1, 1).text.replace('{DATE}', date)
        elif margin and not titleblock_enable:
            doc = Document("src/assets/no_titlebar.docx")

            table = doc.tables[0]

            # Insert image into the single large table cell
            image_cell = table.cell(0, 0)
            paragraph = image_cell.paragraphs[0]
            run = paragraph.add_run()
            run.add_picture(image_stream, width=Inches(5))
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        else:
            doc = Document("src/assets/plain.docx")
            paragraph = doc.add_paragraph()
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = paragraph.add_run()
            run.add_picture(image_stream, width=Inches(5))
        
        if is_pdf == 0:
            doc.save("test.docx")

            return "test.docx"
        elif is_pdf == 1:
            with tempfile.TemporaryDirectory() as tempdir:
                docx_path = os.path.join(tempdir, "temp.docx")
                pdf_path = "test.pdf"
        
                doc.save(docx_path)

                # Convert DOCX to PDF
                d2f.convert(docx_path, pdf_path)
            
                return pdf_path
        else:
            output_pdf_path = "copied_temp.pdf"
            with tempfile.TemporaryDirectory() as tempdir:
                docx_path = os.path.join(tempdir, "temp.docx")
                pdf_path = os.path.join(tempdir, "temp.pdf")
        
                doc.save(docx_path)

                # Convert DOCX to PDF
                d2f.convert(docx_path, pdf_path)
                shutil.copy2(pdf_path, output_pdf_path)

                pdf = pdfium.PdfDocument(output_pdf_path)

                image = pdf[0].render(scale=4).to_pil()
                image.save("test.png", format='PNG')

            return "test.png"
    
    def export_to_png(self):
        image_data = base64.b64decode(self.render_state.image)
        image_stream = io.BytesIO(image_data)

        img = IMG.open(image_stream)
    
        img.save("test.png", format='PNG')

        return "test.png"