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
    def __init__(self, value, label, delete_item, decoration=ft.TextDecoration.NONE, decoration_thickness=0):
        super().__init__()
        self.value = value
        self.label = label
        self.item = ft.Checkbox
        self.view = None
        self.delete_item = delete_item
        self.decoration: ft.TextDecoration = decoration
        self.decoration_thickness = decoration_thickness

    def build(self):
        self.item = ft.Checkbox(value=self.value, label=self.label, on_change=self.status_changed)
        self.item.label_style = ft.TextStyle(decoration=self.decoration, decoration_thickness=self.decoration_thickness)

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
        # Agrega el estilo al texto (label) del Checkbox de acuerdo a su estado
        if e.control.value is True:
            self.item.label_style = ft.TextStyle(decoration=ft.TextDecoration.LINE_THROUGH, decoration_thickness=2)
        else:
            self.item.label_style = ft.TextStyle()

        # Guarda el estado en el archivo cvs en item correspondiente
        # Se asume que no hay dos item con el mismo nombre
        todos = co.leer_csv()
        i = 0
        for todo in todos:
            if todo["todo"] == e.control.label:
                todos[i] = {'todo': e.control.label, 'completed': e.control.value}
                break
            i += 1

        # guarda la nueva lista de tareas
        co.escribir_cvs(todos)

        # Establece el valor del control
        self.value = e.control.value
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
                    height=400,
                    scroll=ft.ScrollMode.AUTO,
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

            # Agrega el nuevo item al archivo cvs
            todo = [[self.newtodo.value, "False"]]
            co.agregar_item(todo)

            # Limpia los controles
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

        for item in todos:
            if eval(item["completed"]) is True:
                todo = TodoItem(eval(item["completed"]), item["todo"],
                                self.delete_item, ft.TextDecoration.LINE_THROUGH, 2)
            else:
                todo = TodoItem(eval(item["completed"]), item["todo"], self.delete_item)

            self.todos.controls.append(todo)

        if len(todos[:]) == 1:
            self.counter.value = f"{len(todos[:])} tareas"
        else:
            self.counter.value = f"{len(todos[:])} tareas"

    def delete_item(self, todo):
        # Eliminar el item en el archivo cvs
        # Se asume que no hay dos tareas con el mismo nombre
        todos = co.leer_csv()
        i = 0
        for item in todos:
            if item["todo"] == todo.label:
                todos.pop(i)
                break
            i += 1

        co.escribir_cvs(todos)

        self.todos.controls.remove(todo)
        self.count_todos()
        self.update()

    def clear_clicked(self, e):
        for task in self.todos.controls[:]:
            print(task.value)
            if task.value is True:
                self.delete_item(task)


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
                        self.todos.counter,
                        ft.OutlinedButton(
                            text="Limpiar Completadas", on_click=self.todos.clear_clicked
                        )
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
    page.window_width = "390"
    page.update()


# ft.app(target=main, view=ft.AppView.WEB_BROWSER)
ft.app(target=main, assets_dir="assets")
