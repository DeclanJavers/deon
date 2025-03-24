import csv
import os
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import concurrent.futures
from datetime import datetime
from your_command_module import process_command

# Constants for the bot token and bot username
TOKEN: Final = 'YOUR_TELEGRAM_BOT_TOKEN'
BOT_USERNAME = '@Deon41_bot'
CSV_FILE = 'bot_data.csv'

# Create a thread pool executor to handle command execution
executor = concurrent.futures.ThreadPoolExecutor()

# Ensure the CSV file exists and has headers
def initialize_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['user_id', 'timestamp', 'command', 'response', 'timer', 'event_type'])

# Append data to the CSV file
def append_to_csv(user_id, command, response, timer=None, event_type='command'):
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), command, response, timer, event_type])

# The /start command function for the bot
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = f"Hello! I am {BOT_USERNAME}. How can I help you today?"
    await update.message.reply_text(response)
    append_to_csv(update.message.chat.id, '/start', response)

# The /help command function for the bot
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = 'I am a bot! Please type something so I can respond!'
    await update.message.reply_text(response)
    append_to_csv(update.message.chat.id, '/help', response)

# Handle messages received by the bot (this is where text commands are processed)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text
    print(f"User ({update.message.chat.id}) sent: \"{text}\"")

    # Process the command asynchronously and get the response
    response = await process_command(update, context, text, executor, testing_mode=True)
    
    # Log the command and response to the CSV
    append_to_csv(update.message.chat.id, text, response)

# Handle errors that occur while processing
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

# The entry point for the bot
if __name__ == '__main__':
    print('Starting bot...')

    # Initialize the CSV file
    initialize_csv()

    # Start the bot
    app = Application.builder().token(TOKEN).build()

    # Register the bot commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))

    # Register the message handler
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Register the error handler
    app.add_error_handler(error)

    # Start polling for updates
    print('Polling...')
    app.run_polling(poll_interval=3)
