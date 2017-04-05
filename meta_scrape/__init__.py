import os

from yapsy.PluginManager import PluginManagerSingleton

VERSION = "0.0.0"
SCRAPERS_DIRECTORY = os.path.join(os.path.abspath(os.path.dirname(__file__)),'scrapers')
SCRAPER_MANAGER = PluginManagerSingleton.get()
