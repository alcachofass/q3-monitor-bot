# q3-monitor-bot
A basic Discord bot to monitor a Quake 3 server.

## Requirements
    py -3 -m pip install -U discord.py
    
    py -3 -m pip install -U python-dotenv
    
    py -3 -m pip install -U pyq3serverlist

    py -3 -m pip install -U cysystemd

## .env File
- AUTH_TOKEN     - Your Discord OAuth Token
- HOSTNAME       - FQDN of game server
- PORT           - Port number
- SECONDS        - Amount of time wait between task execution
- CHANNEL_ID     - Discord channel ID