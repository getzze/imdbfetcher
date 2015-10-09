imdbfetcher
===========
Fetch IMDB information

Requirements
------------

`imdbfetcher` relies on several services to get the best information.
The basic installation does not require any external module. It relies on the omdb_ API.
For better matches, use external python modules:

	* tmdbsimple_ (very efficient)
	* pytvdbapi_
	* python-imdb_
	* duckduckgo_ (requires mechanize_ and bs4_ modules)


.. _omdb: http://omdbapi.com/
.. _tmdbsimple: https://github.com/celiao/tmdbsimple
.. _pytvdbapi: https://github.com/fuzzycode/pytvdbapi
.. _python-imdb: https://github.com/nandhp/python-imdb
.. _duckduckgo: https://duckduckgo.com/
.. _mechanize: https://pypi.python.org/pypi/mechanize/
.. _bs4: https://pypi.python.org/pypi/beautifulsoup4/

Usage
-----
Get a movie ID::

    # get_id_movie(<movie_name>, (year=<movie_year>))
    $ get_id_movie('Shawshank redemption')
    {'movie_imdb_id': 'tt0111161'}
    $ get_id_movie('Shawshank redemption', year=1994) 
    {'movie_imdb_id': 'tt0111161'}

Get an episode ID::

    # get_id_episode(<series_name>, <season_number>, <episode_number>)
    $ get_id_episode('Futurama', 1, 7)
    {'episode_imdb_id': 'tt0756887', 'series_imdb_id': 'tt0149460'}

Retrieve information from an ID::

    # get_info(<imdb_id>)
    $ get_info(0756887)
    {'Episode': '7',
      'Season': '1',
      'Title': 'My Three Suns',
      'Type': 'episode',
      'Year': '1999',
      'imdbID': 'tt0756887',
      'seriesID': 'tt0149460'}
 
    $ get_info("tt0756887")
    {'Episode': '7',
      'Season': '1',
      'Title': 'My Three Suns',
      'Type': 'episode',
      'Year': '1999',
      'imdbID': 'tt0756887',
      'seriesID': 'tt0149460'}
 
License
-------
GPL 3
