import datetime
import sys

def get_date():
    today = datetime.date.today()
    spoken_date = today.strftime("Today is %B %d, %Y")
    return spoken_date

if __name__ == "__main__":
    today = get_date()
    print(today)

    sys.path.append('.')