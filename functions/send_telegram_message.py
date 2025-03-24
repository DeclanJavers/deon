import requests

# Constants for the bot token and bot username
TOKEN = 'enter_your_bot_token_here'
BOT_USERNAME = 'enter_your_bot_username_here'

def send_telegram_message(message):
    """
    Sends a message to a Telegram user via a bot.
    
    Parameters:
    bot_token (str): The API token of the Telegram bot.
    chat_id (str or int): The chat ID of the recipient (could be a user or group ID).
    message (str): The message to send.
    
    Returns:
    dict: The response from Telegram API.
    """

    # hard coded this stuff cause I'm lazy
    chat_id = 'enter_your_chat_id_here'

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    
    response = requests.post(url, json=payload)
    
    return response.json()  # Returns the JSON response from Telegram API
