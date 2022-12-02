from telegram import Bot
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, ConversationHandler
from settings import TG_TOKEN
from db import get_dict, calc_screen, get_all_data
from receiving_data import set_section, set_current_kz, set_time, get_data
from info_file import information

bot = Bot(token=TG_TOKEN)
updater = Updater(token=TG_TOKEN)
dispatcher = updater.dispatcher

start_receiving = 0
choice = 1
screen = 2
current_kz = 3
time_protection = 4


def start(update, context):
    """Начало работы с ботом."""
    context.bot.send_message(update.effective_chat.id, 'Привет! Я бот Mike.\n'
                                                       'Могу рассчитать сечение экрана кабеля по току\n'
                                                       'или величину тока для сечения.')
    context.bot.send_message(update.effective_chat.id, 'Для подробной справки напиши команду - /info')
    beginning(update, context)
    return choice


def beginning(update, context):
    """Выводит фразу бота"""
    context.bot.send_message(update.effective_chat.id, 'Для определения сечения экрана кабеля введите: 1')
    context.bot.send_message(update.effective_chat.id, 'Для определения тока КЗ экрана кабеля введите: 2')


def choice_action(update, context):
    """Выбор действия бота"""
    match update.message.text:
        case '1':
            context.bot.send_message(update.effective_chat.id, 'Введите ток КЗ, А:')
            return current_kz
        case '2':
            context.bot.send_message(update.effective_chat.id, 'Введите сечение экрана, мм2:')
            return screen


def set_current_kz_screen(update, context):
    """Получение значения тока КЗ и его передача на сохранение. Запрос времени действия защит"""
    value_tkz = update.message.text
    check = verify(value_tkz, update, context)
    if check is True:
        set_current_kz(value_tkz)
        context.bot.send_message(update.effective_chat.id, 'Время действия защиты, сек.:')
        return time_protection


def verify(val, update, context):
    """Верификация данных введенных пользователем."""
    for char in val:
        if char in '.,':
            val = val.replace(char, '')
    if not val.isdigit():
        context.bot.send_message(update.effective_chat.id, 'Введено не верное значение')
    else:
        return True


def set_section_screen(update, context):
    """Получение значения сечения экрана. Проверка существования полученных данных и передача на сохранение"""
    value_screen = update.message.text
    check = verify(value_screen, update, context)
    if check is True:
        val_scr = get_dict(value_screen)
        if val_scr[0] is None and val_scr[1] is None:
            context.bot.send_message(update.effective_chat.id, 'Заданное сечение экрана отсутствует')
        else:
            set_section(value_screen)
            context.bot.send_message(update.effective_chat.id, 'Время действия защиты, сек.:')
            return time_protection


def set_time_protect(update, context):
    """Получение значения времени. И передача на сохранение"""
    value_time = update.message.text
    check = verify(value_time, update, context)
    if check is True:
        set_time(value_time)
        data = get_data()
        calculation(data, update, context)
    return choice


def calculation(lst, update, context):
    """Выбор расчета"""
    if lst[0] is None:  # рассчитать экран
        calculation_screen([lst[1], lst[2]], update, context)
    elif lst[1] is None:  # рассчитать ток термической стойкости
        calculation_current([lst[0], lst[2]], update, context)


def calculation_screen(lst, update, context):
    """Расчет сечения экрана"""
    screen_cable_list = calc_screen(lst)
    context.bot.send_message(update.effective_chat.id, f'Для тока {lst[0]} А:')
    if screen_cable_list[0] is None:
        context.bot.send_message(update.effective_chat.id, f'Сечение медного экрана в справочнике отсутствует')
    else:
        context.bot.send_message(update.effective_chat.id, f'Сечение медного экрана {screen_cable_list[0]} мм2')
    if screen_cable_list[1] is None:
        context.bot.send_message(update.effective_chat.id, f'Сечение экрана из алюминиевого сплава в справочнике '
                                                           f'отсутствует')
    else:
        context.bot.send_message(update.effective_chat.id, f'Сечение экрана из алюминиевого сплава '
                                                           f'{screen_cable_list[1]} мм2')
    set_current_kz(None)
    context.bot.send_message(update.effective_chat.id, f'>> начнем с начала <<')
    beginning(update, context)


def calculation_current(lst, update, context):
    """Расчет тока и вывод сообщения на экран"""
    current = get_dict(lst[0])
    context.bot.send_message(update.effective_chat.id, f'При времени действия защит {lst[1]} сек.,\n'
                                                       f'ток термической стойкости:')
    if current[0] is None:
        context.bot.send_message(update.effective_chat.id, f'Значение тока для медного экрана сечением '
                                                           f'{lst[0]} мм2 отсутствует')
    else:
        result_cu = int((current[0] / float(lst[1]) ** 0.5))
        context.bot.send_message(update.effective_chat.id, f'для экрана из меди {result_cu} А')
    if current[1] is None:
        context.bot.send_message(update.effective_chat.id, f'Значение тока для экрана из алюминиевого сплава '
                                                           f'сечением {lst[0]} мм2 в справочнике отсутствует')
    else:
        result_al = int((current[1] / float(lst[1]) ** 0.5))
        context.bot.send_message(update.effective_chat.id, f'для экрана из алюминиевого сплава {result_al} А')
    set_section(None)
    set_time(None)
    context.bot.send_message(update.effective_chat.id, f'>> начнем с начала <<')
    beginning(update, context)


def cancel(update, context):
    """Закрытие бота"""
    context.bot.send_message(update.effective_chat.id, 'До встречи!')
    return ConversationHandler.END


def help_info(update, context):
    information(update, context)


def get_db(update, context):
    get_all_data(update, context)


start_handler = CommandHandler('start', start)
choice_action_handler = MessageHandler(Filters.text & (~Filters.command), choice_action)
set_current_kz_screen_handler = MessageHandler(Filters.text & (~Filters.command), set_current_kz_screen)
set_section_screen_handler = MessageHandler(Filters.text & (~Filters.command), set_section_screen)
set_time_protect_handler = MessageHandler(Filters.text & (~Filters.command), set_time_protect)
mes_data_handler = CommandHandler('end', cancel)
info_handler = CommandHandler('info', help_info)
get_db_handler = CommandHandler('all', get_db)

conv_handler = ConversationHandler(entry_points=[start_handler],
                                   states={choice: [choice_action_handler],
                                           current_kz: [set_current_kz_screen_handler],
                                           screen: [set_section_screen_handler],
                                           time_protection: [set_time_protect_handler]},
                                   fallbacks=[mes_data_handler])

dispatcher.add_handler(conv_handler)
dispatcher.add_handler(info_handler)
dispatcher.add_handler(get_db_handler)

updater.start_polling()
updater.idle()
