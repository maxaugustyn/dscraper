from flask_restplus import Namespace, Resource, fields
from celery import Celery, states
from celery.result import AsyncResult

CELERY_BACKEND = "redis://redis:6379"
CELERY_BROKER = "pyamqp://guest@rabbit:5672//"
CODES = {
    states.SUCCESS: 200,
    states.PENDING: 202,
    states.FAILURE: 505
}

celery_client = Celery(
    "scrape_tasks", broker=CELERY_BROKER, backend=CELERY_BACKEND)


api = Namespace("v1", description="Distributed Scraper")

job_model = api.model('Job', {
    "id": fields.String,
    "targetURL": fields.String,
    "bucketURL": fields.String,
})

jobs_model = api.model('Jobs', {
    "targetURL": fields.String,
})


@api.route("/job/<id>")
class Job(Resource):
    @api.doc(summary="Info about submitted job", params={"id": "Job ID"}, responses={200: "Job completed", 202: "Job in progress", 404: "Unknown Job", 505: "Job has failed after retries."})
    @api.marshal_with(job_model)
    def get(self, id):
        task = AsyncResult(id, backend=celery_client.backend)
        if task.state == states.SUCCESS:
            return {"id": id, "bucketURL": f"http://127.0.0.1:9001/{id}"}, CODES[task.state]
        else:
            return {"id": id}, CODES[task.state]


@api.route("/jobs")
class Jobs(Resource):
    @api.doc(summary="Submit a job", body=jobs_model,
             responses={200: "Job accepted", 500: "Job submission error."})
    @api.expect(jobs_model)
    @api.marshal_with(job_model)
    def post(self):
        task = celery_client.send_task(
            'scrape_tasks.run', args=[api.payload['targetURL']])
        if task.state not in states.EXCEPTION_STATES:
            return {
                'id': task.id,
                'targetURL': api.payload['targetURL']
            }, 200
        else:
            return {}, 500
