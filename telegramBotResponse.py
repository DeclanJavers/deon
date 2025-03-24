from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import concurrent.futures
from your_command_module import process_command  # Import the updated process_command function
from functions.send_telegram_message import send_telegram_message

# Constants for the bot token and bot username
TOKEN: Final = 'enter_your_bot_token_here'
BOT_USERNAME = 'enter_your_bot_username_here'

# Create a thread pool executor to handle command execution
executor = concurrent.futures.ThreadPoolExecutor()

# Handle messages received by the bot (this is where text commands are processed)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # text is what the user sent
    text: str = update.message.text
    print(f"User ({update.message.chat.id}) sent: \"{text}\"")
    
    try:
        with open('text_files/latest_command.txt', 'w', encoding='utf-8') as f:
            f.write('')  # Clears the file by writing an empty string
            f.write(text)
            print("finished adding latest command to file")
    except UnicodeEncodeError as e:
        print(f"Encoding error: {e}")


    # Process the command asynchronously and pass the `update` and `context` for response
    response = await process_command(text, executor)
    
    send_telegram_message(response)



# The entry point for the bot
if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Register the message handler
    app.add_handler(MessageHandler(filters.TEXT, handle_message))


    # Start polling for updates
    print('Polling...')
    app.run_polling(poll_interval=3)
