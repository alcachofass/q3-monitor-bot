import os
import discord
import socket
from pyq3serverlist import Server
from pyq3serverlist.exceptions import PyQ3SLError, PyQ3SLTimeoutError
from dotenv import load_dotenv
from discord.ext import tasks

load_dotenv()

servername        = str(os.environ.get('SERVER_HOSTNAME'))
port              = int(os.environ.get('PORT'))
sec               = int(os.environ.get('SECONDS'))
token             = str(os.environ.get('AUTH_TOKEN'))
channel           = int(os.environ.get('CHANNEL_ID'))

old_count     = int()
new_count     = int()
server_status = str()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def check():
    global old_count
    global new_count
    global server_status

    try:
        server_status = query_quake3_server(servername,port)
    except:
        print("Error querying quake 3 server.")
        return(False)
    
    j = 0
    for i in server_status["players"]:
        ping  = str(i['ping'])
        if ping != '0':
            j+=1

    new_count = j

    if old_count != new_count:
        old_count = new_count
        return(True)
    return(False)

def create_message():
    global server_status
    this_message = ""
    ip = socket.gethostbyname(servername)
    this_message = this_message + "**Server: **" + "__" + servername + " | " + ip + ":" + str(port) + "__" + "\n"

    map = str(server_status['mapname'])
    gameType = str(server_status['g_gametype'])  

    this_message = this_message + "**Map: **" + map +"\n"
    this_message = this_message + "**Game Type: **" + gameType + "\n"
    this_message = this_message + "> **Player**" + " | " + "**Frags**" + "\n"

    for i in server_status["players"]:
        name  = str(i['name'])
        frags = str(i['frags'])
        ping  = str(i['ping'])
        if ping != '0':
            this_message = this_message + "> " + name + " | " + "" + frags + "\n"
    return(this_message)

def query_quake3_server(server, port):

    server = Server(server, port)
    info = server.get_status()
    return(info)

@tasks.loop(seconds=sec)
async def start_checks():
    global channel
    if check() is True:
        message = create_message()
        await channel.send(message)

@client.event
async def on_ready():
    global channel
    global old_count

    old_count = 0

    channel = client.get_channel(channel)
    start_checks.start()

client.run(token)

