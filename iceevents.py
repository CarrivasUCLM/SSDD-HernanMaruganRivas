
import IceStorm
import logging
from common import ICESTORM_PROXY_PROPERTY


class IceEvents:

    def __init__(self, broker, property_name = ICESTORM_PROXY_PROPERTY):
        self._communicator_= broker
        self._property_name_ = property_name
        self._topic_manager_ = None

    def get_topic_manager(self):
        key = 'IceStorm.TopicManager.Proxy'
        proxy = self._communicator_.propertyToProxy(self._property_name_)
        if proxy is None:
            print("property {} not set".format(key))
            return None
        self._topic_manager_ = IceStorm.TopicManagerPrx.checkedCast(proxy)
    
        return self._topic_manager_

    def communicator(self):
        return self._communicator_


    def get_topic(self, topic_name):
        try:
            topic = self._topic_manager_.retrieve(topic_name)
        except IceStorm.NoSuchTopic:
            logging.warning('IceStorm::Topic({}) not found'.format(topic_name))
            topic = self._topic_manager_.create(topic_name)
        return topic

    def get_publisher(self, topic_name):
        topic = self.get_topic(topic_name)
        return topic.getPublisher()


    def subscribe(self, topic_name, proxy):
        topic = self.get_topic(topic_name)
        topic.subscribeAndGetPublisher({}, proxy)

    def unsubscribe(self, topic_name, proxy):
        topic = self.get_topic(topic_name)
        topic_name.unsubscribe(proxy)