from csv import reader


def import_csv_layout(file):
    """Загрузить слой карты (.csv)"""
    map = []
    with open(file, 'r') as layer:
        layout = reader(layer, delimiter=',')
        for row in layout:
            map.append(row)
        return map

