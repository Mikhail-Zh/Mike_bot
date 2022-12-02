current_kz = None
section_screen = None
time_protect = None


def set_section(val_screen):
    """Устанавливает значение сечение экрана"""
    global section_screen
    section_screen = val_screen


def set_current_kz(val_tkz):
    """Устанавливает значение тока КЗ"""
    global current_kz
    current_kz = refactor(val_tkz)


def set_time(val_time):
    """Устанавливает значение времени"""
    global time_protect
    time_protect = refactor(val_time)


def get_data():
    """Возвращает значения сечения, тока, времени"""
    return [section_screen, current_kz, time_protect]


def verify(val):
    """Верификация данных введенных пользователем."""
    for char in val:
        if char in '.,':
            val = val.replace(char, '')
    if not val.isdigit():
        return 'Введено не верное значение'
    else:
        return True


def refactor(elem):
    """Заменяет запятую на точку"""
    if elem is None:
        return None
    elif ',' in elem:
        items = elem.split(',')
        return '.'.join(items)
    else:
        return elem
