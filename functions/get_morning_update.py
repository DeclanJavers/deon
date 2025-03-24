# Add the parent directory to the system path
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from functions.get_date import get_date
from functions.get_calendar import get_calendar
from functions.get_weather import get_weather
from functions.get_news_briefing import get_news_briefing

def get_morning_update():

    date = get_date()
    calendar = get_calendar()
    weather = get_weather()
    news = get_news_briefing()

    morning_update = f"Here is your daily update:\n\n{date}\n\n{calendar}\n\n{weather}\n\n{news}"
    return morning_update
