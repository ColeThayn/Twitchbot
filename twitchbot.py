from time import sleep
import socket
import sys
from commands import all_commands
import pyautogui


s = socket.socket()
keyboard = pyautogui

class Twitchbot:

    def __init__(self, Host, Port, Nick, Pass, Chan):
        global s
        global all_commands
        global keyboard
        self.host = Host
        self.port = Port
        self.nick = Nick
        self.oath = Pass
        self.chan = Chan
        self.loading = True


    def connect(self):
        s.connect((self.host, self.port))
        s.send("PASS {}\r\n".format(self.oath).encode("utf-8"))
        s.send("NICK {}\r\n".format(self.nick).encode("utf-8"))
        s.send("JOIN {}\r\n".format(self.chan).encode("utf-8"))

    def send_message(self, message):
        self.message = message
        s.send("PRIVMSG {} :{}\n".format(self.chan,self.message).encode("utf-8"))
        sleep(1)
        print(self.message)

    def get_user(self,response):
        readbuffer = response.split("!")
        user = readbuffer[0][1::]
        return str(user)

    def get_message(self,response):
        seperate = response.split("\r\n")
        temp = ("").join(seperate).strip().split(":",2)[2:]
        message = ("").join(temp)
        return str(message)

    def get_response(self):
        response = s.recv(2048).decode('utf-8')
        return response

    def chat(self):
        while self.loading:
            response = s.recv(2048).decode('utf-8')
            message = self.get_message(response)
            print("{}".format(message))
            
            if "End of /NAMES list" in message:
                self.send_message("/me Succesfully Joined Channel. Ready to Recieve Commands.")
                self.loading = False

        while not self.loading:
            response = s.recv(2048).decode('utf-8')
            user = self.get_user(response)
            message = self.get_message(response)
            print("{} : {}".format(user, message))
            
            #for static string commands add more in commands.py
            for command in all_commands.items():
                if message in command:
                    self.send_message(command[1])
                    continue
            
            list = []
            if "!help" in message:
                self.send_message("This is the help command, these are the available commands:\n")
                for i in all_commands.keys():
                    list.append(i)
                sleep(.5)  
                self.send_message((", ").join(list))   
            
            if "PING" in response:
                print("PING")
                s.send("PONG".encode("utf-8"))
                print("PONG")
                continue
                    

def run():

   bot = Twitchbot("irc.twitch.tv", 6667, "asylumsbot", "oauth:78lihmvosqs5v5summsp3txuqgaban", "#immasylum")
   bot.connect()


if __name__ == '__main__':
    run()





'''
:user!user@user.tmi.twitch.tv PRIVMSG #channel :This is a sample message
'''