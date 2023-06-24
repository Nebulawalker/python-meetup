from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand('start', 'Начать!'),
            types.BotCommand('reports', 'Доклады'),
            types.BotCommand('donate', 'Задонатить организатору!'),
            types.BotCommand('survey', 'Ваша анкета'),
            types.BotCommand('survey_list', 'Список анкет'),
            types.BotCommand('about', 'О нас'),

        ]
    )
