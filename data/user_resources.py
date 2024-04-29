from data import db_session
from data.user_reqparse import parser
from data.users import User
from flask import jsonify
from flask_restful import abort, Resource


def abort_if_user_not_found(id):
    sess = db_session.create_session()
    user = sess.query(User).get(id)
    if not user:
        abort(404, message='User not found')


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        sess = db_session.create_session()
        user = sess.query(User).get(user_id)
        return jsonify({'User': user.to_dict(only=('surname', 'name', 'age', 'position', 'speciality'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        sess = db_session.create_session()
        user = sess.query(User).get(user_id)
        sess.delete(user)
        sess.commit()
        return jsonify({'success': 'OK'})


class UserListResource(Resource):
    def get(self):
        sess = db_session.create_session()
        users = sess.query(User).all()
        return jsonify({'users': [user.to_dict(only=('surname', 'name', 'age', 'position', 'speciality')) for user in
                                  users]})

    def post(self):
        args = parser.parse_args()
        sess = db_session.create_session()
        user = User(name=args['name'],
                    surname=args['surname'],
                    age=args['age'],
                    position=args['position'],
                    speciality=args['speciality'],
                    address=args['address'],
                    email=args['email'])

        sess.add(user)
        sess.commit()
        return jsonify({'id': user.id})
