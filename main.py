from time import sleep
from obswebsocket import obsws, requests
from twitchbot import Twitchbot
from commands import *
from cfg import *

obs_connect = False
loading = True

##################################################################
# Creates an instance of OBS Websocket Class and connects to OBS #
##################################################################
ws = obsws(OBS_Host, OBS_Port, OBS_Password)

try:
    ws.connect()
    print('Successfully connected to OBS!\n\n')
    obs_connect = True

except BaseException:
    print('Unable to connect to OBS.\nThe bot will continue to run but will not be able to control OBS. \nPlease Check that your OBS is running and websocket plugin is acitve. Also confirm that your password, port, and host match.\n\n')


###############################################################
# Creates an intance of the Chatbot & Connects to Twitch chat #
###############################################################
bot = Twitchbot(TB_Host, TB_Port, TB_User, TB_Oauth, TB_CHANNEL)
bot.connect()


###################
# laoding message #
###################
print('Attempting to connect to', TB_CHANNEL[1::], 'on Twitch!\n')
try:
    while loading:

        #Assigning Variables
        response = bot.get_response()
        message = bot.get_message(response)

        if "End of /NAMES list" in message:
            if obs_connect is True:
                bot.send_message('/me Succesfully Joined Channel and ready to recieve commands. OBS is connected.')

            else:
                bot.send_message('/me Succesfully Joined Channel and ready to recieve commands. OBS is NOT connected. Check OBS websocket plugin and settings are correct. Type "!connect" to retry connection.')
            loading = False

except KeyboardInterrupt:
    print('Terminated by user.')

    
#########################################################################################
# While loop that continously listens to chat, responsible for commands and obs control #
#########################################################################################
print('Successfully connected to', TB_CHANNEL[1::] + '!')
try:
    while not loading:
    
        #Assigning Variables
        not_response = bot.get_response()
        user = bot.get_user(not_response)
        message = bot.get_message(not_response) 


        #prints twitch chat.
        print('{} : {}'.format(user, message))


        #Responds to twitches ping
        if "PING" in not_response:
            print('PING')
            bot.Pong(not_response)
            print('PONG')
            continue

        #commands here
        #checks if there is a command detected
        if message.startswith('!'):
            #is command
            print('\tIs Command')
            #Takes "!" out of messaage for checking commands
            command = message[1::]
            
            #All commands, mostly standard strings.
            for cmd in all_commands.items():
                if message in cmd:
                    bot.send_message(cmd[1])
                continue
        
            #help command is seperate it requires more logic that traditional string.
            commands = []
            if "help" in command:
                for cmds in all_commands.keys():
                    commands.append(cmds)
                #sleep(.2)
                bot.send_message('The available commands are: ' + (', ').join(commands) + '\r\n')
                continue

            if "connect" in command:
                try:
                    ws.connect()
                    bot.send_message('Successfully connected to OBS!')
                    
                
                except BaseException:
                    bot.send_message('Unable to connect to OBS.')
                continue

            #OBS commands
            #Requires mod permission. (specified in cfg.py)
            try:
                ws.call(requests.SetCurrentScene(command))

            except BaseException:
                print("No scene with that name.")
            continue

except KeyboardInterrupt:
    print('Terminated by user.')





#ws.call(requests.GetSceneList())
#ws.call(requests.SetCurrentScene(name))
