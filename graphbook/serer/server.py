from graphbook.core.gui import Box
from flask import Flask, redirect
from graphbook.util import get_logger
from flask_restful import abort, Api, Resource, reqparse


logger = get_logger('server')
app = Flask(__name__, static_folder='../../frontend/dist', static_url_path='/')
api = Api(app, prefix='/api')


Boxes = dict()
Boxes['a'] = Box()
Boxes['b'] = Box()
Boxes['b'].x = 200
Boxes['b'].y = 200

class BoxApi(Resource):
    def __init__(self):
        super(BoxApi, self).__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('x', type=float)
        self.parser.add_argument('y', type=float)
        self.parser.add_argument('width', type=float)
        self.parser.add_argument('height', type=float)
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('id', type=str)

    def get(self, box_id):
        return Boxes[box_id].get_json()

    def delete(self, box_id):
        del Boxes[box_id]

    def put(self, box_id):
        args = self.parser.parse_args()
        Boxes[box_id].from_json()
        return 'OK'


class BoxListApi(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('x', type=float)
        self.parser.add_argument('y', type=float)
        self.parser.add_argument('width', type=float)
        self.parser.add_argument('height', type=float)
        self.parser.add_argument('name', type=str)

    def post(self):
        args = self.parser.parse_args()
        box  = Box()
        box.from_json(args)
        Boxes[box.name] = box
        return "OK"

    def get(self):
        l = []
        for i in Boxes.values():
            l.append(i.get_json())
        return l



api.add_resource(BoxApi, '/box/<string:todo_id>')
api.add_resource(BoxListApi, '/box_list')

@app.route('/')
def _redirect():
    return redirect('/index.html')