from pyramid.view import view_config
from pyramid.response import Response
from socketio.namespace import BaseNamespace
from socketio import socketio_manage
from datetime import timedelta, datetime, time
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

    def on_settime(self, time_str):
        try:
            self.session['time'] = datetime.strptime(time_str, "%H:%M:%S")
        except ValueError:
            print "Invalid Time!"
            self.emit("settime-status", "invalid");
        else:
            self.emit("settime-status", "success");

    def job_send_message(self):
        self.session['time'] = datetime.now()
        while True:
            time_obj = self.session['time']
            messages = parser.get_messages_for_time(time_obj)
            # reformat messages serverside
            formatted_messages = []
            for message in messages:
                message_copy = copy.deepcopy(message)
                dt = datetime.strptime("{0} {1}".format(message['date'],
                    message['time']), "%Y-%m-%d %H:%M:%S")
                message_copy['date'] = dt.strftime("%m/%d/%Y")
                message_copy['time'] = dt.strftime("%I:%M:%S %p")
                formatted_messages.append(message_copy)

            self.emit("message", formatted_messages)
            self.session['time'] = time_obj + timedelta(seconds=1) 
            gevent.sleep(1)

@view_config(route_name='messages', renderer='memorial:templates/messages.jinja2')
def messages(request):
    return {'message': 'Memorial'}

@view_config(route_name='socketio_service')
def socketio_service(request):
    socketio_manage(request.environ, { '/message': MessageNamespace },
            request=request)
    return Response('')

