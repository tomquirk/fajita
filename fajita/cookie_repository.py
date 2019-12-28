import os
import pickle


class CookieInvalidException(Exception):
    pass


class CookieRepository(object):
    """
        Class to act as a repository for the cookies.

        TODO: refactor to use http.cookiejar.FileCookieJar
    """

    def __init__(self, cookie_directory=None, validate_fn=None):
        self.cookie_directory = cookie_directory
        self.validate = validate_fn

        if not os.path.exists(self.cookie_directory):
            os.makedirs(self.cookie_directory)

    def _get_cookies_filepath(self, username):
        """
        Return the absolute path of the cookiejar for a given username
        """
        return "{}{}.jr".format(self.cookie_directory, username)

    def _load_cookies_from_cache(self, username):
        cookiejar_filepath = self._get_cookies_filepath(username)
        try:
            with open(cookiejar_filepath, "rb") as f:
                cookies = pickle.load(f)
                return cookies
        except FileNotFoundError:
            return None

    def save(self, cookies, username):

        cookiejar_filepath = self._get_cookies_filepath(username)
        with open(cookiejar_filepath, "wb") as f:
            pickle.dump(cookies, f)

    def get(self, username):
        cookies = self._load_cookies_from_cache(username)
        if cookies and self.validate is not None and not self.validate(cookies):
            raise CookieInvalidException

        return cookies

