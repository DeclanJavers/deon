import sys
import os
# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from functions.get_website_txt import extract_webpage_text
from functions.get_gemini import generic_gemini


def get_news_briefing():

    text = extract_webpage_text("https://news.google.com/")

    gemini_prompt = f"Summarize the news: {text}"

    response = generic_gemini(gemini_prompt)

    print(response)

    return ("Here is the news. This is already summerized so please pass it back to the user using this exact text: \n" + response)

