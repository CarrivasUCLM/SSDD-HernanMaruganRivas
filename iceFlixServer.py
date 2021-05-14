#!/usr/bin/env python3
#-*- conding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('iceflix.ice')

import IceFlix
import IceStorm

listaCatalog = []
listaAuth=[]
listaMedia=[]

class MainI(IceFlix.Main):
    def getAuthenticator(self, current=None):
        
        if not listaAuth:
            raise IceFlix.TemporaryUnavailable()
        else:  
            return listaAuth.pop() 

    def getCatalogService(self, current=None):
        
        if not listaCatalog:
            raise IceFlix.TemporaryUnavailable()
        else:  
            return listaCatalog.pop()

class ServiceAvailabilityI(IceFlix.ServiceAvailability):
    
    def addService(self, service, lista, current=None):
        lista.append(service)
        print(lista)

    def catalogService(self, service, id, current=None):
        print("New catalog service: '{}'".format(id))
        self.addService(service, listaCatalog)
 
    def authenticationService(self, service, id, current=None):
        print("New authentication service:'{}'".format(id))
        self.addService(service, listaAuth)

    def mediaService(self, service, id, current=None):
        print("New media service:'{}'".format(id))
        self.addService(service, listaMedia)

    
class Server(Ice.Application):

    def get_topic_manager(self):
        key = 'IceStorm.TopicManager.Proxy'
        proxy = self.communicator().propertyToProxy(key)
        if proxy is None:
            print("property '{}' not set".format(key))
            return None

        print("Using IceStorm in: '%s'" % key)
        return IceStorm.TopicManagerPrx.checkedCast(proxy)

    def run(self, argv):
        topic_mgr = self.get_topic_manager()
        if not topic_mgr:
            print("Invalid proxy")
            return 2

        ic = self.communicator()
        servant = ServiceAvailabilityI()
        adapter = ic.createObjectAdapter("ServiceAvailabilityAdapter")
        subscriber = adapter.addWithUUID(servant)

        topic_name = "ServiceAvailability"
        qos = {}
        
        try:
            topic = topic_mgr.retrieve(topic_name)
        except IceStorm.NoSuchTopic:
            topic = topic_mgr.create(topic_name)

        topic.subscribeAndGetPublisher(qos, subscriber)
        #print("Waiting events... '{}'".format(subscriber))

        
        topic.getPublisher()

        adapter.activate()

        broker=self.communicator()
        servant =MainI()
        adapter=broker.createObjectAdapter("IceFlixAdapter")
        proxy=adapter.addWithUUID(servant)
        print(proxy,flush=True)

        adapter.activate()

      
        self.shutdownOnInterrupt()
        ic.waitForShutdown()

        topic.unsubscribe(subscriber)

        return 0
    


server = Server()
sys.exit(server.main(sys.argv))