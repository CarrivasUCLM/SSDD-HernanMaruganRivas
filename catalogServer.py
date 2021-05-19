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
import json

listaCatalog = []
listaAuth=[]
listaMedia=[]
listTileMedia=[]

class MediaCatalogI(IceFlix.MediaCatalog):
    
    def __init__(self):
        self._id_= str(uuid.uuid4())
        self._media = IceFlix.Media()
        self._infoMedia = IceFlix.MediaInfo()
  

    def cargar_peliculas(self):
        '''leer json'''
        return 0

    def getTile(self, _id, current=None):
        '''if _id not in listTileMedia:
            raise IceFlix.WrongMediaId(_id)'''
        if not listaMedia:
            raise IceFlix.TemporaryUnavailable()
        self._media.info = self._infoMedia
        self._media.id=_id
        self._media.provider= None
        self._media.info.name = "Pelicula"
        self._media.info.tags = []
        return self._media
    
    def getTilesByName(self, name, exact, current=None):
        listTile=[]
      
        o=open("media.json", "r")
        content=o.read()
        jsondecode=json.loads(content)
        for entity in jsondecode["Calatog"]:
            entityName= entity["Name"]
            print(entityName)
            if name == entityName:
                id=str(uuid.uuid4())
                print(id)
                listTile.append(id)
        return listTile

    def getTilesByTags(self, tags, includeAllTags, current=None):
        return 0

    def renameTile(self, id, name, authentication, current=None):
        return 0

    def addTags(self, id, tags, authentication, current=None):
        return 0
    
    def removeTags(self, id, tags, authentication, current=None):
        return 0
        
class ServiceAvailabilityI(IceFlix.ServiceAvailability):
        

    def addService(self, service, lista, current=None):
        lista.append(service)
        "print(lista)"

    def catalogService(self, service, id, current=None):
        print("New catalog service: '{}'".format(id))
        self.addService(service, listaCatalog)
 
    def authenticationService(self, service, id, current=None):
        print("New authentication service:'{}'".format(id))
        self.addService(service, listaAuth)

    def mediaService(self, service, id, current=None):
        print("New media service:'{}'".format(id)+ "'{}'".format(service))
        _id_=format(id)
        listaMedia.append([_id_, service])
        "print(self.listaMedia)"

class Server(Ice.Application):

    def run(self, argv):
        '''Publisher'''
        event = iceevents.IceEvents(self.communicator())
        topic_manager = event.get_topic_manager()
        topic = event.get_topic('ServiceAvailability')
        publisher = event.get_publisher('ServiceAvailability')
        publisher_services = IceFlix.ServiceAvailabilityPrx.uncheckedCast(publisher)
        

        '''Subscriber'''
        eventSubscriber = iceevents.IceEvents(self.communicator())
        broker = eventSubscriber.communicator()
        topic_manager = eventSubscriber.get_topic_manager()
        servant = ServiceAvailabilityI()
        adapter=broker.createObjectAdapter("IceFlixAdapter")
        proxy_subscriber = adapter.addWithUUID(servant)
        eventSubscriber.subscribe('ServiceAvailability', proxy_subscriber)


        "Comunicacion directa"
        adapter.activate()
        broker2 = self.communicator()
        catalog = MediaCatalogI()
        adapter2 = broker2.createObjectAdapter("CatalogAdapter")
        proxy=adapter.addWithUUID(catalog)
        publisher_services.catalogService(IceFlix.MediaCatalogPrx.checkedCast(proxy), catalog._id_)
        topic.getPublisher()
        
        broker.waitForShutdown()
        topic.unsubscribe(proxy)

        return 0


server = Server()
sys.exit(server.main(sys.argv))