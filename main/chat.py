#!/usr/bin/python3

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


def udpSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return s


def sender():
    user = User(input("Enter your name: "))
    print("Welcome " + user.name + " to the chat room. You can now chat!\nTo leave at anytime input -1")
    s = udpSocket()

    while True:
        raw = input()
        if isInt(raw):
            print("Leaving Chat room")
            os._exit(1)
            
        
        message = user.buildMessage(raw)
        s.sendto(message.encode(), (DEST_IP, PORT))


def receiver():
    
    s = udpSocket()
    try:
        s.bind((DEST_IP, PORT))
        
        while True:
            msgBytes, address = s.recvfrom(2048)
            m = helper.parse_message(msgBytes.decode())
            display_message(m[0], m[1])
    finally:
        s.close()


def display_message(userName, message):
    cur_date = dt.datetime.now()
    print(''.join([re.sub('T', ' ', cur_date.isoformat()), ' [', str(userName), ']: ', message]))

def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
    
if __name__ == '__main__':
    print("Starting chat")
    threading.Thread(target=sender).start()
    threading.Thread(target=receiver).start()
    
    
    
    