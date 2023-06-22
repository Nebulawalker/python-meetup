ABOUT_MSG = 'Тут будет информация о нас. tg_bot/messages.py var ABOUT_MSG'


async def get_report_button_caption(report):
    if report['is_current']:
        return f'{report["topic"]}, идет прямо сейчас!'
    else:
        return f'{report["topic"]}, начало в {report["starts_at"].strftime("%H-%M (%m.%d.%Y)")}'

async def get_report_description(report):
    description = f'Тема: {report["topic"]},\nСпикер: {report["speaker"]},\n'\
                  f'Начало в {report["starts_at"].strftime("%H-%M (%m.%d.%Y)")},\nОкончание в {report["ends_at"].strftime("%H-%M (%m.%d.%Y)")}'
    return description