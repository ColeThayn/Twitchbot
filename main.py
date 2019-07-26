from time import sleep
from obswebsocket import obsws, requests
from twitchbot import Twitchbot
from commands import *
from cfg import *


#Creates an instance of OBS Websocket Class and connects to OBS
ws = obsws(OBS_Host, OBS_Port, OBS_Password)
ws.connect()

# Creates an intance of the Chatbot & Connects to Twitch chat
bot = Twitchbot(TB_Host, TB_Port, TB_User, TB_Oauth, TB_CHANNEL)
bot.connect()

#While loop that continously listens to chat, responsible for 
while True:
    #Assigning Variables
    response = bot.get_response()
    user = bot.get_user(response)
    message = bot.get_message(response)

    # prints twitch chat.
    print('{} : {}'.format(user, message))

    # commands here
    # checks if there is a command detected
    if message.startswith('!'):
        #is command
        print('Is command')
        #Takes "!" out of messaage for checking commands
        command = message.split('!')[1]
        print(command)

        # All commands, mostly standard strings.
        try:
            ws.call(requests.SetCurrentScene(command))
        
        except:
            raise "No scene with that name."
        
        
            
            





#ws.call(requests.GetSceneList())
#ws.call(requests.SetCurrentScene(name))
