import re
import pandas as pd

def preprocess(data):
    pattern = r"\[(\d{2}/\d{2}/\d{2}), (\d{1,2}:\d{2}:\d{2})\s[AP]M\] (?:(.*?): )?(.*)"
    
     
    # Get all lines
    messages_raw = re.findall(pattern, data)
    
    # Lists to store parsed data
    dates = []
    users = []
    messages = []
    
    for date, time, user, message in messages_raw:
        dates.append(f"{date} {time}")
        
        if user == "":
            users.append("group_notification")
        else:
            users.append(user)
            
        messages.append(message)
    
    df = pd.DataFrame({
        "date": pd.to_datetime(dates, format="%d/%m/%y %H:%M:%S"),
        "user": users,
        "message": messages
    })
    df["only_date"] = df["date"].dt.date
    df["year"] = df["date"].dt.year
    df["month_num"] = df["date"].dt.month
    df["month"] = df["date"].dt.month_name()
    df["day"] = df["date"].dt.day
    df["day_name"] = df["date"].dt.day_name()
    df["hour"] = df["date"].dt.hour
    df["minute"] = df["date"].dt.minute
    
    period = []
    
    for hour in df["hour"]:
        start_hour_12 = (hour % 12) or 12
        end_hour = (hour + 1) % 24
        end_hour_12 = (end_hour % 12) or 12
        
        start_meridiem = "AM" if hour < 12 else "PM"
        end_meridiem = "AM" if end_hour < 12 else "PM"
        
        period.append(f"{start_hour_12} {start_meridiem} - {end_hour_12} {end_meridiem}")
        
    df["period"] = period
    return df