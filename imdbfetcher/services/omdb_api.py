# -*- coding: utf-8 -*-

import logging
import json
import re
from .helpers import check_imdb, imdb2number
from .helpers import urlencode, urlopen

logger = logging.getLogger(__name__)

#: omdbapi.com url
omdbapi_url = "http://www.omdbapi.com/?"

def search_movie(title, year=None):
    results = omdb_query(title, year=year, match='string')
    if not isinstance(results, list):
        return []
    else:
        return results

def search_series(series, year=None):
    results = dict()
    logger.debug('Use omdbapi.com to get series imdbID of {}'.format(series))
    data_series = omdb_query(series, match='string')
    for response in data_series:
        # check if one answer is of type `series`
        if response.get('Type',None) == 'series':
            results['series_imdb_id'] = check_imdb(response.get('imdbID', None))
            logger.debug('Found ids for series: {}'.format(results))
            break
    return results

def search_info(imdbid):
    results = omdb_query(imdb2number(imdbid), match='imdbid')
    if not isinstance(results, dict):
        return dict()
    else:
        return results


def omdb_query(query, year=None, match='string', n_match=None, **kwargs):
    """Search for information on omdbapi.com with title and (optional) year.
      `match` defines what to look for.

    :param string query: title of the video, or imdbID (ex.: 'tt1234567')
    :param double year: year of the video. Default None
    :param string match: 'string', 'title', 'imdbid' . Perform a query which matches the `title` or the `imdbid`. `string` returns a list of answers, the number of answers is defined by `n_match`.
    :param int n_match: if `match` is `string`, number of matches to return in the list.
    :param kwargs: arguments to add to the url. Ex: omdb_search(query, y=2003) to add '&y=2003' to the url
    :return: found movie
    :rtype: dict with keys such as: Title, Year, imdbID, Type.
              for perfect match:  Language, Country, Director, Writer, Actors, Plot, Poster, Runtime, Rating, Votes, Genre, Released, Rated
    """
    if not query:
        logger.debug('Query is empty: {}'.format(type(query)))
        if match in ('title', 'imdbid'):
            return dict()
        else:
            return []

    match_search = 's'
    if match == 'title':
        match_search = 't'
    if match == 'imdbid':
        match_search = 'i'
        query = check_imdb(query)
    query = query.encode("utf-8")

    params = {'r':'json', match_search: query}
    if year:
        params.update({'y':year})
    params.update(kwargs)

    url = omdbapi_url + urlencode(params)
    try:
        data = urlopen(url).read().decode("utf-8")
        data = json.loads(data)
    except Exception as e:
        logger.exception('Error with url {}'.format(url))
        return dict()

    if data.get("Response") == "False":
        logger.debug(data.get("Error", "Unknown error"))
        return dict()

    if match in ('title', 'imdbid'):
        logger.debug('Information found for video {}: {}'.format(query, data))
        return data
    else:
        ## Return only the first n_match. All if n_match is None
        if not isinstance(n_match, int):
            n_match = None
        elif n_match > len(data.get("Search", [])):
            n_match = None

        result = data.get("Search", [])[:n_match]
        logger.debug('Search results for video {}: {}'.format(query, result))
        return result

