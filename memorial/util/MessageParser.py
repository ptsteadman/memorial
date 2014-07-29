import re

class MessageParser:
    ''' Class used for parsing the 9/11 pager data, and inserting to SQL db. '''

    def initialize_db(self, filepath):
        ''' Inserts message data into SQL db '''
        self.filepath = filepath
        
    def create_msg_time_dict(self, filepath):
        filepath

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



     
