#!/usr/bin/env python3
#-*- conding: utf-8 -*-

import uuid
import os.path
import sys
import Ice
import IceStorm
import iceevents
Ice.loadSlice('iceflix.ice')

import IceFlix

class MediaCatalogI(IceFlix.MediaCatalog):
    
    def __init__(self):
        self._id_= str(uuid.uuid4())

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


class ServiceAvailabilityI(IceFlix.ServiceAvailability):
    def __init__(self):
        self.listaCatalog = []
        self.listaAuth=[]
        self.listaMedia=[]

    def addService(self, service, lista, current=None):
        lista.append(service)
        print(lista)

    def catalogService(self, service, id, current=None):
        print("New catalog service: '{}'".format(id))
        self.addService(service, self.listaCatalog)
 
    def authenticationService(self, service, id, current=None):
        print("New authentication service:'{}'".format(id))
        self.addService(service, self.listaAuth)

    def mediaService(self, service, id, current=None):
        print("New media service:'{}'".format(id))
        self.addService(service, self.listaMedia)

class Server(Ice.Application):

    def run(self, argv):
        '''Publisher'''
        event = iceevents.IceEvents(self.communicator())
        topic_manager = event.get_topic_manager()
        topic = event.get_topic('ServiceAvailability')
        publisher = event.get_publisher('ServiceAvailability')
        iceflix = IceFlix.ServiceAvailabilityPrx.uncheckedCast(publisher)
        catalog = MediaCatalogI()
    
        '''Subscriber'''
        eventSubscriber = iceevents.IceEvents(self.communicator())
        broker = eventSubscriber.communicator()
        topic_manager = eventSubscriber.get_topic_manager()
        servant = ServiceAvailabilityI()
        adapter=broker.createObjectAdapter("ServiceAvailabilityAdapter")
        subscriber = adapter.addWithUUID(servant)
        eventSubscriber.subscribe('ServiceAvailability', subscriber)
        iceflix.catalogService(IceFlix.MediaCatalogPrx.checkedCast(subscriber), catalog._id_)
        print("Waiting events... '{}'".format(subscriber))
        topic.getPublisher()
        adapter.activate()
        broker.waitForShutdown()
        topic.unsubscribe(subscriber)


        '''topic_media = "MediaAnnouncements"
        try:
            topic = topic_mgr.retrieve(topic_media)
        except IceStorm.NoSuchTopic:
            print("no such topic found, creating")
            topic = topic_mgr.create(topic_media)

        publisher = topic.getPublisher()
        iceflix = IceFlix.MainPrx.uncheckedCast(publisher)

        iceflix.getCatalogService()'''
        return 0


server = Server()
sys.exit(server.main(sys.argv))