from message import *
from typing import List

class Contact :

    def __init__(self, username : str, name : str):
        self.username = username
        self.name = name
        self.messages : List[Message] = []
