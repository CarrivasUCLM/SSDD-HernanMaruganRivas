#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

'''
Add new user to authorization database
'''

import os
import sys
import json
import signal
import hashlib

import psutil


EXIT_OK = 0
EXIT_ERROR = 1


def auth_server_pid():
    '''
    Search for a running auth_server and get PID
    '''
    for proc in psutil.process_iter():
        if proc.name().startswith('python3'):
            for arg in proc.cmdline():
                if arg.startswith('./'):
                    arg = arg[2:]
                if arg == 'authServer.py':
                    return proc.pid
    return None


def main():
    '''
    Do the stuff
    '''
    try:
        username = sys.argv[1]
    except IndexError:
        print('ERROR: enter a username to reset auth data')
        return EXIT_ERROR

<<<<<<< HEAD
     try:
        password = sys.argv[2]

=======
    try:
        password = sys.argv[2]
       
>>>>>>> 308134f14ca2b7189e35981b3bc92adec46e0b2c
        password_hash = hashlib.sha256(password.encode('utf8')).hexdigest()
    except IndexError:
        print('ERROR: enter a username to reset auth data')
        return EXIT_ERROR

    server_pid = auth_server_pid()
    if not server_pid:
        print('ERROR: auth server process not found. Is the server running?')
        return EXIT_ERROR

    try:
        with open('users.json', 'r') as contents:
            users = json.load(contents)
    except OSError:
        print('ERROR: JSON file with user data not found!')
        return EXIT_ERROR
    except ValueError:
        print('ERROR: corrupt user data!')
        return EXIT_ERROR
    users[username] = {'password_hash':password_hash}
    with open('users.json', 'w') as contents:
        json.dump(users, contents, indent=2, sort_keys=True)
<<<<<<< HEAD
     #os.kill(server_pid, signal.SIGUSR1)

    return EXIT_OK

    
=======
    #os.kill(server_pid, signal.SIGUSR1)

    return EXIT_OK


if __name__ == '__main__':
    sys.exit(main())
>>>>>>> 308134f14ca2b7189e35981b3bc92adec46e0b2c
