import datetime

def get_time():
    now = datetime.datetime.now()
    spoken_time = now.strftime("The time is %H:%M:%S")
    return spoken_time

if __name__ == "__main__":
    current_time = get_time()
    print(current_time)