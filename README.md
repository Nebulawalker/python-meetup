# Python meetup

## Как установить

Для написания скрипта использовался __Python 3.11.0__, подойдет 3.7 и выше

- Клонировать репозиторий.
- Создать виртуальное окружение.

```bash
python -m venv env
```

- Активировать виртуальное окружение:

```bash
. env/bin/activate
```

- Установить зависимости:

```bash
pip install -r requirements.txt
```

- Переименовать файл `.env_example` в .env

```bash
mv .env_example .env
```

- Отредактировать файл `.env`

Описание содержимого:

```text
SECRET_KEY=REPLACE_ME
DEBUG=True
ALLOWED_HOSTS=127.0.0.1
ADMINS_LIST=890938240293
```

Доступны переменные:

- `DEBUG` — дебаг-режим. Поставьте True, чтобы увидеть отладочную информацию в случае ошибки.
  В случае если `DEBUG = True`, используется тестовая база данных `test_db.sqlite3`
- `SECRET_KEY` — секретный ключ проекта
- `ALLOWED_HOSTS` — см [документацию Django](https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts).
- `ADMINS_LIST` - Telegram ID администраторов.
- `TELEGRAM_BOT_TOKEN` - токен Телеграм бота проекта.
- `PAYMENTS_PROVIDER_TOKEN` - токен провайдера платежей (обязательный параметр), его нужно получить у [BotFather](https://t.me/BotFather) в настройках бота в разделе `Payments`. При тестировании проекта использовался "Сбербанк Test". Реквизиты тестовых банковских карт Сбербанка [здесь](https://securepayments.sberbank.ru/wiki/doku.php/test_cards);
- `INVOICE_IMAGE_URL` - ссылка на картинку, которая используется в счете на оплату, необязательный параметр, по умолчанию используется [эта картинка](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSOIcbg2HX4YzFqzHT5wx8dArN4wL6wut2-h010TM7MpO5D7MSZmHMUwILvY52uIF0lNDA&usqp=CAU);
- `MIN_DONATION_AMOUNT` - минимальная сумма доната, необязательный параметр, значение по умолчанию 300, больше можете узнать [здесь](https://core.telegram.org/bots/payments#supported-currencies);
- `MAX_DONATION_AMOUNT` - максимальная сумма доната, необязательный параметр, значение по умолчанию 500000, больше можете узнать [здесь](https://core.telegram.org/bots/payments#supported-currencies);

## Запуск отладочного сервера

Примените миграции:

```bash
python manage.py migrate
```

Создайте суперпользователя:

```bash
python manage.py createsuperuser
```

Запуск админки:

```bash
python manage.py runserver
```

Запуск бота:

```bash
python manage.py runbot
```

Админка бота будет [здесь](http://127.0.0.1:8000/)
