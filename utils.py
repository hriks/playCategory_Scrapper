# -*- coding: utf-8 -*-

import logging
try:
    from urllib import quote_plus
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin, quote_plus

import requests
import grequests
from bs4 import BeautifulSoup, SoupStrainer

from . import settings as s

log = logging.getLogger(__name__)


def _handle_grequest_exception(request, exception):
    """Prints out the exception error from grequests."""
    log.error("{e} with {url}".format(e=exception, url=request.url))
    return None


def default_headers():
    return {
        'Origin': 'https://play.google.com',
        'User-Agent': s.USER_AGENT,
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    }


def generate_post_data(results=None, page=None, pagtok=None, children=0):
    """
    Creates the post data for a POST request. Mainly for pagination and
    limiting results.

    :param results: the number of results to return.
    :param page: the page number; used to calculate start = page * results.
    :param pagtok: a page token string for pagination in search.
    :param children: number of apps under each collection (used only when scraping
        a top-level category's collections).
    :return: a dictionary of post data.
    """
    data = {
        'ipf': 1,
        'xhr': 1
    }
    if children:
        data['numChildren'] = children
    if results is not None:
        if page is not None:
            start = 0 if page <= 0 else results * page
            data['start'] = start
        data['num'] = results
    if pagtok is not None:
        data['pagTok'] = pagtok
    return data


def build_url(method, id_string):
    """Creates the absolute url for a type of object. E.g. details, developer,
    or similar.

    :param method: the corresponding method to get for an id.
    :param id: an id string query parameter.
    :return: a URL string.
    """
    if method == 'developer':
        id_string = quote_plus(id_string)

    url = "{base}/{method}?id={id}".format(
        base=s.BASE_URL, method=method, id=id_string)
    return url


def send_request(method, url, data=None, params=None, headers=None, verify=True):
    """Sends a request to the url and returns the response."""

    data = {} if data is None else data
    params = {} if params is None else params
    headers = default_headers() if headers is None else headers
    if not data and method == 'POST':
        data = generate_post_data()

    try:
        response = requests.request(
            method=method,
            url=url,
            data=data,
            params=params,
            headers=headers,
            verify=verify)
        if not response.status_code == requests.codes.ok:
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        log.error(e)
        raise

    return response