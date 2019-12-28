import requests
import logging
from fajita.cookie_repository import CookieRepository

logger = logging.getLogger(__name__)


class Client(object):
    def __init__(
        self,
        *,
        debug=False,
        headers={},
        base_url=None,
        refresh_cookies=False,
        proxies={},
        authenticate_fn=None,
        cookie_directory=None
    ):
        self.session = requests.session()
        self.logger = logger
        self._authenticate = authenticate_fn

        self._use_cookie_cache = not refresh_cookies
        self._cookie_repository = (
            CookieRepository(cookie_directory) if cookie_directory else None
        )

        self.session.proxies.update(proxies)
        self.session.headers.update(headers)

        logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)

    @property
    def cookies(self):
        return self.session.cookies

    def _set_session_cookies(self, cookies):
        """
        Set cookies of the current session and save them to a file named as the username.
        """
        self.session.cookies = cookies

    def authenticate(self, username, password):
        if not self._authenticate:
            return

        if self._use_cookie_cache and self._cookie_repository is not None:
            self.logger.debug("Attempting to use cached cookies")
            cookies = self._cookie_repository.get(username)
            if cookies:
                self._set_session_cookies(cookies)
                return

        res = self._authenticate(username, password)

        self._set_session_cookies(res.cookies)

        if self._cookie_repository:
            self._cookie_repository.save(res.cookies, username)
