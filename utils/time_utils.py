import datetime

def get_bot_uptime(start_time):
    """Calculate the bot's uptime"""
    current_time = datetime.datetime.utcnow()
    delta = current_time - start_time
    
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    parts = []
    if days > 0:
        parts.append(f"{days} days")
    if hours > 0:
        parts.append(f"{hours} hours")
    if minutes > 0:
        parts.append(f"{minutes} minutes")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} seconds")
    
    return ", ".join(parts)
