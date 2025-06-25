from datetime import datetime
import time


def convert_msutc_datetime(msutc: int):
    """
    Converts Milliseconds since UTC to various datetime formats.

    Args:
        msutc (int): Milliseconds since UTC

    Returns:
        tuple:
             - date (datetime.date): datetime object e.g., datetime.date(2025, 6, 18)
             - date_str (str): date string, e.g., '2025-06-18'
             - hour (int): hour int, e.g. 18
             - time_str (str): time string, e.g., '2025-06-18 18:50:43'
    """
    dt = datetime.utcfromtimestamp(msutc/1000)

    date = dt.date()
    date_str = date.strftime('%Y-%m-%d')
    hour = dt.hour

    time_str = dt.strftime('%Y-%m-%d %H:%M:%S')
    return date, date_str, hour, time_str


def time_wait(seconds: int):
    """
    Wait for a specified number of seconds while printing progress to the console.

    Args:
        seconds (int): The number of seconds to wait.

    Returns:
        None
    """
    print("\n")
    for i in range(1, seconds + 1):
        print(f"\rRabbit is waiting {i}/{seconds}s.", end="")
        time.sleep(1)
    print("\n")
