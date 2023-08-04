import os
import discord
import socket
from pyq3serverlist import Server
from pyq3serverlist.exceptions import PyQ3SLError, PyQ3SLTimeoutError
from dotenv import load_dotenv
from discord.ext import tasks

load_dotenv()

hostname        = str(os.environ.get('HOSTNAME'))
port            = int(os.environ.get('PORT'))
sec             = int(os.environ.get('SECONDS'))
token           = str(os.environ.get('AUTH_TOKEN'))
channel         = int(os.environ.get('CHANNEL_ID'))

old_count = int()
new_count = int()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def check():    
    global old_count
    global new_count 

    serverStatus = query_quake3_server(hostname,port)            
    new_count = len(serverStatus["players"])

    if old_count != new_count:
        print("Player count is different. Post server details.")
        old_count = new_count
        return(True)
    return(False)

def create_message():
    this_message = ""
    ip = socket.gethostbyname(hostname)
    this_message = this_message + "__" + hostname + " | " + ip + ":" + str(port) + "__" + "\n"
    this_message = this_message + "> **Player**" + " | " + "**Frags**" + "\n"
    serverStatus = query_quake3_server(hostname,port)               
    for i in serverStatus["players"]:
        name  = str(i['name'])
        frags = str(i['frags'])
        ping  = str(i['ping'])
        if ping != '0':
            this_message = this_message + "> " + name + " | " + "" + frags + "\n"
    return(this_message)

def query_quake3_server(server, port):
    server = Server(server, port)
    try:
        info = server.get_status()
        return(info)
    except (PyQ3SLError, PyQ3SLTimeoutError) as e:
        print(e)

@tasks.loop(seconds=sec)
async def start_checks():
    if check() is True:
        print(create_message())
        await channel.send(create_message())


@client.event
async def on_ready():
    global channel
    print("bot:user ready == {0.user}".format(client))
    channel = client.get_channel(channel)
    print("bot:user is in channel: " + str(channel))
    start_checks.start()

client.run(token)

