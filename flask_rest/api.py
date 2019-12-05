from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS
import json
import time

app = Flask(__name__)
api = Api(app)
cors = CORS(app)


# def abort_if_todo_doesnt_exist(todo_id):
#     if todo_id not in TODOS:
#         abort(404, message="Todo {} doesn't exist".format(todo_id))


parser = reqparse.RequestParser()
parser.add_argument('path')
parser.add_argument('vm')
parser.add_argument('snapshot')


class SingleTask(Resource):
    def get(self):
        return {'message': 'no'}

    def post(self):
        args = parser.parse_args()
        print(args)
        time.sleep(20)
        return args


class GetCfg(Resource):
    def get(self):
        cfg = {'key1': '11111', 'key2': '22222', 'key3': '33333'}
        with open('snap_dct.json') as fi:
            cfg = json.load(fi)
        return cfg


api.add_resource(SingleTask, '/api/single')
api.add_resource(GetCfg, '/api/cfg')


if __name__ == '__main__':
    app.run(debug=True)