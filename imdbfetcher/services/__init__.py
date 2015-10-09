# -*- coding: utf-8 -*-

import logging
import re

try:  # for python3.*
    from urllib.parse import urlencode
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
except ImportError:
    # for python2.*
    from urllib2 import urlopen
    from urllib import urlencode
    from urllib2 import Request
    from urllib2 import URLError

logger = logging.getLogger(__name__)

def check_imdb(imdb_id):
    """Return a valid imdbID: 'tt' + 7 digits
    """        
    if not imdb:
        return None
        
    if isinstance(imdb_id, int):
        return u'tt{:.7d}'.format(imdb_id)
    elif isinstance(imdb_id, str) or isinstance(imdb_id, basestring):
        match = re.search(r"t{0,2}(?P<number>\d{7})", imdb_id)
        if match:
            return u'tt' + match.group('number')
        else:
            #raise ValueError('ImdbID is badly formed: "%r"'%(imdb_id))
            logger.info('ImdbID is badly formed: "{}"'.format(imdb_id))
            return None
    else:
        #raise ValueError('ImdbID must be integer or string: %r'%(type(imdb_id)))
        logger.info('ImdbID must be an integer or a string: {}'.format(type(imdb_id)))
		return None

import importlib
import collections
__all_providers = ['tmdb', 'searchengine', 'tvdb', 'omdb', 'python-imdb']
__searches = ['movie', 'episode', 'series', 'info']
providers = dict((t, collections.OrderedDict()) for t in searches)
for provider in __all_providers:
	for search in providers:
		try:
			providers[search][provider] = importlib.import_module('{}_api'.format(provider), '{}_api.search_{}'.format(provider, search))
		except ImportError:
			logger.debug("Provider not found: {}".format(provider))
		except SystemError:
			logger.debug("Function `search_{}` not found in {}_api".format(search, provider))

