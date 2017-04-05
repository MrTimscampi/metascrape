import os
import xml.etree.cElementTree as ET

import click

from meta_scrape import SCRAPER_MANAGER


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
    if SCRAPER_MANAGER.getAllPlugins():
        # If the title option wasn't provided, get it from the path
        if not title:
            title = os.path.basename(os.path.normpath(path))

        click.echo("Scraping for title: {0}".format(title))
        for plugin in SCRAPER_MANAGER.getAllPlugins():
            click.echo("Searching for movie using the {0} scraper"
                       .format(plugin.name))
            click.echo("Using search url: {0}{1}"
                       .format(plugin.plugin_object.SEARCH_URL, title))
            search_results = plugin.plugin_object.get_search_results(title)
            if not search_results:
                click.echo("No results found")
                continue
            elif len(search_results) == 1:
                link = search_results[0]
                click.echo("Found a match at: {0}".format(link))
            else:
                click.echo("Multiple matches have been found by the {0} "
                           "scraper:".format(plugin.name))
                for index, link in enumerate(search_results):
                    click.echo("  {0} - {1}".format(index, link))
                value = click.prompt('Please enter the number '
                                     'of the link to use',
                                     default=0)
                link = search_results[value]
            information = plugin.plugin_object.get_movie_information(link)
        root = ET.Element("movie")
        ET.SubElement(root, "title").text = information.get("title")
        ET.SubElement(root, "originaltitle").text = information.get("title")
        ET.SubElement(root, "sorttitle").text = information.get("title")
        ET.SubElement(root, "set").text = information.get("set")
        ET.SubElement(root, "year").text = information.get("release_date")[:4]
        ET.SubElement(root, "plot").text = information.get("plot")
        ET.SubElement(root, "playcount").text = 0
        ET.SubElement(root, "filenameandpath").text = os.path.join(path,
                                                                   title +
                                                                   ".m4v")
        ET.SubElement(root, "studio").text = information.get("studio")
        tree = ET.ElementTree(root)
        tree.write(os.path.join(path, "movie.nfo"), encoding="UTF-8")
    else:
        click.secho("  No scrapers found.", fg="red")
