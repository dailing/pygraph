from gui.gui import Box
from flask import Flask
from util import get_logger
from flask_restful import abort, Api, Resource, reqparse


logger = get_logger('server')
app = Flask(__name__, static_folder='static', static_url_path='/static')
api = Api(app, prefix='/api/')


Boxes = dict()

class BoxApi(Resource):
    def __init__(self):
        super(BoxApi, self).__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('x', type=float)
        self.parser.add_argument('y', type=float)
        self.parser.add_argument('width', type=float)
        self.parser.add_argument('height', type=float)
        self.parser.add_argument('node', type=str)
        self.parser.add_argument('input', type=str)

    def get(self, box_id):
        return Boxes[box_id].json()

    def delete(self, box_id):
        del Boxes[box_id]

    def put(self, box_id):
        Boxes[box_id].json


api.add_resource(BoxApi, '/box/<string:todo_id>')