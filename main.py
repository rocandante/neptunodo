"""
Neptunodo is a simple ToDo app in Python + Flet
"""

import flet as ft

# Define los estilos para el tema light/dark
_dark: str = ft.colors.with_opacity(0.5, "white")
_light: str = ft.colors.with_opacity(1, "black")

toggle_style_sheet: dict = {"icon": ft.icons.DARK_MODE_ROUNDED, "icon_size": 18}


class TodoApp(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.newtodo = ft.TextField
        self.todos = None

    def build(self):
        self.newtodo = ft.TextField(
            label="Agregar tarea",
            hint_text="Qué tienes por hacer?",
            expand=True,
            autofocus=True)
        self.todos = ft.Column(
            self.show_todos()
        )

        return ft.Column(
            width=390,
            controls=[
                ft.Row(
                    controls=[
                        self.newtodo,
                        ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.add_item)
                    ]
                ),
                ft.Column(
                    spacing=25,
                    controls=[
                        self.todos
                    ]
                )
            ]
        )

    def add_item(self, e):
        if not self.newtodo.value:
            self.newtodo.error_text = "Por favor escribe una tarea"
            self.newtodo.focus()
            self.update()
        else:
            todo: ft.Checkbox = ft.Checkbox(label=str(self.newtodo.value))
            self.todos.controls.append(todo)
            self.newtodo.value = ""
            self.newtodo.error_text = None
            self.newtodo.focus()
            self.update()

    def show_todos(self):
        pass


class MainPage(ft.SafeArea):
    """
    Define el layout para Page
    """
    def __init__(self, page: ft.Page):
        super().__init__(minimum=10, maintain_bottom_view_padding=True)
        self.page = page

        # Define el encabezado
        self.title: ft.Text = ft.Text("Neptunodo", size=20, weight=ft.FontWeight.W_800)
        self.toggle: ft.IconButton = ft.IconButton(
            **toggle_style_sheet, on_click=lambda e: self.switch(e)
        )
        self.todos = TodoApp()
        self.main: ft.Column = ft.Column(
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[self.title, self.toggle],
                ),
                ft.Divider(height=20),
                self.todos
            ]
        )

        self.content = self.main

    def switch(self, e):
        if self.page.theme_mode == ft.ThemeMode.DARK:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.toggle.icon = ft.icons.DARK_MODE_ROUNDED

        else:
            self.page.theme_mode = ft.ThemeMode.DARK
            self.toggle.icon = ft.icons.LIGHT_MODE_ROUNDED

        self.page.update()


def main(page: ft.Page):
    page.title = "Neptunodo ToDo App"
    page.window_maximizable = False
    # page.horizontal_alignment = ft.MainAxisAlignment.CENTER

    # Establece el tema por defecto
    page.theme_mode = ft.ThemeMode.LIGHT
    theme = ft.Theme()
    page.theme = theme

    mainpage: object = MainPage(page)

    page.add(mainpage)

    # page.window_resizable = False
    page.window_width = "390"
    page.window_max_width = "400"
    page.update()


# ft.app(target=main, view=ft.AppView.WEB_BROWSER)
ft.app(target=main, assets_dir="assets")
