from flask_restplus import Api
from .jobs import api as job_namespace

api = Api(
    title='Scraper API',
    version='1.0',
    description='A description',
    # All API metadatas
)

api.add_namespace(job_namespace)
