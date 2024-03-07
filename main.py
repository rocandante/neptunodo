import flet as ft

# Define los estilos para el tema light/dark
_dark: str = ft.colors.with_opacity(0.5, "white")
_light: str = ft.colors.with_opacity(1, "black")

toggle_style_sheet: dict = {"icon": ft.icons.DARK_MODE_ROUNDED, "icon_size": 18}


def main(page: ft.Page):
    page.title = "Neptunodo ToDo App"
    page.window_maximizable = False
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.window_resizable = False
    page.window_width = "390"

    # Establece el tema por defecto
    page.theme_mode = ft.ThemeMode.LIGHT
    theme = ft.Theme()
    page.theme = theme

    # Define el encabezado
    title: ft.Text = ft.Text("Neptunodo", size=20, weight="w800")
    toggle: ft.IconButton = ft.IconButton(
        **toggle_style_sheet, on_click=lambda e: switch(e)
    )

    mainpage: ft.Column = ft.Column(
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[title, toggle],
            ),
            ft.Divider(height=20),
        ]
    )

    def switch(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            toggle.icon = ft.icons.DARK_MODE_ROUNDED

        else:
            page.theme_mode = ft.ThemeMode.DARK
            toggle.icon = ft.icons.LIGHT_MODE_ROUNDED

        page.update()

    page.add(mainpage)
    page.window_width = "390"
    page.update()


# ft.app(target=main, view=ft.AppView.WEB_BROWSER)
ft.app(target=main, assets_dir="assets")
