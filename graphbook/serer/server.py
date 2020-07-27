from graphbook.core.gui import Box, Wire
from  flask import Flask, redirect, request
from graphbook.util import get_logger
from flask_restful import abort, Api, Resource, reqparse
from flask_socketio import SocketIO, emit


logger = get_logger('server')
app = Flask(__name__, static_folder='../../frontend/dist', static_url_path='/')
api = Api(app, prefix='/api')
socketio = SocketIO(app, logger=logger,)
 

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
    x = 300, y = 200,
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
Wires.append(Wire(
    output_from_node_uuid=Boxes[1].uuid,
    output_from_node_output_type=Boxes[1].output_type,
    output_from_node_output_index=2,
    input_to_node_uuid=Boxes[2].uuid,
    input_to_node_input_type='kwargs',
    input_to_node_input_key='input1'
))
class BoxApi(Resource):
    def __init__(self):
        super(BoxApi, self).__init__()

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
        # args = self.parser.parse_args()
        box  = Box()
        box.from_json(request.json())
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

 
@socketio.on('test_ping')
def handle_test_event(json):
    logger.info('asdf')
    emit('test_pong', 'fuck')

@socketio.on('ping')
def pongResponse():
    emit('pong')

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)


@app.route('/')
def _redirect():
    return redirect('/index.html')

# @app.route('/socket')
# def socket_test():
#     logger.info(request)
#     return 'OK'

if __name__ == "__main__":
    socketio.run(app, port=5555, host='0.0.0.0', debug=True)
