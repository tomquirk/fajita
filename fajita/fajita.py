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
        authenticate=True,
    ):
        self._client = Client(
            headers={}, refresh_cookies=refresh_cookies, debug=debug, proxies=proxies
        )
        self._logger = logger
        self._base_url = base_url

        logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)

        if authenticate:
            if not (username and password):
                raise Exception("Need username and password to authenticate")
            self._client.authenticate(username, password)

    def _get(self, uri, base_url=None, evade=default_evade, **kwargs):
        """
        GET request to Linkedin API
        """
        evade()

        url = f"{base_url or self._base_url}{uri}"
        return self._client.session.get(url, **kwargs)

    def _post(self, uri, base_url=None, evade=default_evade, **kwargs):
        """
        POST request to Linkedin API
        """
        evade()

        url = f"{base_url or self._base_url}{uri}"
        return self._client.session.post(url, **kwargs)
