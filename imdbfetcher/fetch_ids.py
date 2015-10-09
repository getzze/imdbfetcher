#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time
from .services import providers

logger = logging.getLogger(__name__)


def get_id_movie(title, year=None, use_tmdbsimple=True, use_omdb=True, use_scrapper=True):
    """Get imdbID
    For Movie:
        require: `title`, (optional `year`)
        return: imdbid
    """
    # Time execution
    start_time = time.time()

    # results are stored in a list
    results = []
    if use_tmdbsimple:
        query = providers['movie'].get('tmdb')
        if query:
            results.extend(query(title, year))

    if use_scrapper:
        query = providers['movie'].get('searchengine')
        if query:
            results.extend(query(title, year))

    if use_omdb:
        query = providers['movie'].get('omdb')
        if query:
            results.extend(query(title, year))


    end_time = time.time()
    delta = end_time - start_time

    if len(results) <= 0: ## No match
        logger.info('No perfect match for title "%s" in %.2f s.'%(title, delta))
        return None
    elif len(results) == 1: ## One single match
        logger.info('One single match for title `{}` found in {:.2f} s: imdbID {}'.format(title, delta, results[0]))
        return results[0]
    else:
        best_match = results[0]
        ## TO DO : compare to best value
        #for match in matches[1:]:
            #response = omdb_search(int2str_imdb(match), match='imdbid')
            #if response.get('Type',None) == 'movie':
                #(title, year) = (response.get('Title',None),response.get('Year',None) )
        #end_time = time.time()
        logger.info('Best match for title "{}" found in {:.2f} s: imdbID {}'.format(title, delta, best_match))
        return best_match

def get_id_series(series, year=None, use_tmdbsimple=True, use_tvdb=True, use_omdb=True):
    """Get imdbID
    For Episode:
        require: `series`, `season`, `episode`, (optional `year`)
        return: dict with keys (imdb_id, series_imdb_id, tvdb_id, series_tvdb_id, tmdb_id, series_tmdb_id)
    """
    # Time execution
    start_time = time.time()

    ids = dict()

    # Get series imdbID
    if use_tmdbsimple:
        query = providers['series'].get('tmdb')
        if query:
            ids.update(query(series, year))
    if use_tvdb and not ids.get('series_imdb_id'):
        query = providers['series'].get('tvdb')
        if query:
            ids.update(query(series, guess_series_tvdb_id=ids.get('series_tvdb_id')))
    if use_omdb and not ids.get('series_imdb_id'):
        query = providers['series'].get('omdb')
        if query:
            ids.update(query(series, year))

    end_time = time.time()
    delta = end_time - start_time
    logger.info('Ids for series "{}" found in {:.2f} s: {}'.format(series, delta, ids))

    return ids

def get_id_episode(series, season, episode, year=None, use_tmdbsimple=True, use_scrapper=True, use_tvdb=True, use_omdb=True, use_imdb=True):
    # Collect information on the series
    ids = get_id_series(series, year=year, use_tmdbsimple=use_tmdbsimple, use_tvdb=use_tvdb, use_omdb=use_omdb)

    # Time execution
    start_time = time.time()

    # Get episode imdbID
    if use_tmdbsimple and ids.get('series_tmdb_id'):
        query = providers['episode'].get('tmdb')
        if query:
            ids.update(query(series, season, episode, guess_episode_tmdb_id=ids['series_tmdb_id']))
    if use_scrapper and not ids.get('episode_imdb_id') and ids.get('series_imdb_id'):
        query = providers['episode'].get('searchengine')
        if query:
            ids.update(query(series, season, episode, guess_episode_imdb_id=ids['series_imdb_id']))
    if use_tvdb and not ids.get('episode_imdb_id'):
        query = providers['episode'].get('tvdb')
        if query:
            ids.update(query(series, season, episode, guess_episode_tvdb_id=ids.get('series_tvdb_id'), result_tvdb=ids.get('_query_tvdb')))
    if use_imdb and not ids.get('episode_imdb_id'):
        query = providers['episode'].get('omdb')
        if query:
            ids.update(query(series, season, episode))
    if use_imdb and not ids.get('episode_imdb_id') and ids.get('series_imdb_id'):
        query = providers['episode'].get('python-imdb')
        if query:
            ids.update(query(series, season, episode, guess_series_imdb_id=ids['series_imdb_id']))

    end_time = time.time()
    delta = end_time - start_time
    logger.info('Ids for "{} {:d}x{:d}" found in {:.2f} s: {}'.format(series, season, episode, delta, ids))
    if '_query_tvdb' in ids:
        ids.pop('_query_tvdb')

    return ids

def get_info(imdb_id):
    query = providers['info'].get('omdb')
    if query:
        return query(imdb_id)
    else:
        return dict()
