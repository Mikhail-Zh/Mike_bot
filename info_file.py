def information(update, context):
    context.bot.send_message(update.effective_chat.id, f'Я бот Mike. Я умею:\n'
                                                       f'1 - подобрать сечение экрана кабеля по току термической '
                                                       f'стойкости и времени действия защиты\n'
                                                       f'2 - рассчитать величину тока термической стойкости '
                                                       f'для заданного сечения экрана кабеля с учетом времени '
                                                       f'действия защиты.')
    context.bot.send_message(update.effective_chat.id, f'В расчетах использую следующий ряд сечений:\n'
                                                       f'16, 25, 35, 50, 70, 95, 120, 150, 185, 240')
    context.bot.send_message(update.effective_chat.id, f'Понимаю следующие команды:\n'
                                                       f'/info - информация\n'
                                                       f'/start - начало работы\n'
                                                       f'/end - конец работы\n'
                                                       f'/all - вывести данные справочника сечения экранов и ')
