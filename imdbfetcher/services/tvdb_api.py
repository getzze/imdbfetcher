# -*- coding: utf-8 -*-

import logging
from . import check_imdb

logger = logging.getLogger(__name__)


# key from pytvdbapi example
from pytvdbapi import api as tvdbapi
__tvdb_apikey__ = "B43FF87DE395DF56"


_tvdb = tvdbapi.TVDB(__tvdb_apikey__)
tvdb_lang = 'en'


def search_series(series, year=None, guess_series_tvdb_id=None, check=True):
	results = dict()
	logger.debug('Use thetvdb.org to get series imdbID of {}'.format(series))
	show_tvdb = dict()
	search = _tvdb.search(series, tvdb_lang)
	if len(search) > 0:
		show_tvdb = search[0]
		if check:
			results['series_tvdb_id'] = check_imdb(show_tvdb.data.get('tvdbid')) or guess_series_tvdb_id
			results['series_imdb_id'] = show_tvdb.data.get('imdbid', None)
			logger.debug('Found ids for series: {}'.format(results))
		results['_query_tvdb'] = show_tvdb
	else:
		logger.debug('No ids found')

	return results


def search_episode(series, season, episode, guess_episode_tvdb_id=None, result_tvdb=None):
	results = dict()
	logger.debug('Use thetvdb.org to get imdbID of {} {:d}x{:d}'.format(series, season, episode))
	# Search for series
	if not result_tvdb:
		show_tvdb = search_series(series, check=False).get('_query_tvdb')
		if not show_tvdb:
			logger.debug('Could not find exact match on thetvdb.com for series "{}"'.format(series))
			return results
	else:
		show_tvdb = result_tvdb
		
	# Search for episode
	try:
		episode_tvdb = show_tvdb.get(season, dict()).get(episode, dict()).get(data, dict())
		results['episode_imdb_id'] = check_imdb(episode_tvdb.get('imdbid'))
		results['episode_tvdb_id'] = episode_tvdb.get('tvdbid', None) or guess_episode_tvdb_id
		logger.debug('Found ids: {}'.format(results))
	except Exception as e:
		logger.exception('Could not find exact match on thetvdb.com for show {}, episode {:d}x{:d}'.format(show_tvdb, season, episode))

	return results
