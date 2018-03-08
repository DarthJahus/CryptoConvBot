# CryptoConvBot ver. 2

## Purpose

This bot is a currency converter for Telegram.

## Usage

* Get help: Send `/help` command in private with the bot to receive a list of commands and their usage.
* Convert a currency to another: Send `/convert [amount] <coin1> <coin2>` in a group where the bot is present, or in private to the bot to convert `<coin1>` to `<coin2>`. The `[amount]` is optional. Use period decimal separator (`.`).
* Retreive a snapshot of a currency: `/snap <coin>` command returns a snapshot of `<coin>`, with current *price*, *volume*, *marketcap* and *24 hours change*.

This bot has a greetings feature; that allows him to say "hello" and "bye" to people who join or leave a group. Group administrators can disable or enable this feature by sending `/greetings on` or `/greetings off` in their group.

Send `/about` in private to learn more about us and our other products.

## Installation

### Requirements

* `requests>=2.18.4`
* `python-telegram-bot==9.0.0`
* `emoji>=0.4.5`

### Configuration

`config.json` file contains a dict for tokens. Change `bot` token to your own bot's secret key. You can create a bot and get its token from [@BotFather](https://t.me/BotFather).

Change `bot_name` in `config.json` file to your bot's username (without @).

Run `CryptoConvBot.py` file.

## Licence

<img src="https://mirrors.creativecommons.org/presskit/buttons/88x31/png/by.png" alt="CC-BY-SA"/>
