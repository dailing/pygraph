from util.logs import get_logger


logger = get_logger('graph')


class Node(object):
    """
        The inputs should be list of (Node, OutputName, inputName)
        To calculate the output of this node, it will get outputs from Node,
        and get the OutputName field and set it to inputName, and give it to 
        self.func

        If Node is None: this indicate that there is a constant input,
            We directly set input_dict[inputName] to OutputName
        If outputName is None: set the whole output to input_dict[inputName]
    """
    def __init__(self, func: callable=None, inputs=[], initial_parameters={}, name=None):
        self.inputs = inputs
        self.outputs = None
        self.func = func
        if isinstance(self.func, type):
            self.func = self.func(**initial_parameters)
        self.current_run_id = None
        self.name = name

    @staticmethod
    def _get_output(node, outputName, run_id):
        if node is None:
            return outputName
        elif outputName is None:
            return node.get_outputs(run_id)
        else:
            output = node.get_outputs(run_id)
            if output is None:
                return None
            elif not isinstance(output, dict):
                raise Exception('Value IS Not Dict')
            else:
                return output[outputName]


    def get_outputs(self, run_id: int):
        logger.info(f'get outputs: {run_id}, {self.name}')
        if self.current_run_id != run_id:
            args = []
            kwargs = {}
            for node, outputName, inputName in self.inputs:
                logger.info(f'call_ node: {node.name}, for {outputName}')
                output = Node._get_output(node, outputName, run_id)
                if inputName is None:
                    args.append(output)
                    if len(kwargs) > 0:
                        raise Exception("FUCK THIS!")
                kwargs[inputName] = Node._get_output(node, outputName, run_id)
            self.outputs = self.func(*args, **kwargs)
            self.current_run_id = run_id
        return self.outputs


class _Tick(object):
    def __init__(self):
        self.tick = 0

    def __call__(self):
        self.tick += 1
        return self.tick

def Tick(*args, **kwargs):
    return Node(_Tick(), *args, **kwargs)


class _OnAll(object):
    def __init__(self, exec_node):
        self.exec_node = exec_node

    def __call__(self, * args, **kwargs):
        for _, v in kwargs.items():
            if not v:
                return None
        for v in args:
            if not v:
                return None
        return self.exec_node.get_outputs()


def OnAll(exec_node, *args, **kwargs):
    return OnAll(_OnAll(exec_node), *args, **kwargs)


class _OnAny(object):
    def __init__(self, exec_node):
        self.exec_node = exec_node

    def __call__(self, *args, **kwargs):
        for _, v in kwargs.items():
            if v:
                return self.exec_node.get_outputs()
        for v in args:
            if v:
                return self.exec_node.get_outputs()


def OnAny(exec_node, *args, **kwargs):
    return Node(_OnAny(exec_node), *args, **kwargs)


class _Change(object):
    def __init__(self, exec_node):
        self.exec_node = exec_node
        self.prev_value = None

    def __call__(self):
        result =  self.exec_node.get_outputs() == self.prev_value
        self.prev_value = self.exec_node.get_outputs()
        return result


def Change(exec_node, *args, **kwargs):
    return Node(_Change(exec_node), *args, **kwargs)


class _Log(object):
    def __call__(self, **kwargs):
        for k, v in kwargs.items():
            print(k, v)


def Log(*args, **kwargs):
    return Node(_Log(), *args, **kwargs)


class Runner(object):
    def __init__(self):
        pass

    def run(self):
        pass


if __name__ == "__main__":
    tickNode = Tick(name='tick')
    tickChange = Change(tickNode, name='change')
    tickLog = Log(inputs=[(tickNode, None, 'Tick')], name='log')
    onTick = OnAny(tickLog, inputs=[(tickChange, None, None)])

    for i in range(10):
        tickLog.get_outputs(run_id=i)
    