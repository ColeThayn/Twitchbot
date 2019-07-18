from time import sleep
import socket
import string
from commands import commands

s = socket.socket()

class Twitchbot:

    def __init__(self, Host, Port, Nick, Pass, Chan):
        global s
        global commands
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
        self.chat()

    def send_message(self, message):
        self.message = message
        s.send("PRIVMSG {} :{}\n".format(self.chan,self.message).encode("utf-8"))
        sleep(1)
        print(self.message)

    def get_user(self):
        response = s.recv(2048).decode('utf-8')
        readbuffer = response.split("!")
        user = readbuffer[0][1::]
        return str(user)

    def get_message(self):
        response = s.recv(2048).decode('utf-8')
        seperate = response.split("\r\n")
        temp = ("").join(seperate).strip().split(":",2)[2:]
        message = ("").join(temp)
        return str(message)

    def chat(self):
        while self.loading:
            message = self.get_message()
            print("{}".format(message))
            
            if "End of /NAMES list" in message:
                self.send_message("/me Succesfully Joined Channel. Ready to Receive Commands.")
                self.loading = False
                #break
        
        while not self.loading:
            
            user = self.get_user()
            message = self.get_message()
            print("{} : {}".format(user, message))
            
            for command in commands.items():
                if message in command:
                    self.send_message(command[1])
                    continue
                    









'''
:user!user@user.tmi.twitch.tv PRIVMSG #channel :This is a sample message
'''
