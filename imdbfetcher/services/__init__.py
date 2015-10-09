# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger(__name__)

import importlib
import collections
__all_providers = ['tmdb', 'searchengine', 'tvdb', 'omdb', 'python-imdb']
__searches = ['movie', 'episode', 'series', 'info']
providers = dict((t, collections.OrderedDict()) for t in __searches)
for provider in __all_providers:
    for search in providers:
        try:
            mod = importlib.import_module('imdbfetcher.services.{}_api'.format(provider))
            providers[search][provider] = getattr(mod, 'search_{}'.format(search))
        except ImportError as e:
            #print("Provider not working: {}: {}".format(provider, e))
            logger.debug("Provider not working: {}".format(provider))
        except (SystemError, AttributeError) as e:
            #print("Function `search_{}` not found in {}_api: {}".format(search, provider, e))
            logger.debug("Function `search_{}` not found in {}_api".format(search, provider))

