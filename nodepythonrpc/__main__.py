import uuid
import argparse
from tornadorpc.json import JSONRPCHandler
from tornadorpc import private, start_server


OBJECTS = {}
OBJECTS['os'] = __import__('os')

def remote_import(package_name):
    obj = __import__(package_name)
    uniq_key = str(uuid.uuid4())
    OBJECTS[uniq_key] = obj
    return {
        'type': 'object',
        'value': uniq_key,
    }

def object_call(obj_key, func_name, args=[], kwargs={}):
    obj = OBJECTS.get(obj_key)
    if not obj:
        return None
    if not args:
        args = []
    if not kwargs:
        kwargs = {}

    ret = getattr(obj, func_name)(*args, **kwargs)
    print 'ret =', ret, isinstance(ret, basestring)
    if isinstance(ret, basestring):
        ret_type = 'string'
        value = ret
    elif isinstance(ret, list) or isinstance(ret, tuple):
        ret_type = 'array'
        value = ret
    else:
        ret_type = 'object'
        uniq_key = str(uuid.uuid4())
        OBJECTS[uniq_key] = obj
        value = uniq_key

    print value
    return {
        'type': ret_type,
        'value': value,
    }


class Handler(JSONRPCHandler):
    def pyimport(self, package_name):
        return remote_import(package_name)

    def pyobjcall(self, key, func_name, args):
        print 'call', key
        ret = object_call(key, func_name, args)
        print ret
        return ret

    def add(self, x, y):
        return x+y

    def ping(self, obj):
        return obj

    @private
    def private(self):
        #should not get called
        return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-p', '--port', type=int, help='Port to listen', default=28642)
    parser.add_argument('--host', type=str, help='listen host', default='localhost')
    args = parser.parse_args()

    print 'Node-Python-RPC listening on %s:%s' % (args.host, args.port)
    start_server(Handler, port=args.port)
