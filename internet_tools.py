""" Functions to be used by a Python 3 interpreter.
    Developed by Rodrigo Rivero.
    https://github.com/rodrigo1392"""

import requests


def telegram_bot_send_text(bot_token, bot_chat_id, bot_message):
    """
    Sends telegram message through bot.
    Inputs: bot_token. Token of telegram bot.
            bot_chat_id. ID from chat.
            bot_message. String to be sent.
    Output: JSON variable with details of the message.
    """
    send_text = 'https://api.telegram.org/bot' + bot_token +\
                '/sendMessage?chat_id=' + bot_chat_id + \
                '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()
