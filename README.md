# CryptoConvBot ver. 3

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

<hr/>

### Configuration

`config.json` file contains a dict for tokens. Change `bot` token to your own bot's secret key. You can create a bot and get its token from [@BotFather](https://t.me/BotFather).

Change `bot_name` in `config.json` file to your bot's username (without @).

Unless you are planning to use WebHook, make sure the `enable` property under `webhook` is set to `false`.

Run `CryptoConvBot.py` file.

<hr/>

### WebHook configuration

This bot can get updates from Telegram in two ways:

* **LongPoll:** The bot checks every now and then for updates and reacts whenever there is one.
* **WebHook:** The bot listens for HTTPS POST requests from Telegram and reacts when asked to.

WebHook asks Telegram to communicate with your server. The requests are done through HTTPS (Telegram doesn't support HTTP).

#####Set up a domain name

Your server needs to be reachable at the same address. If you have no fixed IP and domain name, you can set up a Dyn-DNS for free.

####Generate an SSL certificate

If you have no certificate for your domain name, you can still generate your own with OpenSSL. It is enough for Telegram.

    openssl req -new -x509 -keyout server.key -out server.pem -days 365 -nodes

The only required field is the `CommonName`. It has to be equal to your domain name (ex. `convbot.ddns.net`).<br/>
Once generated, move the `server.key` and `server.pem` files to your bot's directory.

####**Enable WebHook in configuration file**

In `config.json`, under the `webhook` section:

* Set `url` to your server URL (ex. `"https://convbot.ddns.net"`) and `port` to the port through which the communication will be done (ex. `433`). You may need to open that port on your server.
* Set `enable` to `true`. The bot will now run WebHook.

For security reasons, your bot's entry point is set to be `/<token>` (ex. `https://convbot.ddns.net/445478:AAG1mv-1jI18`). 

<hr/>

## Licence

<a href="https://creativecommons.org/licenses/by-sa/3.0/"><img src="https://mirrors.creativecommons.org/presskit/buttons/88x31/png/by.png" alt="CC-BY-SA"/></a>
