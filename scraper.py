# -*- coding: utf-8 -*-

import json
import logging
try:
    from urllib import quote_plus
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin, quote_plus

import requests
from bs4 import BeautifulSoup, SoupStrainer

from . import settings as s
from .lists import CATEGORIES 
from .utils import (build_url, send_request)


class PlayScraper(object):
    def __init__(self):
        self.categories = CATEGORIES
        self._base_url = s.BASE_URL

    def _parse_app_details(self, soup):
        """Extracts an app's details from its info page.

        :param soup: a strained BeautifulSoup object of an app
        :return: a dictionary of app details
        """
        title = soup.select_one('div.id-app-title').string

        # Main category will be first
        category = [c.attrs['href'].split('/')[-1] for c in soup.select('.category')]

        return {
            'title': title,
            'category': category,
        }

    def details(self, app_id):
        import pdb; pdb.set_trace()
        """Sends a GET request and parses an application's details.

        :param app_id: the app to retrieve details from, e.g. 'com.nintendo.zaaa'
        :return: a dictionary of app details
        """
        url = build_url('details', app_id)

        try:
            response = send_request('GET', url)
            soup = BeautifulSoup(response.content, 'lxml')
        except requests.exceptions.HTTPError as e:
            raise ValueError('Invalid application ID: {app}. {error}'.format(
                app=app_id, error=e))

        return self._parse_app_details(soup)
