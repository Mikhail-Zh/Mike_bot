from db import get_dict


def parseable_data(data):
    data = data.split(' ')
    return data


def check_screen(lst):
    if ',' in lst[2]:
        items = lst[2].split(',')
        lst[2] = '.'.join(items)

    current = get_dict((lst[0], lst[1]))
    if current is None:
        return 'Задано не верное сечение'
    else:
        result = int((current / float(lst[2]) ** 0.5) * 1000)
        return f'Ток термической стойкости:\n{result} А'
