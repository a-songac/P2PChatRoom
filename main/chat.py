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
DEST_IP = "127.0.0.1"
LOCAL_BROADCAST = "255.255.255.255"

class Command:
    JOIN = 'JOIN'
    TALK = 'TALK'


def udpSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return s


def sender():
    user = User(raw_input("Enter your name: "))
    print("Welcome " + user.name + " to the chat room. You can now chat!\nTo leave at anytime input -1")
    s = udpSocket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    joinMessage = user.buildMessage(Command.JOIN, ''.join([user.name, ' joined!']))
    s.sendto(joinMessage.encode(), (LOCAL_BROADCAST, PORT))

    while True:
        raw = raw_input()
        if isInt(raw):
            print("Leaving Chat room")
            os._exit(1)


        message = user.buildMessage(Command.TALK, raw)
        s.sendto(message.encode(), (LOCAL_BROADCAST, PORT))


def receiver():

    s = udpSocket()
    try:
        s.bind(('', PORT))

        while True:
            msgBytes, address = s.recvfrom(4096)
            m = helper.parse_message(msgBytes.decode())
            handle_message(m[0], m[1], m[2])
    finally:
        s.close()


def handle_message(userName, command, message):

    cur_date_formatted = re.sub('T', ' ', dt.datetime.now().isoformat())

    if Command.JOIN == command:
        print(''.join([cur_date_formatted, ' ', str(userName), ' joined!']))

    elif Command.TALK == command:
        print(''.join([cur_date_formatted, ' [', str(userName), ']: ', message]))


def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

if __name__ == '__main__':
    print("Starting chat")
    threading.Thread(target=receiver).start()
    threading.Thread(target=sender).start()



