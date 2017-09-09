"""A headless metadata scraper for media."""
from setuptools import find_packages, setup

dependencies = ['click', 'yapsy', 'beautifulsoup4', 'Pillow', 'appdirs', 'pyyaml']

setup(
    name='metascrape',
    version='0.0.0',
    url='https://github.com/MrTimscampi/meta-scrape',
    license='BSD',
    author='Julien Machiels',
    author_email='julien.machiels@std.heh.be',
    description='A headless metadata scraper for media.',
    long_description=__doc__,
    packages=[
        'meta_scrape',
        'meta_scrape.scrapers'
    ],
    include_package_data=True,
    package_data={
        'meta_scrape': ['*.yml'],
        'meta_scrape.scrapers': ['*.plugin']
    },
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'metascrape = meta_scrape.cli:main',
        ],
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
