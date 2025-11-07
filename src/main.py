import flet as ft

from presentation.views.calculator_view import setup_calculator_view


def main(page: ft.Page):
    """
    Punto de entrada principal de la aplicación Flet.

    Esta función es llamada por Flet para iniciar la aplicación.
    Su responsabilidad es configurar la página y delegar la construcción
    de la vista a la capa de presentación.

    Args:
        page (ft.Page): El objeto de la página principal gestionado por Flet.
    """
    # --- Configuración de la Ventana ---
    page.window.width = 650
    page.window.height = 600
    page.window.resizable = False
    page.window.alignment = ft.alignment.center

    # Delega la construcción de la UI a la vista específica
    setup_calculator_view(page)


if __name__ == "__main__":
    # Inicia la aplicación Flet, llamando a la función main
    ft.app(target=main)
