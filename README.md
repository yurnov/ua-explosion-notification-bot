# Відправка повідомлень у телеграм-групу при появі повідомлень про вибухи у ЗМІ
![python-version](https://img.shields.io/badge/python-3.12-blue.svg)
[![license](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Невеликий [Telegram bot](https://core.telegram.org/bots/api) що працює у Docker контейнері і потребує мінімальну конфігурацію. Джерелом даних є сервер даних [Сервер даних JAAM](http://alerts.net.ua/).

## Prerequisites
- Docker engine on x86_64 host
- A [Telegram bot](https://core.telegram.org/bots#6-botfather) and its token (see [tutorial](https://core.telegram.org/bots/tutorial#obtain-your-bot-token))
- Chat ID

## Configuration
Just provide `BOT_TOKEN` and `CHAT_ID` in the `.env` file, you may use `.env.example` as example. Alnetratively you may provide `BOT_TOKEN` as enviromental variable.


## Running
### Build own Docker image

Clone the repository and navigate to the project directory:

```shell
git clone https://github.com/yurnov/ua-explosion-notification-bot
cd ua-explosion-notification-bot
```

Build image

```shell
docker build . -t explosion-notification-bot
```

Run container

```shell
docker run --rm -d --env-file .env explosion-notification-bot
```

## Disclaimer
Це персональний проект, робота бота та актуальність даних не гарантуються.

## Подяка
- https://github.com/J-A-A-M/ukraine_alarm_map

## License
Files included in this repository is avaliable under terms of [MIT license](LICENSE). external dependency, such as [requests](https://github.com/psf/requests) is avaliable under their own licenses.

[![Stand With Ukraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/banner-direct-single.svg)](https://stand-with-ukraine.pp.ua)
