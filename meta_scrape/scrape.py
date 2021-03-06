"""Metascrape subcommand for scraping files and folders."""
import os
import io
import urllib.request
from xml.etree.cElementTree import Element, SubElement, ElementTree

import click
from PIL import Image
import requests

from meta_scrape import SCRAPER_MANAGER, CONFIG
from meta_scrape.utils import crop_poster


@click.command()
@click.option('-t', '--title',
              help='Title to use as search string.',
              metavar='TITLE')
@click.argument('path', type=click.Path(exists=True,
                                        file_okay=True,
                                        dir_okay=True,
                                        writable=True,
                                        readable=True))
def scrape(title, path):
    """Scrape the metadata for the directory."""
    information = None

    if SCRAPER_MANAGER.getAllPlugins():
        # If the title option wasn't provided, get it from the path
        if not title:
            title = os.path.basename(os.path.normpath(path))

        click.echo("Scraping for title: {0}".format(title))
        information = dict()
        for plugin in SCRAPER_MANAGER.getAllPlugins():
            click.echo("Searching for movie using the {0} scraper"
                       .format(plugin.name))
            search_results = plugin.plugin_object.get_search_results(title)
            if not search_results:
                click.echo("No results found using scraper {0}."
                           .format(plugin.name))
                continue
            elif len(search_results) == 1:
                link = search_results[0]['link']
                click.echo("Found a match at: {0}".format(link))
            else:
                click.echo("Multiple matches have been found by the {0} "
                           "scraper:".format(plugin.name))
                for index, link in enumerate(search_results):
                    click.echo("  {0} - {1}\n      URL: {2}"
                               .format(index, link['title'], link['link']))
                click.echo("  s - Skip to the next scraper")
                value = click.prompt('Please enter the number '
                                     'of the link to use',
                                     default=0)
                if value == 's':
                    continue
                else:
                    link = search_results[value]['link']
            information[plugin.name] = plugin.plugin_object.get_movie_information(link)
        if information:
            merged_information = _merge_results(information)
            _write_kodi_nfo(merged_information, path)
            _write_poster(merged_information, path, title)
            _write_fanart(merged_information, path)
            click.echo("Scraped {0} as {1}.".format(title,
                                                    merged_information.get("title")))
        else:
            click.echo("No match found.")
    else:
        click.secho("  No scrapers found.", fg="red")


def _merge_results(information):
    merged_information = dict()
    for field in CONFIG.get('priority'):
        for field_name, scraper_list in field.items():
            for scraper in scraper_list:
                if information.get(scraper) is None:
                    # If the scraper didn't return any info, skip it
                    continue
                elif information.get(scraper).get(field_name) is None:
                    # If the current field in the scraper doesn't have any info, skip it
                    continue
                else:
                    merged_information[field_name] = information.get(scraper).get(field_name)
    return merged_information


def _write_kodi_nfo(information, path):
    """Write the provided information to movie.nfo."""
    click.echo("Writing movie.nfo...")
    root = Element("movie")
    SubElement(root, "title").text = information.get("title")
    SubElement(root, "originaltitle").text = information.get("title")
    SubElement(root, "sorttitle").text = information.get("title")
    SubElement(root, "set").text = information.get("set")
    SubElement(root, "year").text = information.get("release_date")[:4]
    SubElement(root, "plot").text = information.get("plot")
    SubElement(root, "studio").text = information.get("studio")
    tree = ElementTree(root)
    tree.write(os.path.join(path, "movie.nfo"), encoding="UTF-8")


def _write_poster(information, path, title):
    try:
        if not os.path.isfile(os.path.join(path, "poster.jpg")):
            click.echo("Writing poster...")
            request = requests.get(information.get("poster"), stream=True)
            request.raw.decode_content = True
            cover = Image.open(request.raw)
            cover_width, cover_height = cover.size

            if cover_width > cover_height:
                cover = crop_poster(cover, cover_width, cover_height, title)

            cover.save(os.path.join(path, "poster.jpg"))
            os.link(os.path.join(path, "poster.jpg"), os.path.join(path, "folder.jpg"))
            cover.close()
        else:
            raise FileExistsError
    except FileExistsError:
        click.echo('Poster already exists, skipping')


def _write_fanart(information, path):
    try:
        if not os.path.isfile(os.path.join(path, "fanart.jpg")):
            click.echo("Writing fanart...")
            request = requests.get(information.get("poster"), stream=True)
            request.raw.decode_content = True
            cover = Image.open(request.raw)
            cover.save(os.path.join(path, "fanart.jpg"))
            cover.close()
        else:
            raise FileExistsError
    except FileExistsError:
        click.echo('Fanart already exists, skipping')
