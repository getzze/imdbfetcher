# -*- coding: utf-8 -*-

import logging
import string
from .helpers import check_imdb, imdb2number

import imdb as imdbapi

logger = logging.getLogger(__name__)

_imdb = imdbapi.IMDb()


def search_episode(series, season, episode, guess_series_imdb_id=None):
    results = dict()
    logger.debug('Use imdb.org to get imdbID of {} {:d}x{:d}'.format(series, season, episode))

    guess_series_imdb_id = imdb2number(guess_series_imdb_id)
    if not guess_series_imdb_id:
        return results

    try:
        show_imdb = _imdb.get_movie_episodes(guess_series_imdb_id).get('data',dict()).get('episodes', dict())
        episode_imdb = show_imdb[season][episode]
        results['episode_imdb_id'] = check_imdb(episode_imdb.getID())
        logger.debug('Found ids: {}'.format(results))
    except Exception:
        logger.exception('Could not find exact match on imdb.com for show {}, episode {:d}x{:d}'.format(series, season, episode))

    return results
