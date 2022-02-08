from api import Resource, reqparse, db
from api.models.user import UserModel
from api.schemas.user import user_schema, users_schema


class UserResource(Resource):
    def get(self, user_id=None):
        if user_id is None:
            user = UserModel.query.all()
            return users_schema.dump(user), 200
        user = UserModel.query.get(user_id)
        if not user:
            return {"Error": f"User with {user_id} not found"}, 400
        return user_schema.dump(user), 200

    # @auth.login_required
    # def post(self, author_id):
    #     ...

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('password', required=True)
        data = parser.parse_args()
        user = UserModel(**data)
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user), 201

    def put(self, user_id):
        user = UserModel.query.get(user_id)
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('password', required=False)
        data = parser.parse_args()
        if user is None:
            user = UserModel(**data)
            db.session.add(user)
            db.session.commit()
            return user_schema.dump(user), 201
        if data["username"]:
            user.username = data["username"]
        if data["password"]:
            user.hash_password(data["password"])
        db.session.commit()
        return user_schema.dump(user), 200
