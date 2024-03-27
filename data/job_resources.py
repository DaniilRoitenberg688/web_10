from flask import jsonify
from flask_restful import abort, Resource

from data import db_session
from data.jobs import Job
from data.job_reqparse import parser


def abort_if_job_not_found(id):
    sess = db_session.create_session()
    job = sess.query(Job).get(id)
    if not job:
        abort(404, message='Job not found')


class JobResource(Resource):
    def get(self, job_id):
        abort_if_job_not_found(job_id)
        sess = db_session.create_session()
        job = sess.query(Job).get(job_id)
        return jsonify({'job': job.to_dict(
            only=('team_leader', 'job', 'work_size', 'collaborators'))})

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Job).get(job_id)
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})


class JobListResource(Resource):
    def get(self):
        sess = db_session.create_session()
        jobs = sess.query(Job).all()
        return jsonify(
            {'jobs': [item.to_dict(only=('team_leader', 'job', 'work_size', 'collaborators')) for item in jobs]})

    def post(self):
        args = parser.parse_args()
        sess = db_session.create_session()
        job = Job(team_leader=args['/'],
                  job=args['job'],
                  work_size=args['work_size'],
                  collaborators=args['collaborators'],
                  is_finished=args['is_finished'])
        sess.add(job)
        sess.commit()
        return jsonify({'id': job.id})
