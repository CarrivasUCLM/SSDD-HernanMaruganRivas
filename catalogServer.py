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
        self.listJson=self.cargar_peliculas()

    def cargar_peliculas(self):
        '''leer json'''
        listJ=[]
        o=open("media.json", "r")
        content=o.read()
        jsondecode=json.loads(content)
        for entity in jsondecode["Calatog"]:
            entityName= entity["Name"]
            entityTag= entity["tag"]
            listJ.append([entityName,entityTag])
        return listJ

    def getTile(self, _id, current=None):
        '''if _id not in listTileMedia:
            raise IceFlix.WrongMediaId(_id)'''
        if not listaMedia:
            raise IceFlix.TemporaryUnavailable()
        self._media.info = self._infoMedia
        self._media.id=_id
        self._media.provider= None
        for i in self.listJson:
            self._media.info.name = i[0]
            self._media.info.tags = i[1]
       
        return self._media
    
    def getTilesByName(self, name, exact, current=None):
        listID=[]
      
        for i in self.listJson:
            nameAux=i[0]
            n = self.listJson.index(i)
            if name == nameAux:
                id=str(uuid.uuid4())
                listID.append(id)
                self.listJson[n].append(id)
            
        return listID

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