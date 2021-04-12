#!/usr/bin/env python3
#-*- conding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('iceflix.ice')

import IceFlix
import IceStorm


class MainI(IceFlix.Main):
    def getAuthenticator(self):
        return 0

    def getCatalogService(self):
        return 0


class ServiceAvailabilityI(Ice.Application, IceFlix.ServiceAvailability):
    
    def get_topic_manager(self):
        key = 'IceStorm.TopicManager.Proxy'
        proxy = self.communicator().propertyToProxy(key)
        if proxy is None:
            print ("property {} not set".format(key))
            return None
        print("Using IceStorm in: '%s'" % key)
        return IceStorm.TopicManagerPrx.checkedCast(proxy)

    def catalogService(self, service, id):
        return 0

    def authenticationService(self, service, id):
        return 0

    def mediaService(self, service, id):
        return 0
    
    def __init__(self, servant):
        topic_mgr = self.get_topic_manager()
        if not topic_mgr:
            print('Invalid proxy')
            return 2
        topic_name = 'ServiceAvailability'
        try:
            topic = topic_mgr.retrieve(topic_name)
        except IceStorm.NoSuchTopic:
            print ("no such topic found, creating")
            topic = topic_mgr.create(topic_name)
        publisher = topic.getPublisher()
        ServiceAvailability = IceFlix.ServiceAvailabilityPrx.uncheckedCast(publisher)
        print("Hola")
        return 0 
        ####Continuar aqui

    
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