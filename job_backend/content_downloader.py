import requests
import validators
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from custom_types import TypedContent


class ContentDownloader():
    def __init__(self, retry_on_codes=(500, 502, 504), retries=5,
                 exponential_backoff_factor=0.2):
        self.retry_setting = Retry(status_forcelist=retry_on_codes,
                                   total=retries, read=retries, connect=retries,
                                   backoff_factor=exponential_backoff_factor)

    def get(self, url):
        """
        Returns website content or raises Exception
        """
        self._validate(url)
        req = self._get_download_session().get(url)
        req.raise_for_status()
        return TypedContent(req.headers.get("Content-Type"), req.content, req.url)

    def _get_download_session(self):
        """
        Prepares download session with retries
        """
        session = requests.Session()
        adapter = HTTPAdapter(max_retries=self.retry_setting)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def _validate(self, url):
        """
        Throws InvalidURLException on Error
        """
        valid = validators.url(url)
        if not valid:
            raise InvalidURLException(
                f"Presented URL: '{valid.value}' is not valid.")
        else:
            return valid


class InvalidURLException(Exception):
    pass
