import re
from time import localtime, strftime, strptime, mktime
from collections import defaultdict
import shelve


class MessageParser:
    ''' Class used for parsing the 9/11 pager data, and inserting to SQL db. '''
    
    @staticmethod
    def time_obj(timestr):
        return mktime(strptime(timestr, "%H:%M:%S"))

    def __init__(self, filepath, shelvepath):
        ''' Creates a dict with message time as keys. '''
        self.shelvepath = shelvepath
        self.filepath = filepath
        s = shelve.open(shelvepath)
        if s.has_key('msg_time_dict'):
            self.msg_time_dict = s['msg_time_dict']
            s.close()
        else:
            self.generate_msg_time_dict()
            s['msg_time_dict'] = self.msg_time_dict
            s.close()

    def generate_msg_time_dict(self):
        self.msg_id_dict = {}
        self.msg_time_dict = defaultdict(list)
        with open(self.filepath,'r') as f:
            # First we create a dictionary by msg id,
            # in order to concatenate broken-apart messages.
            count = 0
            for line in f:
                msg = self.parse_message(line)
                count = count + 1
                print str(float(count)/float(500000)) + "\r",
                if msg is not None and msg['type'] == "ALPHA":
                    msg_time = self.time_obj(msg['time'])
                    # unholy mess to bucketize messages with the same
                    # id into 5 minute buckets...
                    if msg['id'] not in self.msg_id_dict:
                        self.msg_id_dict[msg['id']] = { msg_time : msg }
                    else:
                        appended = False
                        for time_bkt in self.msg_id_dict[msg['id']]:
                            t_delta = msg_time - time_bkt
                            if abs(t_delta) < 60*5:
                                self.msg_id_dict[msg['id']][time_bkt]['text'] += \
                                    "<br>" + msg['text']
                                appended = True
                        if not appended:
                            self.msg_id_dict[msg['id']][msg_time] =  msg

        for msg_id in self.msg_id_dict: 
            for time_bkt in self.msg_id_dict[msg_id]:
                msg = self.msg_id_dict[msg_id][time_bkt]
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



     
