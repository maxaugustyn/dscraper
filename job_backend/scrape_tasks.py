from content_downloader import ContentDownloader
from content_parser import TextualContentExtractor
from content_storage import ContentStorageManager
from custom_types import TypedContent, ImageURL
from celery import Celery, group, chain
from random import randint
import time

app = Celery("scrape_tasks", broker="pyamqp://guest@rabbit:5672//",
             backend="redis://redis:6379")


@app.task(bind=True)
def run(self, url):
    master_chain = chain(download_text.s(
        url, self.request.id), download_images.s(self.request.id))()
    master_chain.get(disable_sync_subtasks=False)
    return self.request.id


@app.task(bind=True)
def download_text(self, url, job_id):
    downloader = ContentDownloader()
    storage = ContentStorageManager()
    raw_html = downloader.get(url)
    scraped_html = TextualContentExtractor(raw_html).process()
    storage.save_content(job_id, scraped_html.text)
    return [image_url.get_absolute() for image_url in scraped_html.images]


@app.task
def download_images(image_urls, job_id):
    image_download_group = group([download_image.s(image_url, job_id)
                                  for image_url in image_urls])
    image_download_group().get(disable_sync_subtasks=False)
    return job_id


@app.task()
def download_image(image_url, job_id):
    time.sleep(randint(10, 20))
    downloader = ContentDownloader()
    storage = ContentStorageManager()
    storage.save_content(job_id, downloader.get(image_url))
