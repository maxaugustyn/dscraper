from flask_restplus import Namespace, Resource, fields

api = Namespace("v1", description="Distributed Scraper")

job_model = api.model('Job', {
    'id': fields.Integer,
    'targetURL': fields.String,
    'imageBucketURL': fields.String,
    'textURL': fields.String
})

jobs_model = api.model('Jobs', {
    'id': fields.Integer,
    'targetURL': fields.String
})

@api.route("/job/<id>")
class Job(Resource):
    @api.doc(summary="Info about submitted job", params={"id": "An ID"}, responses={200: "Job completed", 202: "Job in progress", 505: "Job has failed after retries."})
    @api.marshal_with(job_model)
    def get(self, id):
        return {"id": id}
    

@api.route("/jobs")
class Jobs(Resource):
    @api.doc(summary="Submit a job", body=jobs_model,
    responses={200: "Job completed", 202: "Job in progress", 500: "Job has failed after retries."})
    @api.expect(jobs_model)
    @api.marshal_with(job_model)    
    def post(self):
        return api.payload
