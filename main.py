import flet as ft


def main(page: ft.Page):
    page.title = "Neptunodo App"
    page.window_maximizable = False
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.window_resizable = False
    page.window_width = "390"

    # Set theme
    page.theme_mode = ft.ThemeMode.LIGHT
    theme = ft.Theme()
    page.theme = theme



    page.update()


# ft.app(target=main, view=ft.AppView.WEB_BROWSER)
ft.app(target=main, assets_dir="assets")