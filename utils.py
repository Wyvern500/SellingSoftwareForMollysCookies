from datetime import datetime


def get_formatted_current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")