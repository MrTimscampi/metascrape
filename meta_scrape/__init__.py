"""A headless metadata scraper for media."""
import os
from shutil import copyfile

import sys
from appdirs import AppDirs
import yaml

from yapsy.PluginManager import PluginManagerSingleton

VERSION = "0.0.0"
SCRAPERS_DIRECTORY = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                  'scrapers')
SCRAPER_MANAGER = PluginManagerSingleton.get()

APPLICATION_DIRECTORIES = AppDirs("metascrape", "metascrape")
PRESETS_FILE = os.path.join(APPLICATION_DIRECTORIES.user_config_dir,
                            "presets.yml")

# Make the configuration directory and copy config files
os.makedirs(APPLICATION_DIRECTORIES.user_config_dir, exist_ok=True)
if not os.path.isfile(PRESETS_FILE):
    copyfile(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                          "presets.yml"),
             PRESETS_FILE)

# Load configuration
with open(PRESETS_FILE, 'r') as ymlfile:
    PRESETS = yaml.load(ymlfile)
