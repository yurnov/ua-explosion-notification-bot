# Відправка повідомлень у телеграм-групу при появі повідомлень про вибухи у ЗМІ
![python-version](https://img.shields.io/badge/python-3.12-blue.svg)
[![license](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Невеликий [Telegram bot](https://core.telegram.org/bots/api) що працює у Docker контейнері і потребує мінімальну конфігурацію. Джерелом даних є сервер даних [Сервер даних JAAM](http://alerts.net.ua/).

## Що потрібно для роботи?
- Docker engine встановлений на хост з x86_64
- [Телеграм-бот](https://core.telegram.org/bots#6-botfather) та його токен (дивись [керівництво](https://core.telegram.org/bots/tutorial#obtain-your-bot-token))
- Chat ID чату, куди бот присиатиме повідомлення

## Налаштування
Просто надай `BOT_TOKEN` та `CHAT_ID` у файлі `.env`, можеш використовувати `.env.example` як приклад. Додатково можна обрати, щодо яких регіонів бот буде відправляти повідомлення, для цього використовуй змінну `REGION_LIST`, приклад і список регіонів, що підтримуються можеш знайти у `.env.example`.

Додатково можна налаштувати часовий пояс (за змовчуванням використовується `Europe/Kyiv` і для нього нічого вказувати не потрібно), а також вимкнути нотифікації за допомогою параметра `SLIENT` (його можна ставити у `true` чи `false`)

Також, бот може відправляти схематичну карту повітряних тривог з сервера даних [JAAM - Just another alerts map](https://github.com/J-A-A-M/ukraine_alarm_map), для цього додай параметер `MAP` (його можна ставьт у `true` чи `false`, за змовчуванням `false`). При цьому, якщо вам подобається інша карта потвітряних тривог (наприклад `https://ubilling.net.ua/aerialalerts/?map=true`), лінк на зображення (формати `png` чи `jpg`) можуть бути передані у змінній `MAP_URL`.

## Запуск
### Збудуй власний імедж

Клонуй цей репозиторій:

```shell
git https://github.com/yurnov/ua-explosion-notification-bot.git
cd ua-explosion-notification-bot
```

збудуй імедж

```shell
docker build . -t explosion-notification-bot
```

Запускай

```shell
docker run --rm -d --env-file .env explosion-notification-bot
```

Не забудь перед запуском відредагувати `.env` файл!

### Запускай готовий імедж

Відредагуй `.env` (дивись секцію налаштувань) та запускай уже збудований імедж:

```shell
docker pull ghcr.io/yurnov/explosion-notifier:latest
docker run -d --rm --env-file .env ghcr.io/yurnov/explosion-notifier:latest
```

Можеш використовувати теги `latest` для останньої випущеної версії, чи `dev` для версії, що розробляється.


## Перестороги
Це персональний проект, робота бота та актуальність даних не гарантуються. Не варто сприймати повідомлення для важливих для життя рішень!

## Подяка
Пану @v00g100skr та його [JAAM - Just another alerts map](https://github.com/J-A-A-M/ukraine_alarm_map) за ідею та сервер даних.

Але головна подяка — ЗСУ!, можете і ви подякувати їм [тут](https://koloua.com/donate)

## License
Files included in this repository is avaliable under terms of [MIT license](LICENSE). external dependency, such as [requests](https://github.com/psf/requests) is avaliable under their own licenses.

[![Stand With Ukraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/banner-direct-single.svg)](https://stand-with-ukraine.pp.ua)
