"""Utility functions for metascrape."""


def crop_poster(image):
    """Crop a cover to poster size."""
    image_width, image_height = image.size
    return image.crop([int(image_width / 2.11), 0, image_width, image_height])
