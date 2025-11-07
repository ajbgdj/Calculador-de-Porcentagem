import uuid
from typing import Dict, List, Union

import flet as ft

from core.use_cases.calculate_inverse_percentage import \
    calculate_inverse_percentage


def setup_calculator_view(page: ft.Page):
    """

    Configura a view da calculadora de porcentagem inversa
    com funcionalidades avançadas.

    """

    page.title = "Calculadora de Acumulação de Porcentagem"

    page.vertical_alignment = ft.MainAxisAlignment.START

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # --- Estado da Sessão ---

    if not page.session.contains_key("entries"):

        page.session.set("entries", [])

    if not page.session.contains_key("total_percentage"):

        page.session.set("total_percentage", 0.0)

    if not page.session.contains_key("total_value_sum"):
        page.session.set("total_value_sum", 0.0)

    def handle_delete_click(e):
        """Callback para excluir uma entrada específica."""

        entry_id_to_delete = e.control.data

        entries = page.session.get("entries")

        entries = [entry for entry in entries if entry["id"]
                   != entry_id_to_delete]
        new_total_percentage = sum(entry['percentage'] for entry in entries)
        new_total_value = sum(entry['value'] for entry in entries)

        page.session.set("entries", entries)
        page.session.set("total_percentage", new_total_percentage)
        page.session.set("total_value_sum", new_total_value)

        update_table()

        page.update()

    def handle_copy_click(e):
        """Callback para copiar o valor da porcentagem e mostrar um SnackBar."""

        data = e.control.data

        entry_id_to_copy = data["id"]

        value_to_copy = data["value"]

        page.set_clipboard(value_to_copy)

        entries = page.session.get("entries")

        for entry in entries:

            if entry["id"] == entry_id_to_copy:

                entry["copied"] = True

                break

        page.session.set("entries", entries)

        page.snack_bar = ft.SnackBar(

            content=ft.Text(f"Valor {value_to_copy} copiado!"),

            duration=2000

        )

        page.snack_bar.open = True

        update_table()

        page.update()

    def clear_border_error(e):
        """Limpa o erro de borda de um controle quando seu valor muda."""

        e.control.border_color = None

        page.update()

    # --- Controles da UI ---

    def on_submit_base_value(e):
        """Move focus to partial_value_input when Enter is pressed."""

        partial_value_input.focus()

    def on_submit_partial_value(e):
        """Handle add and keep focus on partial_value_input when Enter is pressed."""

        handle_add_click(e)

        partial_value_input.focus()

    base_value_input = ft.TextField(

        label="Base (100%)",

        keyboard_type=ft.KeyboardType.NUMBER,

        hint_text="Ex: 3760",

        width=200,

        border_color=ft.Colors.WHITE70,

        on_submit=on_submit_base_value,

        on_change=clear_border_error

    )

    partial_value_input = ft.TextField(

        label="Parcial",

        keyboard_type=ft.KeyboardType.NUMBER,

        hint_text="Ex: 1200",

        width=200,

        border_color=ft.Colors.WHITE70,

        on_submit=on_submit_partial_value,

        on_change=clear_border_error

    )

    result_table = ft.DataTable(

        columns=[

            ft.DataColumn(ft.Text("QTD")),

            ft.DataColumn(ft.Text("VALOR")),

            ft.DataColumn(ft.Text("% 5 dec")),

            ft.DataColumn(ft.Text("Soma %")),

            ft.DataColumn(ft.Text("Ações")),

        ],

        rows=[]

    )

    total_sum_text = ft.Text(

        size=20,

        weight=ft.FontWeight.BOLD

    )

    remaining_value_text = ft.Text(

        size=16,

        weight=ft.FontWeight.BOLD,

        color=ft.Colors.GREEN

    )

    error_text = ft.Text(value="", color=ft.Colors.RED)

    def update_table():
        """Atualiza a tabela com os dados da sessão."""

        result_table.rows.clear()

        entries: List[Dict[str, Union[int, float, str]]
                      ] = page.session.get("entries")

        accumulated = 0

        for i, entry in enumerate(entries):

            accumulated += entry['percentage']

            percentage_value = f"{entry['percentage']:.5f}"

            if entry.get("copied"):

                percentage_cell_content = ft.Row(

                    [

                        ft.Text(percentage_value),

                        ft.Icon(ft.Icons.CHECK, color=ft.Colors.GREEN, size=16)

                    ],

                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN

                )

            else:

                percentage_cell_content = ft.Container(

                    content=ft.Text(percentage_value),

                    data={"id": entry["id"], "value": percentage_value},

                    on_click=handle_copy_click,

                    tooltip="Copiar valor"

                )

            result_table.rows.append(

                ft.DataRow(cells=[

                    ft.DataCell(ft.Text(str(i + 1))),

                    ft.DataCell(ft.Text(f"{entry['value']:.2f}")),

                    ft.DataCell(percentage_cell_content),

                    ft.DataCell(ft.Text(f"{accumulated:.1f}%")),

                    ft.DataCell(ft.IconButton(

                        icon=ft.Icons.DELETE,

                        icon_color=ft.Colors.RED,

                        data=entry["id"],

                        on_click=handle_delete_click,

                        tooltip="Excluir esta linha"

                    )),

                ])

            )

        total_percentage = page.session.get('total_percentage')

        total_sum_text.value = f"Soma Total: {total_percentage:.1f}%"

        total_value_sum = page.session.get("total_value_sum")
        try:
            if base_value_input.value:
                base_value = float(base_value_input.value)
                remaining_value = base_value - total_value_sum
                remaining_value_text.value = f"Restante: {remaining_value:.2f}"
                if remaining_value <= 0:
                    remaining_value_text.color = ft.Colors.RED
                else:
                    remaining_value_text.color = ft.Colors.GREEN
            else:
                remaining_value_text.value = "Restante: -"
                remaining_value_text.color = ft.Colors.GREEN
        except ValueError:
            remaining_value_text.value = "Restante: -"
            remaining_value_text.color = ft.Colors.GREEN

        check_and_update_controls_state()

    def check_and_update_controls_state():
        """Habilita ou desabilita os controles com base no estado."""

        total_percentage = page.session.get("total_percentage")

        is_full = total_percentage >= 100

        partial_value_input.disabled = is_full

        add_button.disabled = is_full

        if is_full:

            error_text.value = "Limite de 100% alcançado."

        else:

            if "Limite" in error_text.value:

                error_text.value = ""

    def handle_add_click(e):
        """Callback para o botão de adicionar com validação visual."""

        base_value_input.border_color = None

        partial_value_input.border_color = None

        try:

            base_value = float(base_value_input.value)

            partial_value = float(partial_value_input.value)

            percentage = calculate_inverse_percentage(

                total_value=base_value, partial_value=partial_value)

            entries = page.session.get("entries")

            current_total = page.session.get("total_percentage")
            new_total = current_total + percentage

            current_total_value = page.session.get("total_value_sum")
            new_total_value = current_total_value + partial_value
            page.session.set("total_value_sum", new_total_value)

            new_entry = {

                "id": str(uuid.uuid4()),

                "value": partial_value,

                "percentage": percentage,

                "copied": False,

            }

            entries.append(new_entry)

            page.session.set("entries", entries)

            page.session.set("total_percentage", new_total)

            if not base_value_input.read_only:

                base_value_input.read_only = True

            error_text.value = ""

            partial_value_input.value = ""

            update_table()

        except ValueError:

            error_text.value = "Erro: Por favor, insira números válidos em ambos os campos."

            if not base_value_input.value:

                base_value_input.border_color = ft.Colors.RED

            if not partial_value_input.value:

                partial_value_input.border_color = ft.Colors.RED

            if base_value_input.value and partial_value_input.value:

                try:

                    float(base_value_input.value)

                except ValueError:

                    base_value_input.border_color = ft.Colors.RED

                try:

                    float(partial_value_input.value)

                except ValueError:

                    partial_value_input.border_color = ft.Colors.RED

        except ZeroDivisionError:

            error_text.value = "Erro: O 'Valor Base' não pode ser zero."

            base_value_input.border_color = ft.Colors.RED

        page.update()

    def handle_clear_all_click(e):
        """Callback para limpar todo o estado."""

        page.session.set("entries", [])
        page.session.set("total_percentage", 0.0)
        page.session.set("total_value_sum", 0.0)

        base_value_input.read_only = False

        base_value_input.value = ""

        partial_value_input.value = ""

        error_text.value = ""

        base_value_input.border_color = None

        partial_value_input.border_color = None

        update_table()

        page.update()

    add_button = ft.IconButton(

        # text="Adicionar",

        bgcolor=ft.Colors.GREEN,

        icon_color=ft.Colors.WHITE,

        on_click=handle_add_click,

        icon=ft.Icons.ADD,

        tooltip="Adicionar"

    )

    clear_button = ft.IconButton(

        bgcolor=ft.Colors.RED_400,

        icon_color=ft.Colors.WHITE,

        on_click=handle_clear_all_click,

        icon=ft.Icons.CLEAR_ALL,

        tooltip="Limpar"

    )

    # Carga inicial

    update_table()

    # --- Montagem da Vista ---

    page.add(

        ft.Column(

            controls=[

                ft.Text("Calculadora de Porcentagem Inversa",

                        size=24, weight=ft.FontWeight.BOLD),

                # ft.Text("", size=24, weight=ft.FontWeight.BOLD),

                ft.Row([base_value_input, partial_value_input, add_button, clear_button],

                       alignment=ft.MainAxisAlignment.CENTER),

                ft.Container(

                    content=ft.Column(

                        [result_table],

                        scroll=ft.ScrollMode.AUTO,

                        # height=300

                    ),

                    border=ft.border.all(1, ft.Colors.GREY),

                    border_radius=ft.border_radius.all(5),

                    padding=10,

                    # expand=True,

                ),

                ft.Row(

                    [total_sum_text, remaining_value_text],

                    alignment=ft.MainAxisAlignment.CENTER,

                    spacing=40

                ),

                error_text,

            ],

            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            spacing=15,

            expand=True

        )

    )
