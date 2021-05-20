#!/usr/bin/env python3
#-*- conding: utf-8 -*-

import uuid
import os.path
import sys
import Ice
import IceStorm
Ice.loadSlice('iceflix.ice')
import IceFlix


class Client(Ice.Application):
    def run(self, argv):
        print("========================")
        print("Welcome to IceFlix CLI")
        print("========================")
        print("Use 'connect' to connect to a IceFlix server or 'help' for more commands.")
        print("Enter 'exit' or ctrl-D to exit.")


        '''
        broker = self.communicator()
        address = broker.stringToProxy(argv[1])
        main = IceFlix.MainPrx.checkedCast(address)
        if not main:
            raise IceFlix.TemporaryUnavailable()
        '''
        return 0

client = Client()
sys.exit(client.main(sys.argv))
