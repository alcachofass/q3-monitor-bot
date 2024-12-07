# q3-monitor-bot
A basic Discord bot to monitor a Quake 3 server.

## Requirements
    pip install -U discord.py
    
    pip install -U python-dotenv
    
    pip install -U pyq3serverlist

## .env File
- AUTH_TOKEN            - Your Discord OAuth Token
- SERVER_HOSTNAME       - FQDN of game server
- PORT                  - Port number
- SECONDS               - Amount of time wait between task execution
- CHANNEL_ID            - Discord channel ID
