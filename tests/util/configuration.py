import configparser
import os

class Configuration(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
          cls.instance = super(Configuration, cls).__new__(cls)
          cls.items = configparser.ConfigParser()
          cls.items.read("config.ini")
        return cls.instance
