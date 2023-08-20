import os
import discord
import socket
from pyq3serverlist import Server
from pyq3serverlist.exceptions import PyQ3SLError, PyQ3SLTimeoutError
from dotenv import load_dotenv
from discord.ext import tasks
import logging
from cysystemd import journal

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.addHandler(journal.JournaldLogHandler())

load_dotenv()

hostname        = str(os.environ.get('HOSTNAME'))
port            = int(os.environ.get('PORT'))
sec             = int(os.environ.get('SECONDS'))
token           = str(os.environ.get('AUTH_TOKEN'))
channel         = int(os.environ.get('CHANNEL_ID'))

old_count     = int()
new_count     = int()
server_status = str()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def check():
    logger.info("DEBUG: Checking player count.")

    global old_count
    global new_count
    global server_status

    server_status = query_quake3_server(hostname,port)
    
    j = 0
    for i in server_status["players"]:
        ping  = str(i['ping'])
        if ping != '0':
            j+=1

    new_count = j

    logger.info("DEBUG: Old count is " + str(old_count))
    logger.info("DEBUG: New count is " + str(new_count))

    if old_count != new_count:
        logger.info("DEBUG: Player count is different. Post server details.")
        old_count = new_count
        return(True)
    return(False)

def create_message():
    logger.info("DEBUG: Creating the message.")

    global server_status
    this_message = ""
    ip = socket.gethostbyname(hostname)
    this_message = this_message + "**Server: **" + "__" + hostname + " | " + ip + ":" + str(port) + "__" + "\n"

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
    logger.info("DEBUG: Querying server.")

    server = Server(server, port)

    try:
        info = server.get_status()
        return(info)
    except (PyQ3SLError, PyQ3SLTimeoutError) as e:
        logger.info(e)

@tasks.loop(seconds=sec)
async def start_checks():
    global channel
    logger.info("DEBUG: Running the loop.")
    if check() is True:
        logger.info("DEBUG: Sending the message to channel.")
        try:
            logger.info("DEBUG: Trying to create the message.")
            message = create_message()
            logger.info("DEBUG: Message created, sending to channel.")
            await channel.send(message)
        except:
            logger.info("DEBUG: Sending the message FAILED.")



@client.event
async def on_ready():
    global channel
    global old_count

    old_count = 0

    logger.info("bot:user ready == {0.user}".format(client))
    channel = client.get_channel(channel)
    logger.info("bot:user is in channel: " + str(channel))
    start_checks.start()

client.run(token)

