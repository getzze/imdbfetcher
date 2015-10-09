# -*- coding: utf-8 -*-

import logging
import re
import json
from mechanize import Browser
from bs4 import BeautifulSoup

from . import check_imdb
from . import urlencode, urlopen, Request, URLError

logger = logging.getLogger(__name__)

# DuckDuckGo information
ddg_url = 'http://api.duckduckgo.com/?'
__ddg_version__ = 0.242
__search_engines__ = ['bing']


imdb_url = 'http://akas.imdb.com/title/{}/episodes?season={:d}'


def search_episode(series, season, episode, guess_series_imdb_id):
	results = dict()
	logger.debug('Use imdb scrapper to get imdbID of {} {:d}x{:d}'.format(series, season, episode))
	br = Browser()
	br.set_handle_robots(False)
	br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.2;\
						WOW64) AppleWebKit/537.11 (KHTML, like Gecko)\
						Chrome/23.0.1271.97 Safari/537.11')]
	r = br.open(imdb_url.format(guess_series_imdb_id, season))
	soup = BeautifulSoup(r, 'lxml')
	for a in soup.find_all('a'):
		href = a.get('href', '')
		match = re.search(r"/title/tt(?P<id>\d{7})/\?ref_=tt_ep_ep" + '{:d}'.format(episode), href)
		if match:
			results['episode_imdb_id'] = check_imdb(match.group('id'))
			logger.debug('Found ids: {}'.format(results))
			break
	return results

def search_movie(title, year=None):
	results = []
	logger.debug('Use scrapper to get imdbID of {} from search engines: {}'.format(title, bangs))
	for bang in bangs:
		query = title + (' %d'%(year) if isinstance(year, (int, float)) else '')
		answer = scrap_query(query, bang=bang)
		if not answer:
			logger.debug('Could not make the search on duckduckgo with query {} and bang {}'%(query, bang))
			continue
		imdb_id = check_imdb(answer)
		if imdb_id not in results:
			results.append(imdb_id)
			logger.debug('Found possible imdbID for title {}: {}'.format(title, imdb_id))
		else:
			logger.debug('ImdbID already matched for title {}: {}'.format(title, imdb_id))
	return results


Response = namedtuple('Response', 
		['type', 'api_version',
		'heading', 'result',
		'related', 'definition',
		'abstract', 'redirect',
		'answer', 'error_code', 
		'error_msg'])
Result = namedtuple('Result', ['html', 'text', 'url', 'icon'])
Related = namedtuple('Related', ['html', 'text', 'url', 'icon'])
Definition = namedtuple('Definition', ['primary','url', 'source'])
Abstract = namedtuple('Abstract', ['primary', 'url', 'text', 'source'])
Redirect = namedtuple('Redirect', ['primary',])
Icon = namedtuple('Icon', ['url', 'width', 'height'])
Topic = namedtuple('Topic',['name', 'results'])
Answer = namedtuple('Answer', ['primary', 'type'])

def scrap_query(query, bang=None):
    
    r = ddg_query('imbd ' + query, bang=bang)
    if 'redirect' in dir(r) and 'primary' in dir(r.redirect):
        url = r.redirect.primary
    else:
        logger.info('Could not find imdb searchpage from DuckDuckGo bang')
        return None
    
    br = Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.2;\
                        WOW64) AppleWebKit/537.11 (KHTML, like Gecko)\
                        Chrome/23.0.1271.97 Safari/537.11')]

    r = br.open(url)
    soup = BeautifulSoup(r)


    for link in soup.find_all('a'):
        href = link.get('href','')
        match = re.search(r"imdb\.com/.*tt(?P<number>[^/]*)", href)
        if match:
            imdb_id = check_imdb(match.group('number'))
            return imdb_id
    
    return None

