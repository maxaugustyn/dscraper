from content_downloader import ContentDownloader
from content_parser import TextualContentExtractor
from content_storage import ContentStorageManager
from custom_types import TypedContent, ImageURL


class ScrapeJob():
    def __init__(self, url):
        self.url = url
        self.downloader = ContentDownloader()
        self.storage = ContentStorageManager()

    def scrape(self, job_id):
        raw_html = self.downloader.get(self.url)
        scraped_html = TextualContentExtractor(raw_html).process()
        self.storage.save_content(job_id, scraped_html.text)
        for image_url in scraped_html.images:
            self.storage._save_content(
                job_id, self.downloader.get(image_url.get_absolute()))


if __name__ == "__main__":
    sj = ScrapeJob("https://onet.pl")
    sj.scrape('xdddd')
