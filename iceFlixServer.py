#!/usr/bin/env python3
#-*- conding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('iceflix.ice')

import IceFlix


class MainI(IceFlix.Main):
    def getAuthenticator(self):
        return 0

    def getCatalogService(self):
        return 0


class ServiceAvailabilityI(IceFlix.ServiceAvailability):
    def catalogService(self, service, id):
        return 0

    def authenticationService(self, service, id):
        return 0

    def mediaService(self, service, id):
        return 0
    
class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = MainI()

        adapter = broker.createObjectAdapter("MainAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("main"))

        print(proxy, flush=True)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


server = Server()
sys.exit(server.main(sys.argv))