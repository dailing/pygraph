from graphbook.core.gui import Box, Wire, add_wire
from graphbook.util.logs import get_logger

logger = get_logger('session')

class Session(object):
    def __init__(self, boxes=None, wires=None):
        self.boxes = {}
        self.connection = {}
        self.result = {}
        for box in boxes.values():
            self.boxes[box.uuid] = box
            self.connection[box.uuid] = []
        for wire in wires:
            in_index = None
            out_index = None
            if wire.input_to_node_input_type == 'kwargs':
                in_index = wire.input_to_node_input_key
            elif wire.input_to_node_input_type == 'args':
                in_index = wire.input_to_node_input_index
            if wire.output_from_node_output_type =='dict':
                out_index = wire.output_from_node_output_key
            elif wire.output_from_node_output_type == 'list':
                out_index = wire.output_from_node_output_index
            self.connection[wire.input_to_node_uuid].append((
                in_index,
                out_index,
                wire.output_from_node_uuid,
            ))

    def run(self, box_id):
        instance = globals()[self.boxes[box_id].name]
        if not callable(instance):
            self.result[box_id] = instance
            return instance
        all_arg = {}
        for in_index, out_index, req_id in self.connection[box_id]:
            if req_id not in self.result:
                self.run(req_id)
            all_arg[in_index] = self.result[req_id] if out_index is None else self.result[req_id][out_index]
        kwargs = {k:all_arg[k] for k in filter(lambda x: isinstance(x, str), all_arg.keys())}
        args = [all_arg[x] for x in filter(lambda x: isinstance(x, int), all_arg.keys())]
        logger.info(args)
        logger.info(kwargs)
        result = instance(*args, **kwargs)
        if self.boxes[box_id].output_type == 'list':
            if not isinstance(result, list):
                result = [result]
        elif self.boxes[box_id].output_type == 'dict':
            assert isinstance(result, dict)
        self.result[box_id] = result
        return result
        

if __name__ == "__main__":
    def add(a,b):
        return a+b

    def mul(a,b):
        return a*b

    a = 1
    b = 2
    c = 3
    
    boxes = dict(
        a=Box(name='a'),
        b=Box(name='b'),
        c=Box(name='c'),
        mul=Box(name='mul'),
        add=Box(name='add'),
    )
    wires = []
    wires.append( add_wire(boxes['b'], boxes['add'], in_index=1))
    wires.append( add_wire(boxes['a'], boxes['add'], in_index=0))
    wires.append( add_wire(boxes['c'], boxes['mul'], in_index=0))
    wires.append( add_wire(boxes['add'], boxes['mul'], in_index=1))
    ss = Session(boxes, wires)
    logger.info(ss.run(boxes['mul'].uuid))
