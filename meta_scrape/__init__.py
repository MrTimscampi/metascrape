"""A headless metadata scraper for media."""
import os
from shutil import copyfile

from appdirs import AppDirs
import yaml

from yapsy.PluginManager import PluginManagerSingleton

SCRAPERS_DIRECTORY = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                  'scrapers')
SCRAPER_MANAGER = PluginManagerSingleton.get()

APPLICATION_DIRECTORIES = AppDirs("metascrape", "metascrape")
CONFIG_FILE = os.path.join(APPLICATION_DIRECTORIES.user_config_dir,
                           "config.yml")

# Make the configuration directory and copy config files
os.makedirs(APPLICATION_DIRECTORIES.user_config_dir, exist_ok=True)
if not os.path.isfile(CONFIG_FILE):
    copyfile(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                          "config.yml"),
             CONFIG_FILE)

# Load configuration
with open(CONFIG_FILE, 'r') as ymlfile:
    CONFIG = yaml.load(ymlfile)
