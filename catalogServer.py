#!/usr/bin/env python3
#-*- conding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('iceflix.ice')

import IceFlix

class MediaCatalogI(IceFlix.MediaCatalog):
    def getTile(self, id):
        return 0
    
    def getTilesByName(self, name, exact):
        return True

    def getTilesByTags(self, tags, includeAllTags):
        return 0

    def renameTile(self, id, name, authentication):
        return 0

    def addTags(self, id, tags, authentication):
        return 0
    
    def removeTags(self, id, tags, authentication):
        return 0
    

class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = MediaCatalogI()

        adapter = broker.createObjectAdapter("CatalogAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("catalog"))

        print(proxy, flush=True)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


server = Server()
sys.exit(server.main(sys.argv))