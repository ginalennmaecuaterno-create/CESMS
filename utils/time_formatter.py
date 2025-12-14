from datetime import datetime, timedelta, timezone

# Philippine Time is UTC+8
PHILIPPINE_TZ = timezone(timedelta(hours=8))

def format_time_12hr(time_str):
    """
    Convert 24-hour time format to 12-hour format with AM/PM
    Input: "14:30:00" or "14:30"
    Output: "2:30 PM"
    """
    if not time_str:
        return ""
    
    try:
        # Handle both HH:MM:SS and HH:MM formats
        if len(time_str.split(':')) == 3:
            time_obj = datetime.strptime(time_str, "%H:%M:%S")
        else:
            time_obj = datetime.strptime(time_str, "%H:%M")
        
        # Format to 12-hour with AM/PM
        return time_obj.strftime("%I:%M %p")
    except:
        return time_str

def format_date_readable(date_str):
    """
    Convert date to more readable format
    Input: "2025-12-08"
    Output: "December 8, 2025"
    """
    if not date_str:
        return ""
    
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%B %d, %Y")
    except:
        return date_str

def format_datetime_readable(datetime_str):
    """
    Convert datetime to readable format in Philippine Time (UTC+8)
    Input: "2025-12-08T14:30:00" (UTC)
    Output: "December 8, 2025 at 10:30 PM" (Philippine Time)
    """
    if not datetime_str:
        return ""
    
    try:
        # Handle different datetime formats
        if 'T' in datetime_str:
            # Parse ISO format
            dt_obj = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
        elif '+' in datetime_str or datetime_str.endswith('00'):
            # Already has timezone info
            dt_obj = datetime.fromisoformat(datetime_str)
        else:
            # Assume UTC if no timezone
            dt_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            dt_obj = dt_obj.replace(tzinfo=timezone.utc)
        
        # Convert to Philippine Time (UTC+8)
        ph_time = dt_obj.astimezone(PHILIPPINE_TZ)
        
        return ph_time.strftime("%B %d, %Y at %I:%M %p")
    except Exception as e:
        print(f"Error formatting datetime: {e}, input: {datetime_str}")
        return datetime_str
