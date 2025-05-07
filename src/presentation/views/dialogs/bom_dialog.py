from flet import *
from utils.singleton import Singleton
from xilowidgets import XDialog
from math import ceil

from presentation.states.bom_state import BOMState
from presentation.states.dialogs_state import Dialogs, DialogState
from presentation.states.language_state import LanguageState

class BOMDialog(XDialog, metaclass = Singleton):
    current_index: int = 0
    def __init__(self):
        super().__init__()

        self.bom_state = BOMState()
        self.bom_state.on_count_change = self.update_contents
        self.dia_state = DialogState()
        self.lang_state = LanguageState()

        self.elevation = 0
        self.title = "Bill of Materials"
        self.clip_behavior = ClipBehavior.HARD_EDGE
        self.bgcolor = "#ededed"
        self.actions_padding = padding.all(16)
        self.action_button_padding = 0
        self.actions_overflow_button_spacing = 0
        self.open_duration = 300
        self.modal = True

        self.close_button = FilledButton(
            "Close", 
            width=128,
            bgcolor="#4d191f51",
            color="black",
            style=ButtonStyle(
                shape=RoundedRectangleBorder(8),
                padding=8
            ),
            on_click = lambda e: setattr(self.dia_state, 'state', Dialogs.CLOSE)
        )

        self.actions=[
            self.close_button
        ]
        self.actions_alignment=MainAxisAlignment.END

        self.datatable = DataTable(
            columns = [
                DataColumn(
                    Text("Amount", weight=FontWeight.BOLD)
                ),
                DataColumn(
                    Text("Part Number", weight=FontWeight.BOLD)
                ),
                DataColumn(
                    Text("Description", weight=FontWeight.BOLD)
                ),
            ],
            expand=True,
            horizontal_lines=BorderSide(1, "black"),
            vertical_lines=BorderSide(1, "black")
        )

        self.content = Container(
            padding = 8,
            height=320,
            width=400,
            expand=True,
            content = Column(
                expand=True,
                horizontal_alignment=CrossAxisAlignment.STRETCH,
                spacing=0,
                controls=[
                    self.datatable
                ]
            )
        )
    
    def did_mount(self):
        super().did_mount()
        self.lang_state.on_lang_updated = self.update_lang
        self.update_lang()
        self.update_contents()

    def update_contents(self):
        self.datatable.rows.clear()
        for item, amount in self.bom_state.counts.items():
            if item == "AND":
                self.datatable.rows.append(
                    DataRow(
                        cells=[
                            DataCell(
                                Text(ceil(amount / 4), text_align=TextAlign.CENTER)
                            ),
                            DataCell(
                                Text("7408", text_align=TextAlign.CENTER)
                            ),
                            DataCell(
                                Text("AND Gate IC", text_align=TextAlign.CENTER)
                            )
                        ]
                    )
                )
            elif item == "OR":
                self.datatable.rows.append(
                    DataRow(
                        cells=[
                            DataCell(
                                Text(ceil(amount / 4), text_align=TextAlign.CENTER)
                            ),
                            DataCell(
                                Text("7432", text_align=TextAlign.CENTER)
                            ),
                            DataCell(
                                Text("OR Gate IC", text_align=TextAlign.CENTER)
                            )
                        ]
                    )
                )
            elif item == "XOR":
                self.datatable.rows.append(
                    DataRow(
                        cells=[
                            DataCell(
                                Text(ceil(amount / 4), text_align=TextAlign.CENTER)
                            ),
                            DataCell(
                                Text("7486", text_align=TextAlign.CENTER)
                            ),
                            DataCell(
                                Text("XOR Gate IC", text_align=TextAlign.CENTER)
                            )
                        ]
                    )
                )
            elif item == "NOT":
                self.datatable.rows.append(
                    DataRow(
                        cells=[
                            DataCell(
                                Text(ceil(amount / 6), text_align=TextAlign.CENTER)
                            ),
                            DataCell(
                                Text("7404", text_align=TextAlign.CENTER)
                            ),
                            DataCell(
                                Text("HEX NOT Gate IC", text_align=TextAlign.CENTER)
                            )
                        ]
                    )
                )
        self.datatable.update()
    
    def update_lang(self):
        lang_values = self.lang_state.lang_values
        self.title = lang_values["title"]
        self.close_button.text = lang_values["close_button"]
        self.datatable.columns[0].label.value = lang_values["amount_column"]
        self.datatable.columns[1].label.value = lang_values["part_number_column"]
        self.datatable.columns[2].label.value = lang_values["description_column"]
        
        # Update descriptions in datatable rows
        for row in self.datatable.rows:
            part_number = row.cells[1].content.value
            if part_number == "7408":
                row.cells[2].content.value = lang_values["and_gate_description"]
            elif part_number == "7432":
                row.cells[2].content.value = lang_values["or_gate_description"]
            elif part_number == "7486":
                row.cells[2].content.value = lang_values["xor_gate_description"]
            elif part_number == "7404":
                row.cells[2].content.value = lang_values["not_gate_description"]
        
        self.update()
        self.datatable.update()