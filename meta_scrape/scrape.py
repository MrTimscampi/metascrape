"""Metascrape subcommand for scraping files and folders."""
import os
import io
import urllib.request
from xml.etree.cElementTree import Element, SubElement, ElementTree

import click
from PIL import Image

from meta_scrape import SCRAPER_MANAGER
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
                value = click.prompt('Please enter the number '
                                     'of the link to use',
                                     default=0)
                link = search_results[value]['link']
            information = plugin.plugin_object.get_movie_information(link)
        if information:
            _write_kodi_nfo(information, path)
            _write_poster(information, path)
            _write_fanart(information, path)
            click.echo("Scraped {0} as {1}.".format(title,
                                                    information.get("title")))
        else:
            click.echo("No match found.")
    else:
        click.secho("  No scrapers found.", fg="red")


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


def _write_poster(information, path):
    # TODO: Detect poster format
    # TODO: Crop poster automatically
    cover = Image.open(io.BytesIO(urllib.request.urlopen(
        information.get("poster")).read()))
    cover_width, cover_height = cover.size
    if cover_width > cover_height:
        cover = crop_poster(cover)
    else:
        # This is already in the expected format
        pass
    click.echo("Writing poster...")
    cover.save(os.path.join(path, "folder.jpg"))
    cover.save(os.path.join(path, "poster.jpg"))
    cover.close()


def _write_fanart(information, path):
    # TODO: Detect fanart format
    # TODO: Handle cases where fanart isn't the same source as poster
    cover = Image.open(io.BytesIO(urllib.request.urlopen(
        information.get("poster")).read()))
    cover_width, cover_height = cover.size
    if cover_width > cover_height:
        # This should be the whole cover
        pass
    else:
        # This is a poster
        pass
    click.echo("Writing fanart...")
    cover.save(os.path.join(path, "fanart.jpg"))
    cover.close()
