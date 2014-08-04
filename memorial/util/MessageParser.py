import re
from time import localtime, strftime
from collections import defaultdict


class MessageParser:
    ''' Class used for parsing the 9/11 pager data, and inserting to SQL db. '''

    def __init__(self, filepath):
        ''' Creates a dict with message time as keys. '''
        self.filepath = filepath
        self.msg_id_dict = {}
        self.msg_time_dict = defaultdict(list) 

        with open(filepath,'r') as f:
            # First we create a dictionary by msg id,
            # in order to concatenate broken-apart messages.
            for line in f:
                msg = self.parse_message(line)
                if msg is not None and msg['type'] == "ALPHA":
                    if msg['id'] not in self.msg_id_dict:
                        self.msg_id_dict[msg['id']] = msg
                    else:
                        self.msg_id_dict[msg['id']]['text'] +=  "<br>" + msg['text']

        for msg in self.msg_id_dict.values(): 
            self.msg_time_dict[msg['time']].append(msg)

    def get_messages_for_now(self):
        ''' Return a list of messages for the current time on 9/11 '''
        now = strftime("%H:%M:%S", localtime())
        messages = self.msg_time_dict[now]
        return messages

    def parse_message(self, message):
        ''' Parse a line of the message text file. '''
        message_format = r"(\d{4}-\d{2}-\d{2})\s+" \
                         r"(\d{2}:\d{2}:\d{2})\s+" \
                         r"(\w+)\s+" \
                         r"[\[{]([\d\?]+)[\]}](\d{1,2}:\d\d:\d\d[AP]M)?\s+" \
                         r"(\w)\s+" \
                         r"(ALPHA|ST NUM|SH/TONE)\s+" \
                         r"(.*)" \

        p = re.compile(message_format)
        m = p.match(message)
        try:
            groups = m.groups()
            message_dict = {
                'date': groups[0],
                'time': groups[1],
                'service': groups[2],
                'id': groups[3],
                'garbage': groups[4],
                'code': groups[5],
                'type': groups[6],
                'text': groups[7]
            }
            return message_dict
        except AttributeError:
            return None 



     
