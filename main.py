"""
Neptunodo is a simple ToDo app in Python + Flet
"""

import flet as ft
import csv_operations as co

# Define los estilos para el tema light/dark
toggle_style_sheet: dict = {"icon": ft.icons.DARK_MODE_ROUNDED, "icon_size": 18}


class TodoItem(ft.UserControl):
    """
    Clase para crear y gestionar los item (tarea) que se agregan desde TodoApp
    """
    def __init__(self, value, label, delete_item):
        super().__init__()
        self.value = value
        self.label = label
        self.item = ft.Checkbox
        self.view = None
        self.delete_item = delete_item

    def build(self):
        self.item = ft.Checkbox(value=self.value, label=self.label, on_change=self.status_changed)
        self.view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.item,
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.DELETE_OUTLINE,
                            tooltip="Borrar tarea",
                            on_click=self.delete_clicked
                        )
                    ]
                )
            ]
        )

        return ft.Column(controls=[self.view])

    def status_changed(self, e):

        if e.control.value is True:
            self.item.label_style = ft.TextStyle(decoration=ft.TextDecoration.LINE_THROUGH, decoration_thickness=2)
        else:
            self.item.label_style = ft.TextStyle()

        self.item.update()

    def delete_clicked(self, e):
        self.delete_item(self)


class TodoApp(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.newtodo = ft.TextField
        self.todos = None
        self.counter: ft.Text = ft.Text(value="0 tareas", italic=True)

    def build(self):
        self.newtodo = ft.TextField(
            label="Agregar tarea",
            hint_text="Qué tienes por hacer?",
            expand=True,
            autofocus=True)
        self.todos = ft.Column()
        self.show_todos()

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
        """
        Agrega nuevos objetos checkbox a todos.controls
        """
        if not self.newtodo.value:
            self.newtodo.error_text = "Por favor escribe una tarea"
            self.newtodo.focus()
            self.update()
        else:
            # Llama a la clase TodoItem
            todo = TodoItem(False, self.newtodo.value, self.delete_item)
            self.todos.controls.append(todo)
            self.newtodo.value = ""
            self.newtodo.error_text = None
            self.newtodo.focus()

            self.count_todos()

            self.update()

    def count_todos(self):
        """
        Cuenta cuantos controles hay en el objeto self.todos.controls
        Returns: len(self.todos.controls)

        """
        if len(self.todos.controls[:]) == 1:
            self.counter.value = f"{len(self.todos.controls[:])} tareas"
        else:
            self.counter.value = f"{len(self.todos.controls[:])} tareas"

        self.counter.update()

    def show_todos(self):
        todos = co.leer_csv()
        controls = []

        for item in todos:
            todo = TodoItem(item["completed"], item["todo"], self.delete_item)
            self.todos.controls.append(todo)

        if len(todos[:]) == 1:
            self.counter.value = f"{len(todos[:])} tareas"
        else:
            self.counter.value = f"{len(todos[:])} tareas"

    def delete_item(self, todo):
        self.todos.controls.remove(todo)
        self.count_todos()
        self.update()


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
                self.todos,
                ft.Divider(height=20),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        self.todos.counter
                    ]
                )
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
