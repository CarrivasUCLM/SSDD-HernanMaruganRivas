#!/usr/bin/env python3
#-*- conding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('iceflix.ice')

import IceFlix
import IceStorm

class MainI(IceFlix.Main):
    def getAuthenticator(self, current=None):
        try:
            print("Este es el authenticator")
            sys.stdout.flush()
        except IceStorm.TemporaryUnavailable:
            print("No hay servicios de autenticacion")

    def getCatalogService(self, current=None):
        try:
            print("Y este es el catálogo")
            sys.stdout.flush()
        except IceStorm.TemporaryUnavailable:
            print("No hay servicios de catalogo")

class ServiceAvailabilityI(IceFlix.ServiceAvailability):
    def __init__(self):
        self.listaCatalog = []
        self.listaAuth=[]
        self.listaMedia=[]

    def addById(self, service, id, lista, current=None):
        _id=format(id)
        lista.append([service, _id])
        print(lista)
    
    def removeById(self, id, lista, current=None):
        _id=format(id)
        self.lista.remove(_id)

    def catalogService(self, service, id, current=None):
        print("New catalog service: '{}'".format(id))
        _id=format(id)
        self.addById(service, _id, self.listaCatalog)
 
    def authenticationService(self, service, id, current=None):
        print("New authentication service:'{}'".format(id))
        _id=format(id)
        _service = format(service)
        self.addById(_service, _id, self.listaAuth)

    def mediaService(self, service, id, current=None):
        print("New media service:'{}'".format(id))
        _id=format(id)
        self.addById(service, _id, self.listaMedia)

    
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
        adapter=broker.createObjectAdapter("MainAdapter")
        proxy=adapter.addWithUUID(servant)
        print(proxy,flush=True)

        adapter.activate()

      
        self.shutdownOnInterrupt()
        ic.waitForShutdown()

        topic.unsubscribe(subscriber)

        return 0
    


server = Server()
sys.exit(server.main(sys.argv))