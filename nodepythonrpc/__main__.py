import argparse
from tornadorpc.json import JSONRPCHandler
from tornadorpc import private, start_server

class Handler(JSONRPCHandler):

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
