from graphbook.core.gui import Box, Wire
from  flask import Flask, redirect, request
from graphbook.util import get_logger
from flask_restful import abort, Api, Resource, reqparse


logger = get_logger('server')
app = Flask(__name__, static_folder='../../frontend/dist', static_url_path='/')
api = Api(app, prefix='/api')


Boxes = []
Wires = []
Boxes.append(Box(
    name='a',
    x=10, y=10,
    output_type='value',
    num_input_args=2,
    kwargs = ['input1', 'input2']
))
Boxes.append(Box(
    name='b',
    x = 200, y = 200,
    output_type='list',
    num_input_args=2,
    kwargs = ['input1', 'input2'],
    output_list_number=5,
))
Boxes.append(Box(
    name='c',
    x = 200, y = 400,
    output_type='dict',
    num_input_args=0,
    kwargs = ['input1', 'input2'],
    output_keywords = ['out1', 'out2']
))
Wires.append(Wire(
    output_from_node_uuid=Boxes[0].uuid,
    output_from_node_output_type=Boxes[0].output_type,
    input_to_node_uuid=Boxes[1].uuid,
    input_to_node_input_type='args',
    input_to_node_input_index=0
))
class BoxApi(Resource):
    def __init__(self):
        super(BoxApi, self).__init__()
        # self.parser = reqparse.RequestParser()
        # self.parser.add_argument('x', type=float)
        # self.parser.add_argument('y', type=float)
        # self.parser.add_argument('width', type=float)
        # self.parser.add_argument('height', type=float)
        # self.parser.add_argument('name', type=str)
        # self.parser.add_argument('id', type=str)

    def get(self, box_id):
        return Boxes[box_id].get_json()

    def delete(self, box_id):
        del Boxes[box_id]

    def put(self, box_id):
        logger.info(request.json())
        # args = self.parser.parse_args()
        Boxes[box_id].from_json(request.json())
        return 'OK'


class BoxListApi(Resource):
    def post(self):
        args = self.parser.parse_args()
        box  = Box()
        box.from_json(args)
        Boxes[box.name] = box
        return "OK"

    def get(self):
        return {i.uuid: i.get_json() for i in Boxes}


class WireListApi(Resource):
    def get(self):
        return {i.uuid: i.get_json() for i in Wires}


api.add_resource(BoxApi, '/box/<string:todo_id>')
api.add_resource(BoxListApi, '/box_list')
api.add_resource(WireListApi, '/wire_list')

@app.route('/')
def _redirect():
    return redirect('/index.html')