#!/usr/bin/python

from user import User
import socket
import re
import datetime as dt
import helper
import threading
import os
'''
Created on Mar 27, 2017

@author: arno
'''

PORT = 1025
LOCALHOST = "127.0.0.1"
LOCAL_BROADCAST = "255.255.255.255"

class Command:
    JOIN = 'JOIN'
    TALK = 'TALK'
    LEAVE = 'LEAVE'
    QUIT = 'QUIT'


def udpSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return s


def sender():
    user = User(raw_input("Enter your name: "))
    print("Welcome " + user.name + " to the chat room. You can now chat!")
    s = udpSocket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    joinMessage = user.buildMessage(Command.JOIN, ''.join([user.name, ' joined!']))
    s.sendto(joinMessage.encode(), (LOCAL_BROADCAST, PORT))

    while True:
        raw = raw_input()
        command = parseUserCommand(raw)
        
        if command is not None:
            handleUserCommand(s, user, command[0], command[1])

        else:
            message = user.buildMessage(Command.TALK, raw)
            s.sendto(message.encode(), (LOCAL_BROADCAST, PORT))


def receiver():

    s = udpSocket()
    try:
        s.bind(('', PORT))

        while True:
            msgBytes, address = s.recvfrom(4096)
            m = helper.parse_message(msgBytes.decode())
            handleMessageReceived(m[0], m[1], m[2])
    finally:
        s.close()


def handleMessageReceived(userName, command, message):

    cur_date_formatted = re.sub('T', ' ', dt.datetime.now().isoformat())

    if Command.JOIN == command:
        print(''.join([cur_date_formatted, ' ', str(userName), ' joined!']))

    elif Command.TALK == command:
        print(''.join([cur_date_formatted, ' [', str(userName), ']: ', message]))
        
    elif Command.LEAVE == command:
        print(''.join([cur_date_formatted, ' ', str(userName), ' left!']))
        
    elif Command.QUIT == command:
        print('Bye now!\n')
        os._exit(1)


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


def handleUserCommand(soc, user, action, content):
    if Command.LEAVE == action:
        leaveMessage = user.buildMessage(Command.LEAVE, '')
        quitMessage = user.buildMessage(Command.QUIT, '')
        soc.sendto(leaveMessage.encode(), (LOCAL_BROADCAST, PORT))
        soc.sendto(quitMessage.encode(), (LOCALHOST, PORT))
        
        

if __name__ == '__main__':
    print("Starting chat")
    threading.Thread(target=receiver).start()
    threading.Thread(target=sender).start()



