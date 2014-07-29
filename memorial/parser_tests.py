import unittest
import os
from collections import defaultdict
from time import localtime, strftime, sleep

class ParserTests(unittest.TestCase):
    def test_parse_line(self):
        from util.MessageParser import MessageParser 
        parser = MessageParser()
        filepath = os.path.join(os.path.dirname(__file__), 'data',
            'messages_all.txt')
        # dictionary of list of messages, with time as keys
        msg_time_dict = defaultdict(list) 

        with open(filepath,'r') as f:
            for line in f:
                msg = parser.parse_message(line)
                if msg is not None:
                    msg_time_dict[msg['time']].append(msg)
        
        while True:
            now = strftime("%H:%M:%S", localtime())
            messages =  msg_time_dict[now]
            for message in messages:
                print "{0} {1} on {2}: {3}".format(message['time'], message['date'], message['service'], message['text'])
            sleep(1)



                    


