#coding: utf-8
"""
jsonrpc

Warning: no garbage collect, sorry I donot how to do it.
"""

import uuid
import tornado.ioloop
import tornado.web



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
    if isinstance(ret, basestring):
        ret_type = 'string'
        value = ret
    if isinstance(ret, list) or isinstance(ret, tuple):
        ret_type = 'array'
        value = ret
    else:
        ret_type = 'object'
        uniq_key = str(uuid.uuid4())
        OBJECTS[uniq_key] = obj
        value = uniq_key

    return {
        'type': ret_type,
        'value': value,
    }



class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello world")

application = tornado.web.Application([
    (r'/', MainHandler),
])

if __name__ == '__main__':
    os = remote_import('os')
    print os
    print object_call(os.get('value'), 'listdir', ['.'])

    application.listen(5000)
    tornado.ioloop.IOLoop.instance().start()
