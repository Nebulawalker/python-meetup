from django.utils import timezone

ABOUT_MSG = 'Тут будет информация о нас. tg_bot/messages.py var ABOUT_MSG'
START_SURVEY_MSG = f'Далее Вам необходимо заполнить анкету.\nОбратите внимание на следующие моменты:\n'\
                   f'- Она будет доступна для просмотра другими участниками мероприятия\n'\
                   f'- Вы также сможете просматривать анкеты других участников\n'\
                   f'- В анкете будет присутствовать ссылка на Ваш аккаунт в Telegram\n'\
                   f'Если передумали заполнять анкету, нажмите /start или наберите exit'


async def get_report_button_caption(report):
    if report['is_current']:
        return f'{report["topic"]}, идет прямо сейчас!'
    else:
        return f'{report["topic"]}, начало в {timezone.localtime(report["starts_at"]).strftime("%H-%M (%m.%d.%Y)")}'


async def get_report_description(report):
    description = f'Тема: {report["topic"]},\nСпикер: {report["speaker"]},\n'\
                  f'Начало в {timezone.localtime(report["starts_at"]).strftime("%H-%M (%m.%d.%Y)")},\nОкончание в {timezone.localtime(report["ends_at"]).strftime("%H-%M (%m.%d.%Y)")}'
    return description
