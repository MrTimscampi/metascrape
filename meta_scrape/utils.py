"""Utility functions for metascrape."""
import re


def crop_poster(image, cover_width, cover_height, code):
    """Crop a cover to poster size."""
    image_width, image_height = image.size
    image_cropped_width = int(image_width / 2.11)

    # Custom overides for some produt codes
    if (any(prefix in code for prefix in ['HTV', 'EVO', 'DAY', 'ZER', 'EZD', 'DIM'])) or (image_height == 537 and image_width == 800) or ('DOM' in code and image_height == 522):
        image_cropped_width -= 1
    elif (any(prefix in code for prefix in ['NHDT', 'P9', 'RCT'])) or ('FSET' in code and image_width == 675) or (image_height == 538 and image_width == 800):
        image_cropped_width -= 2
    elif any(prefix in code for prefix in ['SDDE', 'SDMS']):
        image_cropped_width -= 3
    elif ('SIMG' in code and image_height == 541) or ('SVDVD' in code and image_height == 950):
        image_cropped_width -= 4
    elif ('DIM' in code) or ('CRZ' and image_height == 541):
        image_cropped_width -= 5
    elif 'XV-65' in code and image_height == 750:
        image_cropped_width -= 6
    elif 'SIMG' in code and image_height == 864:
        image_cropped_width -= 10
    elif 'DOM' in code and image_height == 488:
        image_cropped_width += 13
    elif image_height == 513 and image_width == 800:
        image_cropped_width += 14

    # Handle inverted covers
    if ('DNPD' in code):
        return image.crop([0, 0, image_cropped_width, image_height])
    else:
        return image.crop([image_width - image_cropped_width, 0, image_width, image_height])


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
