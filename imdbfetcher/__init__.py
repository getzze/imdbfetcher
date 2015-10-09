# -*- coding: utf-8 -*-
__title__ = 'imdbfetcher'
__version__ = '0.1'
__license__ = 'GPL3'

import logging

from .fetch_ids import get_info, get_id_movie, get_id_episode

logging.getLogger(__name__).addHandler(logging.NullHandler())
