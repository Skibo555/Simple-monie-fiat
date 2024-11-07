from datetime import datetime


# This function generates the last number of a pan entered by customers
def get_last_four_num(pan):
    last_four = pan[-4]
    return last_four


# This function generates the time the card was added in a format that Visa Alias API wants it.
def get_current_time():
    # Get current date and time
    current_datetime = datetime.now()
    # Format it to Visa Alias pattern
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_datetime


time = get_current_time()
