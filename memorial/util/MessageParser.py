import re
from time import localtime, strftime, strptime, mktime
from datetime import datetime
from collections import defaultdict
import shelve


class MessageParser(object):
    ''' Class used for parsing the 9/11 pager data, and inserting to SQL db. '''

    @staticmethod
    def time_obj(timestr):
        ''' Convert time to seconds. '''
        return mktime(strptime(timestr, "%H:%M:%S"))

    def __init__(self, filepath, shelvepath):
        ''' Check to see if we have a "shelved" version of time -> msg
            dictionary.  If we don't, create it.  '''
        self.shelvepath = shelvepath
        self.filepath = filepath
        self.msg_time_dict = None
        shelf = shelve.open(shelvepath)
        if shelf.has_key('msg_time_dict'):
            self.msg_time_dict = shelf['msg_time_dict']
            shelf.close()
        else:
            self.generate_msg_time_dict()
            shelf['msg_time_dict'] = self.msg_time_dict
            shelf.close()

    def generate_msg_time_dict(self):
        ''' Creates a dict with message time as keys. '''
        msg_id_dict = {}
        self.msg_time_dict = defaultdict(list)
        with open(self.filepath, 'r') as msg_file:
            # First we create a dictionary by msg id,
            # in order to concatenate broken-apart messages.
            count = 0
            for line in msg_file:
                msg = self.parse_message(line)
                count = count + 1
                print str(float(count)/float(500000)) + "\r",
                if msg is not None and msg['type'] == "ALPHA":
                    msg_time = self.time_obj(msg['time'])
                    # unholy mess to bucketize messages with the same
                    # id into 5 minute buckets...
                    if msg['id'] not in msg_id_dict:
                        msg_id_dict[msg['id']] = {msg_time : msg}
                    else:
                        appended = False
                        for time_bkt in msg_id_dict[msg['id']]:
                            t_delta = msg_time - time_bkt
                            if abs(t_delta) < 60*5:
                                msg_id_dict[msg['id']][time_bkt]['text'] += \
                                    "<br>" + msg['text']
                                appended = True
                        if not appended:
                            msg_id_dict[msg['id']][msg_time] = msg

        for msg_id in msg_id_dict:
            for time_bkt in msg_id_dict[msg_id]:
                msg = msg_id_dict[msg_id][time_bkt]
                self.msg_time_dict[msg['time']].append(msg)

    def get_messages_for_now(self):
        ''' Return a list of messages for the current time on 9/11. '''
        now = datetime.now()
        now_str = now.strftime("%H:%M:%S")
        messages = self.msg_time_dict[now_str]
        return messages

    def get_messages_for_time(self, time_obj):
        ''' Return a list of messages for the specified time. '''
        time_str = time_obj.strftime("%H:%M:%S") 
        messages = self.msg_time_dict[time_str]
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

        message_regex = re.compile(message_format)
        message_groups = message_regex.match(message)
        try:
            groups = message_groups.groups()
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
