import re
from time import localtime, strftime
from collections import defaultdict


class MessageParser:
    ''' Class used for parsing the 9/11 pager data, and inserting to SQL db. '''

    def __init__(self, filepath):
        ''' Creates a dict with message time as keys. '''
        self.filepath = filepath
        self.msg_time_dict = defaultdict(list) 

        with open(filepath,'r') as f:
            for line in f:
                msg = self.parse_message(line)
                if msg is not None:
                    self.msg_time_dict[msg['time']].append(msg)

    def get_messages_for_now(self):
        ''' Return a list of messages for the current time on 9/11 '''
        now = strftime("%H:%M:%S", localtime())
        messages = self.msg_time_dict[now]
        return messages

    def parse_message(self, message):
        ''' Parse a line of the message text file. '''
        message_format = r"^(\d{4}\-\d\d\-\d\d)\s+(\d\d\:\d\d\:\d\d)\s+(\w+)\s+\[([0-9\?]+)\]\s+(?:\d{1,2}\:\d\d\:\d\d\s+[AP]M)?\s*\w\s+\w+\s+(.*)$"
        p = re.compile(message_format)
        m = p.match(message)
        try:
            groups = m.groups()
            message_dict = {
                'date': groups[0],
                'time': groups[1],
                'service': groups[2],
                'id': groups[3],
                'text': groups[4]
            }
            return message_dict
        except AttributeError:
            return None 



     
