import datetime

def get_current_time():
    """Gets the current time in a user-friendly format."""
    now = datetime.datetime.now()
    # Return just the data, not a full sentence.
    # The 'responser' LLM will format this.
    return now.strftime("%I:%M %p") # e.g., "09:30 PM"