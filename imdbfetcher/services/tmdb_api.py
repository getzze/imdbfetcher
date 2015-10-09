# -*- coding: utf-8 -*-

import logging

import tmdbsimple

from .helpers import check_imdb

logger = logging.getLogger(__name__)

# key from vlc (videolan.org)
__tmdb_apikey__ = 'c2c73ebd1e25cbc29cf61158c04ad78a'
_tmdbsimple = tmdbsimple.TMDB(__tmdb_apikey__)

def search_series(series, year=None):
    results = dict()
    logger.debug('Use themoviedb.org to get series imdbID of {}'.format(series))
    search = _tmdbsimple.Search().tv({'query':series, 'year':year})
    if search['total_results'] > 0:
        results['series_tmdb_id'] = search['results'][0]['id']
        series_ids = _tmdbsimple.TV(ids['series_tmdb_id']).external_ids()
        results['series_imdb_id'] = check_imdb(series_ids.get('imdb_id', None))
        results['series_tvdb_id'] = series_ids.get('tvdb_id', None)
        logger.debug('Found ids for series: {}'.format(results))
    else:
        logger.debug('No ids found')
    return results

def search_episode(series, season, episode, guess_episode_tmdb_id):
    results = dict()
    logger.debug('Use themoviedb.org to get imdbID of {} {:d}x{:d}'.format(series, season, episode))
    episode_ids = _tmdbsimple.TV_Episodes(guess_episode_tmdb_id, season, episode).external_ids()
    results['episode_tmdb_id'] = episode_ids.get('id', None)
    results['episode_imdb_id'] = check_imdb(episode_ids.get('imdb_id', None))
    results['episode_tvdb_id'] = episode_ids.get('tvdb_id', None)
    logger.debug('Found ids: {}'.format(results))
    return results

def search_movie(title, year=None):
    results = []
    logger.debug('Use themoviedb.org to get imdbID of {}'.format(title))
    search = _tmdbsimple.Search().movie({'query':title, 'year':year})
    if search['total_results'] > 0:
        movie_tmdbsimple = _tmdbsimple.Movies(search['results'][0]['id'])
        imdb_id = check_imdb(movie_tmdbsimple.info().get('imdb_id',None))
        if imdb_id not in results:
            results.append(imdb_id)
            logger.debug('Found possible imdbID for title {}: {}'.format(title, imdb_id))
    return results
