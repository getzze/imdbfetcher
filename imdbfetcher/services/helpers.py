# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
import re

try:
    unicode = unicode
except NameError:
    # 'unicode' is undefined, must be Python 3
    str = str
    unicode = str
    bytes = bytes
    basestring = (str,bytes)
else:
    # 'unicode' exists, must be Python 2
    str = unicode
    unicode = unicode
    bytes = str
    basestring = basestring
    
    
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

IMDB_ID_SIZE = 7

def check_imdb(imdb_id):
    """Return a valid imdbID: 'tt' + 7 digits
    """
    if not imdb_id:
        return None

    if isinstance(imdb_id, float):
        try:
            imdb_id = int(imdb_id)
        except ValueError:
            logger.exception('ImdbID is badly formed, it should contain 7 digits: "{}"'.format(imdb_id))
            return None

    if isinstance(imdb_id, int):
        idd = 'tt{:07d}'.format(imdb_id)
        if len(idd) == IMDB_ID_SIZE + 2:
            return idd
        else:
            logger.info('ImdbID is badly formed, it should contain 7 digits: "{}"'.format(imdb_id))
            return None
    elif isinstance(imdb_id, str) or isinstance(imdb_id, basestring):
        match = re.search(r"t{0,2}(?P<number>\d*)", imdb_id)
        if match:
            return 'tt{:07d}'.format(int(match.group('number')))
        else:
            #raise ValueError('ImdbID is badly formed: "%r"'%(imdb_id))
            logger.info('ImdbID is badly formed: "{}"'.format(imdb_id))
            return None
    else:
        #raise ValueError('ImdbID must be integer or string: %r'%(type(imdb_id)))
        logger.info('ImdbID must be an integer or a string: {}'.format(type(imdb_id)))
        return None

def imdb2number(imdb_id):
    """Return the imdbID as an integer of 7 digits
    """
    imdb_number =  None
    if not imdb_id:
        return imdb_number

    try:
        imdb_id = imdb_id.replace("tt", "")
    except AttributeError:
        # Not a string
        pass

    try:
        imdb_number = int(imdb_id)
    except ValueError:
        logger.exception('Badly defined IMdb id: {}'.format(imdb_id))
        return None
        
    return imdb_number
