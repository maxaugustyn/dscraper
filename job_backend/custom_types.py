from io import BytesIO
from requests.packages.urllib3.util import parse_url
from dataclasses import dataclass, field
from typing import List


class TypedContent(object):
    """
    Class for anything that can be saved
    """

    def __init__(self, content_type, bvalue, source_url):
        self.content_type = content_type.partition("/")[0].capitalize()
        self.bvalue = BytesIO(bvalue)
        self.source_url = source_url


class ImageURL():
    """
    Class for getting absolute URLs from any kind of URL
    """

    def __init__(self, scraped_url, source_url):
        self.scraped_url = scraped_url
        self.source_url = source_url
        self.parsed_scraped_url = parse_url(self.scraped_url)
        self.parsed_source_url = parse_url(self.source_url)

    def get_absolute(self):
        if self.scraped_url[0:2] == "//":
            return self._from_protocol_relative()

        if self.parsed_scraped_url.scheme is None:
            return self._from_relative()

        return self.scraped_url

    def _from_relative(self):
        return f"{self.parsed_source_url.scheme}://{self.parsed_source_url.host}{self.scraped_url}"

    def _from_protocol_relative(self):
        return f"{self.parsed_source_url.scheme}:{self.scraped_url}"


@dataclass
class ScrapingResult(object):
    text: TypedContent
    images: List[ImageURL]
