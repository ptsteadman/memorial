from pyramid.view import view_config
from pyramid.response import Response
from socketio.namespace import BaseNamespace
from socketio import socketio_manage
from time import strftime, strptime
import gevent
from util.MessageParser import MessageParser 
import os
import copy

filepath = os.path.join(os.path.dirname(__file__), 'data',
    'messages_all.txt')
shelvepath = os.path.join(os.path.dirname(__file__), 'data',
    'msg_time_dict.shelf')

parser = MessageParser(filepath, shelvepath)

class MessageNamespace(BaseNamespace):
    def initialize(self):
        print "INIT NS"
        self.spawn(self.job_send_message)

    def job_send_message(self):
        while True:
            messages = parser.get_messages_for_now()
            # reformat messages serverside
            formatted_messages = []
            for message in messages:
                message_copy = copy.deepcopy(message)
                datetime = strptime("{0} {1}".format(message['date'],
                    message['time']), "%Y-%m-%d %H:%M:%S")
                message_copy['date'] = strftime("%m/%d/%Y", datetime)
                message_copy['time'] = strftime("%I:%M:%S %p", datetime)
                formatted_messages.append(message_copy)

            self.emit("message", formatted_messages)
            gevent.sleep(1)

@view_config(route_name='messages', renderer='memorial:templates/messages.jinja2')
def messages(request):
    return {'message': 'Memorial'}

@view_config(route_name='socketio_service')
def socketio_service(request):
    socketio_manage(request.environ, { '/message': MessageNamespace },
            request=request)
    return Response('')

