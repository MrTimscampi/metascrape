"""Utility functions for metascrape."""
import re


def crop_poster(image):
    """Crop a cover to poster size."""
    image_width, image_height = image.size
    return image.crop([int(image_width / 2.11), 0, image_width, image_height])


def clean_title(title):
    """Removes format information from the title."""
    replacement_map = {
        " [DVD]": "",
        " [Blu-ray]": "",
        "　": " ",
        " Blu-ray版": "",
        " DVD版": "",
        " 【特価】": "",
        "【10%POINTBACK】": ""
    }
    substrings = sorted(replacement_map, key=lambda k: len(k), reverse=True)
    regexp = re.compile('|'.join(map(re.escape, substrings)))
    return regexp.sub(lambda match: replacement_map[match.group(0)], title)
