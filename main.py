import discord
import asyncio
import time
import subprocess
from mcipc.rcon.je import Biome, Client     
import shutil    
import os, sys
from datetime import datetime


now = datetime.now()

server = os.getcwd()
print(server)

rconpwd = 'retcon'
rconport = 25575

backups = os.path.join(server, "World backups")
world = os.path.join(server, "world")
print(world)

client = discord.Client()


@client.event
async def on_ready():
    print("Bot online")
    await start()
    await timer()

async def start():
    print ("starting minecraft server")
    subprocess.Popen([os.path.join(server, "run.bat")], stdin=None, stdout=None, stderr=None, close_fds=True)
    channel = client.get_channel(809087383067951144)
    await channel.send("<@&809086423181164564> SERVER IS UP")
    time.sleep(10)
    


async def backup():
    print('Backing up')
    await stop()
    subprocess.call([os.path.join(server, "backup.bat")])
    print("Backup Complete")
    
    


async def stop():
    print("stopping")
    with Client('127.0.0.1', rconport, passwd=rconpwd) as client:
        client.say('stopping server in 60 seconds')
        time.sleep(30)
        client.say('stopping server in 30 seconds')
        time.sleep(15)
        client.say('stopping server in 15 seconds')
        time.sleep(5)
        client.say('stopping server in 10 seconds')
        time.sleep(5)
        client.say('stopping server in 5 seconds')
        time.sleep(5)
        client.stop()
        await serverdown()
            
@client.event
async def serverdown():
    print("pining with server down")
    channel = client.get_channel(809087383067951144)
    await channel.send("<@&809086423181164564> THE SERVER IS DOWN")

async def timer():
    time.sleep(30) #30
    while True:
        time.sleep(900) #900
        
        rawTime = time.localtime(time.time())
        ints = [rawTime.tm_hour,rawTime.tm_min,rawTime.tm_sec]
        string_time = [str(int) for int in ints]
        preIntTime = "".join(string_time)
        current_time = int(preIntTime)
        
        #current_time = int(now.strftime("%H%M%S"))
        print(current_time)
        if 84400>current_time>81500:
            print("Restarting Server")
            await backup()
            time.sleep(10)
            await start()
            time.sleep(10)
        
    


'''
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!ping'):
        channel = client.get_channel(809087383067951144)
        await channel.send("<@&809086423181164564> BRO THE SERVER JUST DIED!!11!1!11!1")
'''

@client.event
async def serverdied():
    channel = client.get_channel(809087383067951144)
    await channel.send("<@&809086423181164564> THE SERVER JUST DIED")
    


client.run('ODA5MDY4NjgyNjQ1OTk1NTMw.YCPt7Q.wkfGBpXnxa5U-LRJinRky3R46VA')

