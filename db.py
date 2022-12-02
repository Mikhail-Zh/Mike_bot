cu = {'16': 3100, '25': 4800, '35': 6700, '50': 9600, '70': 13400,
      '95': 18100, '120': 22900, '150': 28700, '185': 35300, '240': 45800}
al = {'25': 3340, '35': 4620, '50': 6540, '70': 9110,
      '95': 12310, '120': 15520, '150': 19370, '185': 23860, '240': 30910}


def get_dict(value):
    """Получение значения из словаря по ключу"""
    return [cu.get(value), al.get(value)]


def calc_screen(values_list):
    """Вычисление экрана кабеля"""
    current, time = values_list
    screen_list = []
    for i in [cu, al]:
        for key, val in i.items():
            val = (val / float(time) ** 0.5)
            if float(current) > max(i.values()):
                screen_list.append(None)
                break
            if float(current) <= val:
                screen_list.append(key)
                break
    return screen_list


def get_all_data(update, context):
    for i in [cu, al]:
        data_list = [f'{key} мм2 - {val} A' for key, val in i.items()]
        if i == cu:
            context.bot.send_message(update.effective_chat.id, f'Данные для медных экранов кабеля')
        if i == al:
            context.bot.send_message(update.effective_chat.id, f'Данные для экранов кабеля из алюминиевого сплава')
        context.bot.send_message(update.effective_chat.id, f'{data_list}')
