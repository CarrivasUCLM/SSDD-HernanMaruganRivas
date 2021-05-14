#!/usr/bin/env python3
#-*- conding: utf-8 -*-
import uuid
import os.path
import sys
import Ice
import IceStorm
Ice.loadSlice('iceflix.ice')
import iceevents
import IceFlix
import logging
import json
import string
import random


USERS_FILE = 'users.json'
PASSWORD_HASH = 'password_hash'
CURRENT_TOKEN = 'current_token'
TOKEN_SIZE = 40

def _build_token_():
    valid_chars = string.digits + string.ascii_letters
    return ''.join([random.choice(valid_chars) for _ in range(TOKEN_SIZE)])


class AuthenticatorI(IceFlix.Authenticator):
    def __init__(self):
        self._id_= str(uuid.uuid4())
        self._users_ = {}
        self._active_tokens_ = set()
        if os.path.exists(USERS_FILE):
            self.refresh()
        else:
           self.__commit__()
    
    def refresh(self, *args, **kwargs):
        '''Reload user DB to RAM'''
        logging.debug('Reloading user database')
        with open(USERS_FILE, 'r') as contents:
            self._users_ = json.load(contents)
        self._active_tokens_ = set([
            user.get(CURRENT_TOKEN, None) for user in self._users_.values()
        ])

    def __commit__(self):
        logging.debug('User database updated!')
        with open(USERS_FILE, 'w') as contents:
            json.dump(self._users_, contents, indent=4, sort_keys=True)

    def refreshAuthorization(self, user, passwordHash, current=None):
        '''Create new auth token'''
        logging.debug(f'New token requested by {user}')
        if user not in self._users_:
            raise IceFlix.Unauthorized()
        current_hash = self._users_[user].get(PASSWORD_HASH, None)
        if not current_hash:
            # User auth is empty
            raise IceFlix.Unauthorized()
        if current_hash != passwordHash:
            raise IceFlix.Unauthorized()

        current_token = self._users_[user].get(CURRENT_TOKEN, None)
        if current_token:
            # pylint: disable=W0702
            try:
                self._active_tokens_.remove(current_token)
            except:
                # Token is already inactive!
                pass
            # pylint: enable=W0702
        new_token = _build_token_()
        self._users_[user][CURRENT_TOKEN] = new_token
        self.__commit__()
        self._active_tokens_.add(new_token)
        return new_token
    
    def isAuthorized(self, authentication):
        '''Return if token is active'''
        return token in self._active_tokens_

class TokenRevocationI(IceFlix.TokenRevocation):
    def revoke(self, authentication):
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
        autenticator = AuthenticatorI()
        adapter2 = broker2.createObjectAdapter("AuthAdapter")
        proxy=adapter.addWithUUID(autenticator)
        publisher_services.authenticationService(IceFlix.AuthenticatorPrx.checkedCast(proxy), autenticator._id_)
        print("Waiting events... '{}'".format(proxy))
        topic.getPublisher()
        
        broker.waitForShutdown()
        topic.unsubscribe(proxy)

        return 0

server = Server()
sys.exit(server.main(sys.argv))