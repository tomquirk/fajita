"""
Provides linkedin api-related code
"""
import random
import logging
from time import sleep

from fajita.client import Client

logger = logging.getLogger(__name__)


def default_evade():
    """
    A catch-all method to try and evade suspension.
    Currenly, just delays the request by a random (bounded) time
    """
    sleep(random.randint(2, 5))  # sleep a random duration to try and evade suspention


class Fajita(object):
    """
    Extend this to build your wrapper
    """

    def __init__(
        self,
        base_url=None,
        headers={},
        proxies={},
        refresh_cookies=False,
        debug=False,
        username=None,
        password=None,
        authenticate=False,
        cookie_directory=None,
    ):
        self._client = Client(
            headers=headers,
            refresh_cookies=refresh_cookies,
            debug=debug,
            proxies=proxies,
            cookie_directory=cookie_directory,
        )
        self._logger = logger
        self._base_url = base_url
        self._fresh = True  # False if the instance has been used

        logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)

        if authenticate:
            if not (username and password):
                raise Exception("Need username and password to authenticate")
            self._client.authenticate(username, password)

    def _get(self, uri, base_url=None, evade=default_evade, **kwargs):
        """
        GET request to Linkedin API
        """
        if not self._fresh:
            evade()
        self._fresh = False

        url = f"{base_url or self._base_url}{uri}"
        return self._client.session.get(url, **kwargs)

    def _post(self, uri, base_url=None, evade=default_evade, **kwargs):
        """
        POST request to Linkedin API
        """
        if not self._fresh:
            evade()
        self._fresh = False

        url = f"{base_url or self._base_url}{uri}"
        return self._client.session.post(url, **kwargs)

    def _scroll(
        self, uri, method, parse_items, next_page_fn, done_fn, items=[], **kwargs
    ):
        res = None
        if method == "GET":
            res = self._get(uri, **kwargs)
        elif method == "POST":
            res = self._post(uri, **kwargs)
        items = items + parse_items(res)

        if done_fn(items, res, **kwargs):
            return items

        new_kwargs = next_page_fn(**kwargs)
        return self._scroll(
            uri, method, parse_items, next_page_fn, done_fn, items=items, **new_kwargs
        )

