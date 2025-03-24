from __future__ import print_function
import datetime
import os
import re
import sys
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from generic_gemini import generic_gemini  # Assuming this module is available

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def format_event_time(start, end=None):
    """Format event start and end times for conversational output."""
    try:
        if 'T' in start:  # DateTime format
            event_start_time = datetime.datetime.fromisoformat(start.replace('Z', '+00:00'))
            formatted_start = event_start_time.strftime('%A at %I:%M %p')  # e.g., "Saturday at 12:00 PM"
            if end:  # Include end time if provided
                event_end_time = datetime.datetime.fromisoformat(end.replace('Z', '+00:00'))
                formatted_end = event_end_time.strftime('%I:%M %p')  # e.g., "1:00 PM"
                return f"{formatted_start} - {formatted_end}"
            return formatted_start
        else:  # Date-only format (all-day event)
            event_date = datetime.datetime.strptime(start, '%Y-%m-%d')
            return event_date.strftime('%A (All day)')  # e.g., "Sunday (All day)"
    except ValueError:
        return "Unknown time"

def days_until_next(target_day):
    """Calculate the number of days from today until the next target day (e.g., Friday)."""
    days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    today = datetime.datetime.today().weekday()  # Monday is 0, Sunday is 6
    target_day = target_day.lower()

    if target_day in days_of_week:
        target_day_index = days_of_week.index(target_day)
        days_ahead = (target_day_index - today + 7) % 7
        return days_ahead if days_ahead != 0 else 7  # Return 7 if today is the target day
    return None

def extract_days_from_command(userCommand):
    """Extracts the number of days or day of the week from the user's command."""
    # Check for day-of-week phrases like "till", "through", "until"
    match = re.search(r'(until|till|through|to) (\w+)', userCommand.lower())
    if match:
        day_of_week = match.group(2)  # Capture the specified day
        days = days_until_next(day_of_week)  # Get the days until that day
        if days is not None:
            return days
    
    # Check for number of days (e.g., "next 5 days")
    match_days = re.search(r'next (\d+) days', userCommand.lower())
    if match_days:
        return int(match_days.group(1))

    # If nothing is found, return None
    return None

def get_calendar():
    """Fetch events from all calendars in the user's Google Calendar based on their command."""
    # Get the latest command from the text file
    with open('text_files/latest_command.txt', 'r') as file:
        userCommand = file.read().strip()

    # Append the current date for better context in Gemini
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    gemini_prompt = f"The current date is {current_date}. The user wants to know their upcoming events. Based on their question, please return just the number of days they want to view, defaulting to 7 if no clear answer is presented.\n\nUser's command: {userCommand}"

    # Attempt to extract the number of days from the user's command
    days = extract_days_from_command(userCommand)

    if days is None:
        # Fallback to querying Gemini API if no days were found in the user command
        gemini_response = generic_gemini(gemini_prompt)

        # Try to parse the Gemini response for a number of days
        try:
            days = int(gemini_response) if gemini_response.isdigit() else 7
        except ValueError:
            days = 7  # Default to 7 days if the Gemini response is unclear

    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'functions/client_secret_855943609045-b24139d6ifkbpa1od67vfacmb3rvchhk.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    calendar_list = service.calendarList().list().execute()
    calendars = calendar_list.get('items', [])

    if not calendars:
        return 'No calendars found.'

    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    time_max = (datetime.datetime.utcnow() + datetime.timedelta(days=days)).isoformat() + 'Z'

    all_events = []
    for calendar in calendars:
        calendar_id = calendar['id']
        calendar_name = calendar.get('summary', 'Unnamed Calendar')

        if calendar_id == 'maureenjavers@gmail.com':
            continue

        events_result = service.events().list(calendarId=calendar_id, timeMin=now, timeMax=time_max,
                                              maxResults=100, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))  # Fetch the end time
            all_events.append({
                'summary': event['summary'],
                'start': start,
                'end': end,
                'calendar_name': calendar_name
            })

    if not all_events:
        return 'No upcoming events found.'

    all_events_sorted = sorted(all_events, key=lambda x: x['start'])

    events_str = []
    for event in all_events_sorted:
        formatted_time = format_event_time(event['start'], event['end'])
        
        # Get event date from the start time
        event_date = datetime.datetime.fromisoformat(event['start'].replace('Z', '+00:00')).strftime('%Y-%m-%d')
        
        events_str.append(f"- {event_date}, {formatted_time}: {event['summary']} from {event['calendar_name']}")

    returnText = (
        f'Here are the user\'s events for the next {days} days, excluding maureenjavers@gmail.com. Please list their events in a bulleted list format:\n'
        + '\n'.join(events_str)
    )
    return returnText


if __name__ == "__main__":
    # Run the function and print the results for testing purposes
    result = get_calendar()
    print(result)
