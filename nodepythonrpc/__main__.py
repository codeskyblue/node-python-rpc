# coding: utf-8
import argparse
import json
from tornadorpc.json import JSONRPCHandler
from tornadorpc import private, start_server


OBJECTS = {}
OBJECTS['os'] = __import__('os')


def wrap(obj):
    # if isinstance(obj, basestring):
    #     return dict(type='string', value=obj)

    # if isinstance(obj, list) or isinstance(obj, tuple):
    #     return dict(type='array', value=obj)
    try:
        json.dumps(obj)
        return dict(type='json', value=obj)
    except:
        pass
        
    uniq_key = id(obj)
    OBJECTS[uniq_key] = obj
    print id(obj), type(obj)
    if callable(obj):
        return dict(type='function', value=uniq_key)
    return dict(type='object', value=uniq_key)


class Handler(JSONRPCHandler):
    def pyimport(self, package_name):
        obj = __import__(package_name)
        uniq_key = id(obj)
        OBJECTS[uniq_key] = obj
        return dict(type='object', value=uniq_key)

    def pyobjget(self, key, attr):
        try:
            ret = getattr(OBJECTS[key], attr)
        except Exception as e:
            return dict(type='error', value=str(e))
        return wrap(ret)

    def pyobjrun(self, key, args=[], kwargs={}):
        ret = OBJECTS[key](*args, **kwargs)
        return wrap(ret)

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
