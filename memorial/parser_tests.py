import unittest

class ParserTests(unittest.TestCase):
    
    def setUp(self):
        from util.MessageParser import MessageParser 
        import os
        filepath = os.path.join(os.path.dirname(__file__), 'data',
            'messages_all.txt')
        shelvepath = os.path.join(os.path.dirname(__file__), 'data',
            'msg_time_dict.shelf')
        self.parser = MessageParser(filepath, shelvepath)

    def test_parse(self):
        import os
        filepath = os.path.join(os.path.dirname(__file__), 'data',
            'messages_all.txt')
        with open(filepath,'r') as f:
            line = f.readline()
            msg = self.parser.parse_message(line)
            self.assertIsNotNone(msg)
        
    def test_get_messages_for_now(self):
        print self.parser.get_messages_for_now()

    def test_get_messages_for_time(self):
        from datetime import datetime
        dt = datetime.strptime("2001-09-13 03:00:00", "%Y-%m-%d %H:%M:%S")
        print self.parser.get_messages_for_time(dt)
                    


