import discord
import asyncio
import time
import subprocess
from mcipc.rcon.je import Biome, Client     
import shutil    
import os, sys
from datetime import datetime
import configparser


#index of varibles
config = configparser.ConfigParser()

now = datetime.now()

server = os.getcwd()
print(server)

backups = os.path.join(server, "World backups")
world = os.path.join(server, "world")
print(world)

client = discord.Client()
#creating the config

if os.path.isfile('mcServerRestartConfig.ini') != True:
    print ("No config found, creating one.")
    config['DISCORDSETTINGS'] = {'DiscordChannelId': '000000000000000001',
                                 'RoleToPing': '<@&000000000000000001>'}

    config['RCONSETTINGS'] = {'RconPassword': 'aGoodPassword',
                              'RconServerPort': '25575'}

    with open('mcServerRestartConfig.ini', 'w') as configfile:
        config.write(configfile)
    print("default settings loaded, please set config correctly, exiting in five seconds")
    time.sleep(5)
    exit()

else:
    print ("Config found!")
    config.read("mcServerRestartConfig.ini")
    discordSettings = config['DISCORDSETTINGS']
    rconSettings = config['RCONSETTINGS']

    if discordSettings["DiscordChannelId"] == '000000000000000001' or discordSettings["RoleToPing"] == '<@&000000000000000001>':
        print('You need to set either the Channel id or the role to ping id! use \#channel or \@role in discord chat to get the ids! exiting in ten seconds')
        time.sleep(10)
        exit()

    if rconSettings["RconPassword"] == 'aGoodPassword':
        print('You have not set the rcon password to a different one than default. This may cause problems!')
        time.sleep(1)

    if rconSettings["RconServerPort"] == '25575':
        print('You are using the default Rcon port')



channelid = int(discordSettings["DiscordChannelId"])#'809087383067951144'
pingid = discordSettings["RoleToPing"]#'<@&809086423181164564>'

rconpwd = rconSettings["RconPassword"] #'retcon'
rconport = int(rconSettings["RconServerPort"]) #25575

print("Channel Id is {}".format(discordSettings["DiscordChannelId"]))
print("Role to ping is {}".format(discordSettings["RoleToPing"]))
print("Rcon password is {}".format(rconSettings["RconPassword"]))
print("Rcon server port is {}".format(rconSettings["RconServerPort"]))
time.sleep(5)

#error check to see if all components are there
if os.path.isfile('run.bat') != True:
    print('run.bat not found! this will cause the server to not run! exiting in 5 seconds')
    time.sleep(5)
    exit()
if os.path.isfile('backup.bat') != True:
    print('backup.bat not found, this is very likely to cause problems cause problems, exit?')
    if input("Are you sure? (y/n): ").lower().strip()[:1] == "y":
        exit()
    

#the main program
@client.event
async def on_ready():
    print("Bot online")
    await start()
    await timer()

# starts the mc server, requires run.bat
async def start():
    print ("starting minecraft server")
    subprocess.Popen([os.path.join(server, "run.bat")], stdin=None, stdout=None, stderr=None, close_fds=True)
    print("make sure the .jar file of your server is "server.jar", else the server will not start!")
    channel = client.get_channel(channelid)
    await channel.send(pingid + " SERVER IS UP")
    time.sleep(10)
    
# say the server is down on the discord channel
async def serverdown():
    print("pining with server down")
    channel = client.get_channel(channelid)
    await channel.send(pingid + " THE SERVER IS DOWN")

#backup the mc world
async def backup():
    print('Backing up')
    await stop()
    subprocess.call([os.path.join(server, "backup.bat")])
    print("Backup Complete")
    
    

#safely stop the server, requires 60 seconds

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
            

# the timer to check when to run the backup command
async def timer():
    time.sleep(30) #waits 30 seconds for the server to start
    while True:
        time.sleep(1740) #waits 1,740 (29 minutes) seconds to check if the time is right
        
        rawTime = time.localtime(time.time())
        ints = [rawTime.tm_hour,rawTime.tm_min,rawTime.tm_sec]
        string_time = [str(int) for int in ints]
        preIntTime = "".join(string_time)
        current_time = int(preIntTime)
        
        #current_time = int(now.strftime("%H%M%S"))
        print(current_time)
        if 84500>current_time>81500: # checks to see if the time is between 8:15 and 8:45, i might see if i could do it more persicly with only minutes and hours + TODO make this varible
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
# wip crash alerter, nothing calls it yet
@client.event
async def serverdied():
    channel = client.get_channel(channelid)
    await channel.send(pingid + " THE SERVER JUST DIED")
    


client.run('ODA5MDY4NjgyNjQ1OTk1NTMw.YCPt7Q.wkfGBpXnxa5U-LRJinRky3R46VA')