def ddg_query(query, bang=None, useragent='python-duckduckgo '+str(__ddg_version__), redirect=False, safesearch=True, html=False, meanings=True, **kwargs):
    """
    Query DuckDuckGo, returning a Results object.

    Here's a query that's unlikely to change:

    >>> result = ddg_query('1 + 1')
    >>> result.type
    'nothing'
    >>> result.answer.text
    '1 + 1 = 2'
    >>> result.answer.type
    'calc'

    Keword arguments:
    useragent: UserAgent to use while querying. Default: "python-duckduckgo %d" (str)
    safesearch: True for on, False for off. Default: True (bool)
    html: True to allow HTML in output. Default: False (bool)
    meanings: True to include disambiguations in results (bool)
    Any other keyword arguments are passed directly to DuckDuckGo as URL params.
    """ % __ddg_version__

    safesearch = '1' if safesearch else '-1'
    html = '0' if html else '1'
    meanings = '0' if meanings else '1'
    no_redirect = '0' if redirect else '1'
    params = {
        'q': query,
        'o': 'json',
        'kp': safesearch,
        'no_redirect': no_redirect,
        'no_html': html,
        'd': meanings,
        }
    params.update(kwargs)
    encparams = urlencode(params)
    if bang:
        encparams = encparams.replace('q=', 'q=!{}+'.format(bang))
    url = ddg_url + encparams
    request = Request(url, headers={'User-Agent': useragent})
    try:
        response = urlopen(request)
    except URLError as e:
        return Response(type='Error', api_version=__ddg_version__,
                        heading=None, redirect=None,
                        abstract=None,
                        definition=None,
                        answer=None,
                        related=None,
                        result=None, error_code=1,
                        error_msg=str(e))

    try:
        js = json.loads(response.read())
    except Exception as e:
        return Response(type='Error', api_version=__ddg_version__,
                        heading=None, redirect=None,
                        abstract=None,
                        definition=None,
                        answer=None,
                        related=None,
                        result=None, error_code=2,
                        error_msg='Data from api malformed')

    response.close()

    return process_results(js)

def process_results(js):
    resp_type = {'A': 'answer', 
                 'D': 'disambiguation',
                 'C': 'category',
                 'N': 'name',
                 'E': 'exclusive', 
                 '': 'nothing'}.get(js.get('Type',''), '')
    if resp_type == 'Nothing':
        return Response(type='nothing', api_version=__ddg_version__, heading=None, 
                        result=None, related=None, definition=None, 
                        abstract=None, redirect=None, answer=None,
                        error_code=0, error_msg=None)
    
    redirect = search_deserialize(js, 'Redirect', Redirect)
    abstract = search_deserialize(js, 'Abstract', Abstract)
    definition = search_deserialize(js, 'Definition', Definition)
    js_results = js.get('Results', [])
    results = [result_deserialize(jr, Result) for jr in js_results]
    js_related = js.get('RelatedTopics', [])
    related = [result_deserialize(jr, Related) for jr in js_related]
    answer = search_deserialize(js, 'Answer', Answer)
    return Response(type=resp_type, api_version=__ddg_version__,
                    heading='', redirect=redirect,
                    abstract=abstract,
                    definition=definition,
                    answer=answer,
                    related=related,
                    result=results, error_code=0,
                    error_msg=None)

def result_deserialize(dataset, obj_type):
    d = dataset
    topics = None
    if 'Topics' in d:
        results = [result_deserialize(t, Result) for t in d['Topics']]
        return Topic(d['Name'], results=results)
    text = d['Text']
    url = d['FirstURL']
    html = d['Result']
    i_url = d['Icon']['URL']
    i_width = d['Icon']['Width']
    i_height = d['Icon']['Height']
    icon = None
    if i_url != '':
        icon = Icon(url=i_url, width=i_width,
                    height=i_height)
    dt = obj_type(text=text, url=url, html=html,
                      icon=icon)
    return dt

def search_deserialize(dataset, prefix, obj_type):
    if dataset[prefix] == '':
        return None
    keys = dataset.keys()
    required = filter(lambda x: x.startswith(prefix) and x != prefix, keys)
    unq_required = [r.split(prefix)[1].lower() for r in required]
    args = {ur: dataset[r] for ur, r in map(None, unq_required, required)}
    if prefix in dataset:
        args['primary'] = dataset[prefix]
    return obj_type(**args)
