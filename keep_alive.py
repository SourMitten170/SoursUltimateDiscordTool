from flask import Flask
from threading import Thread
import logging
import os

app = Flask('')
logger = logging.getLogger('discord_bot')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    """Run the server with proper host configuration for Raspberry Pi"""
    try:
        # Get the port from environment variable or use default
        port = int(os.getenv('PORT', 8080))
        # Bind to all network interfaces
        app.run(host='0.0.0.0', port=port)
    except Exception as e:
        logger.error(f"Error in keep-alive server: {e}")
        raise

def keep_alive():
    """Creates and starts a web server that keeps the bot running"""
    try:
        t = Thread(target=run, daemon=True)  # Make thread daemon so it exits when main program exits
        t.start()
        logger.info("Keep-alive server started successfully")
    except Exception as e:
        logger.error(f"Error starting keep-alive server: {str(e)}")