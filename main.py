import discord
import asyncio
import time
import subprocess
from mcipc.rcon.je import Biome, Client     
import shutil    
import os
import sys
from datetime import datetime
import configparser
import pathlib


#index of varibles of things that don't need oredered activation
config = configparser.ConfigParser()
now = datetime.now()
client = discord.Client()

#creating the config

if os.path.isfile('mcServerRestartConfig.ini') != True:
    print ("No config found, creating one.")
    
    config['SERVER'] = {'ServerDir': "",
                        'BackupPath': "",
                        'ServerJar': "server.jar",
                        'WorldFolderName': "world",
                        'ServerStartFile': "run.bat"}
    
    config['DISCORDSETTINGS'] = {'DiscordChannelId': '000000000000000001',
                                 'RoleToPing': '<@&000000000000000001>',
                                 'TOKEN': ""}

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

    serverSettings = config['SERVER']
    discordSettings = config['DISCORDSETTINGS']
    rconSettings = config['RCONSETTINGS']

    server = serverSettings["ServerDir"]
    backups = serverSettings["BackupPath"]
    world = os.path.join(server, serverSettings["WorldFolderName"])
    
    #making sure things are set up right
    if discordSettings["TOKEN"] == "":
        print('You need to set the bot token! exiting in 5 seconds')
        time.sleep(5)
        exit()
        
    if serverSettings["ServerDir"] == "":
        print('You need to set the config for server path! exiting in 5 seconds')
        time.sleep(5)
        exit()
        
    if serverSettings["BackupPath"] == "":
        print('You need to set the config for backup path! exiting in 5 seconds')
        time.sleep(5)
        exit()
        
    if os.path.isfile(os.path.join(server, serverSettings["ServerJar"])) != True:
        print(os.path.join(server, serverSettings["ServerJar"]))
        print('Cannot find the file specified, please check again! exiting in 5 seconds')
        time.sleep(5)
        exit()

    if os.path.isfile(os.path.join(world, "\\level.dat")):
        print(world)
        print('Cannot find the folder specified, please check again! exiting in 5 seconds')
        worldThere = ask_user()
        if worldThere:
            exit()
        

    if discordSettings["DiscordChannelId"] == '000000000000000001' or discordSettings["RoleToPing"] == '<@&000000000000000001>':
        print('You need to set either the Channel id or the role to ping id! use \#channel or \@role in discord chat to get the ids! exiting in ten seconds')
        time.sleep(10)
        exit()

    if rconSettings["RconPassword"] == 'aGoodPassword':
        print('You have not set the rcon password to a different one than default.')
        time.sleep(1)

    if rconSettings["RconServerPort"] == '25575':
        print('You are using the default Rcon port')




channelid = int(discordSettings["DiscordChannelId"])
pingid = discordSettings["RoleToPing"]

rconpwd = rconSettings["RconPassword"]
rconport = int(rconSettings["RconServerPort"])

print("Server directory is {}".format(serverSettings["ServerDir"]))
print("Backup directory is {}".format(serverSettings["BackupPath"]))
print("Server .Jar file is {}".format(serverSettings["ServerJar"]))
print("World folder is named {}".format(serverSettings["WorldFolderName"]))
print("Server Start file is {}".format(serverSettings["ServerStartFile"]))

print("Channel Id is {}".format(discordSettings["DiscordChannelId"]))
print("Role to ping is {}".format(discordSettings["RoleToPing"]))

print("Rcon password is {}".format(rconSettings["RconPassword"]))
print("Rcon server port is {}".format(rconSettings["RconServerPort"]))
time.sleep(5)

#error check to see if all components are there
if os.path.isfile(os.path.join(server, serverSettings["ServerStartFile"])) != True:
    print('No start file found! this will cause the server to not run! exiting in 5 seconds')
    time.sleep(5)
    exit()
''' this is a old asset
if os.path.isfile('backup.bat') != True:
    print('backup.bat not found, this is very likely to cause problems cause problems, exit?')
    leave = ask_user()
    if leave: exit()
'''


#server = os.getcwd()


print(world)




#the main program starter, only runs once the discord bot is ready, ie, after the client.run() is done.
@client.event
async def on_ready():
    print("Bot online")
    await start()
    await timer()

# starts the mc server
async def start():
    print ("starting minecraft server")
    subprocess.Popen([os.path.join(server, serverSettings["ServerStartFile"])], stdin=None, stdout=None, stderr=None, close_fds=True)
    print("make sure the .jar file of your server is server.jar, else the server will not start!")
    channel = client.get_channel(channelid)
    await channel.send(pingid + " SERVER IS UP")
    time.sleep(10)
    
# say the server is down on the discord channel
async def serverdown():
    print("pinging with server down")
    channel = client.get_channel(channelid)
    await channel.send(pingid + " THE SERVER IS DOWN")

#backup the mc world
async def backup():
    print('Backing up')
    await stop()
    time.sleep(5)
    rawTime = time.localtime(time.time())
    ints = [rawTime.tm_year,rawTime.tm_mon,rawTime.tm_mday,rawTime.tm_hour,rawTime.tm_min,rawTime.tm_sec]
    string_time = [str(int) for int in ints]
    preIntTime = "".join(string_time)
    current_time = int(preIntTime)

    print("backing up at " + str(current_time))

    copyFrom = pathlib.Path(r"" + world)
    preCopyTo = pathlib.Path(r"" + backups)

    copyTo = os.path.join(preCopyTo, str(current_time))
    shutil.copytree(copyFrom, copyTo)
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
            print('started')
            time.sleep(10)
        
#ask a y/n are you sure? with an error reset.
def ask_user():
    check = str(input("(Y/N): ")).lower().strip()
    try:
        if check[:1] == 'y':
            return True
        elif check[:1] == 'n':
            return False
        else:
            print('Invalid Input')
            return ask_user()
    except Exception as error:
        print("Please enter valid inputs")
        print(error)
        return ask_user()

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
    


client.run(discordSettings["TOKEN"])
