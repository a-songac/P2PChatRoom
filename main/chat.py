#!/usr/bin/python

from user import User
import socket
import re
import datetime as dt
import helper
import threading
import os
import argparse
'''
Created on Mar 27, 2017

@author: arno
'''

DEFAULT_PORT = 1025
LOCALHOST = "127.0.0.1"
LOCAL_BROADCAST = "255.255.255.255"

class Command:
    JOIN = 'JOIN'
    TALK = 'TALK'
    LEAVE = 'LEAVE'
    QUIT = 'QUIT'
    WHO = 'WHO'
    PING = 'PING'

class ChatRoom:
    
    participants = {}
    
    @staticmethod  
    def addUser(name, ip):
        if name not in ChatRoom.participants.keys():
            ChatRoom.participants[ip] = name
            
    @staticmethod  
    def removeUser(name):
        if name in ChatRoom.participants.keys():
            del ChatRoom.participants[name]
            
    @staticmethod
    def listUserNames():
            return str(ChatRoom.participants.values())
            

def udpSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    return s


def sender(user, port):
    user.name = raw_input("Enter your name: ")
    print("Welcome " + user.name + " to the chat room. You can now chat!")
    s = udpSocket()

    joinMessage = user.buildMessage(Command.JOIN, ''.join([user.name, ' joined!']))
    s.sendto(joinMessage.encode(), (LOCAL_BROADCAST, port))

    while True:
        raw = raw_input()
        command = parseUserCommand(raw)
        
        if command is not None:
            handleUserCommand(s, port, user, command[0], command[1])

        else:
            message = user.buildMessage(Command.TALK, raw)
            s.sendto(message.encode(), (LOCAL_BROADCAST, port))


def receiver(user, port):

    s = udpSocket()
    try:
        s.bind(('', port))

        while True:
            msgBytes, address = s.recvfrom(4096)
            m = helper.parse_message(str(msgBytes.decode()))
            handleMessageReceived(s, port, user, address, m[0], m[1], m[2])
    finally:
        s.close()


def handleMessageReceived(soc, port, curUser, senderAddress, senderName, command, message):
    cur_date_formatted = re.sub('T', ' ', dt.datetime.now().isoformat())

    if Command.JOIN == command:
        print(''.join([cur_date_formatted, ' ', str(senderName), ' joined!']))
        ChatRoom.addUser(senderName, senderAddress[0])
        pingMessage = curUser.buildMessage(Command.PING, "")
        soc.sendto(pingMessage.encode(), (LOCAL_BROADCAST, port))

    elif Command.TALK == command:
        print(''.join([cur_date_formatted, ' [', str(senderName), ']: ', message]))
        
    elif Command.LEAVE == command:
        print(''.join([cur_date_formatted, ' ', str(senderName), ' left!']))
        ChatRoom.removeUser(str(senderName))
        
    elif Command.QUIT == command:
        print('Bye now!\n')
        os._exit(1)
        
    elif Command.WHO == command:
        print(''.join([cur_date_formatted, ' Connected Users: ', ChatRoom.listUserNames()]))
        
    elif Command.PING == command:
        ChatRoom.addUser(senderName, senderAddress[0])


def parseUserCommand(message):
    command = re.match("\/(.+)", message, re.IGNORECASE)
    if command is not None:
        command = command.group(1).split()
        action = command[0].upper()
        content = ''
        if len(command) > 1:
            content = command[1]
        return (action, content)
    
    return None


def handleUserCommand(soc, port, user, action, content):
    if Command.LEAVE == action:
        leaveMessage = user.buildMessage(Command.LEAVE, '')
        quitMessage = user.buildMessage(Command.QUIT, '')
        soc.sendto(leaveMessage.encode(), (LOCAL_BROADCAST, port))
        soc.sendto(quitMessage.encode(), (LOCALHOST, port))
        
    elif Command.WHO == action:
        message = user.buildMessage(Command.WHO, '')
        soc.sendto(message.encode(), (LOCALHOST, port))
        
    else:
        print("Command not found")
        
        

if __name__ == '__main__':
    
    args = argparse.ArgumentParser(description="Chat room on the LAN")
    helpMessage = 'Port number on which chat runs, default is ' + str(DEFAULT_PORT)
    args.add_argument('-p', '--port', action='store', dest='port', type=int, metavar="", default=DEFAULT_PORT, help=helpMessage)
    parser = args.parse_args()
    
    port = int(parser.port)
    
    if port <= 1024:
        print ("Forbidden port")
        os._exit(1)
    
    print("Starting chat on port " + str(port))
    user = User("")
    threading.Thread(target=receiver, args=[user, port]).start()
    threading.Thread(target=sender, args=[user, port]).start()



