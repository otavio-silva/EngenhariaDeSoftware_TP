from message import *
from typing import List

class Contact :

    def __init__(self, username : str, name : str):
        self.username = username
        self.name = name
        self.messages : List[Message] = []

    def search_msg_id(self, message_id):
        for msg in self.messages:
            if msg.id == message_id:
                return True
        return False