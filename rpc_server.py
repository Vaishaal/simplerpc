import tornado
import tornado.web
import tornado.websocket
import tornado.options

import os

import json
import uuid

import argparse
import logging
import time
from inspect import getmembers, isfunction
import rpc
logger = logging.getLogger('gateway')

args = None

def parse_args():
    global args
    static_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
    parser = argparse.ArgumentParser(description='Gateway server')

    parser.add_argument('-v', '--verbose', help='verbose logging', action='store_true')

    parser.add_argument('-s', '--static-path', help='path for static files [default: %(default)s]', default=static_path)

    parser.add_argument('-p', '--listen-port', help='port to listen on [default: %(default)s]', default=9000, type=int, metavar='PORT')
    parser.add_argument('-i', '--listen-interface', help='interface to listen on. [default: %(default)s]', default='0.0.0.0', metavar='IFACE')

    args = parser.parse_args()

connections = set()

class RPCSetupHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print "Sending {0}".format(functions_list.keys())
        self.write_message(json.dumps(functions_list.keys()))
        return None
    def on_message(self, msg):
        pass
    def send(self,msg):
        pass
    def on_close(self):
        pass

class RPCHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        connections.add(self)
        return None
    def on_message(self, msg):
        obj = json.loads(msg)
        print obj
        ret = functions_list[obj[u"name"]](*obj[u"args"])

        self.write_message(json.dumps(ret))
        pass
    def send(self,msg):
        pass
    def on_close(self):
        pass

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

def main():
    parse_args()
    if args.verbose:
        tornado.options.enable_pretty_logging()
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
    settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    }
    application = tornado.web.Application([
        (r"/rpc", RPCSetupHandler),
        (r"/rpc_call", RPCHandler),
        (r"/", MainHandler),
        (r'/static/(.*)', tornado.web.StaticFileHandler, settings["static_path"])
      ],
        **settings)

    print "Listening on %s:%s" % (args.listen_interface, args.listen_port)
    application.listen(args.listen_port, args.listen_interface)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    functions_list = dict([o for o in getmembers(rpc) if isfunction(o[1])])
    main()
