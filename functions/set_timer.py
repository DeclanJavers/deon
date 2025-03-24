import sys
import os
import asyncio
import re

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from functions.send_telegram_message import send_telegram_message

# Function to read the latest command and extract the duration in seconds
def get_duration_from_command(command_text):
    patterns = [
        (r'(\d+)\sseconds?', 1),
        (r'(\d+)\sminutes?', 60),
        (r'(\d+)\s*hours?', 3600)
    ]
    total_seconds = 0
    for pattern, multiplier in patterns:
        match = re.search(pattern, command_text, re.IGNORECASE)
        if match:
            total_seconds += int(match.group(1)) * multiplier
    return total_seconds if total_seconds > 0 else None

# Async function to set a timer
async def set_timer():
    duration = get_duration_from_command("Start timer for 10 seconds") 
    if duration is not None:
        # Send an immediate response to the user
        # send_telegram_message(f"Timer set for {duration} seconds.")
        print(f"Timer set for {duration} seconds.")
        # Start the countdown as a background task
        asyncio.create_task(timer_countdown(duration))
    else:
        send_telegram_message("Could not understand the timer duration.")

# Async function that runs the countdown and alerts the user when time is up
async def timer_countdown(duration: int):
    print(f"Timer started for {duration} seconds.")
    await asyncio.sleep(duration)  # Await asyncio.sleep
    print("Timer ended.")
    send_telegram_message("Timer has ended.")  # Ensure send_telegram_message is awaited if async

if __name__ == "__main__":
    # Run the coroutine in the event loop
    asyncio.run(set_timer())
