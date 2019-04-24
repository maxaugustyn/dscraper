from bs4 import BeautifulSoup, Doctype
from custom_types import ImageURL, TypedContent, ScrapingResult


class TextualContentExtractor():
    def __init__(self, content):
        self.content = content
        self.soup = BeautifulSoup(
            self.content.bvalue.getvalue(), 'html.parser')
        self._remove_scripts_and_css()

    def process(self):
        return ScrapingResult(TypedContent("Text",
                                           bytes(
                                               self._get_inner_text(), 'utf-8'),
                                           self.content.source_url),
                              self._get_image_sources())

    def _remove_scripts_and_css(self):
        """
        Removes <script>, <style> and <!DOCTYPE> tags.
        For some reason unpaired tags don't work with string matching
        """
        for unwanted_tag in self.soup(["script", "style"]):
            unwanted_tag.decompose()

        for element in self.soup.contents:
            if isinstance(element, Doctype):
                element.extract()
                break

    def _get_image_sources(self):
        return [ImageURL(image_tag['src'].strip(), self.content.source_url) for image_tag in self.soup(["img"])]

    def _get_inner_text(self):
        return u' '.join(
            [line.rstrip()
             for line in self.soup.find_all(text=True)
             if line != "\n"]
        )
