import csv

CSVFILE = 'data/todos.csv'


def leer_csv():
    """
    Abre un archivo csv y lo retorna como un objeto lista
    :return: data
    """
    with open(CSVFILE, newline='') as file:
        data = list(csv.DictReader(file))

    return data


def agregar_item(data):
    """
    Agrega una nueva fila de datos en un archivo csv existente
    """
    with open(CSVFILE, 'a', newline='') as file:
        f = csv.writer(file)
        f.writerows(data)


def escribir_cvs(data):
    """
    Reemplaza los datos en un archivo csv existente
    """
    with open(CSVFILE, 'w', newline='') as file:
        headers = ['todo', 'completed']
        f = csv.DictWriter(file, fieldnames=headers)
        f.writeheader()
        for row in data:
            f.writerow(row)
