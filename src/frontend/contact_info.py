from typing import List
from contact import *
from message import *

class ContactInfo :

    def __init__(self, contact_list : List[Contact]):
        self.contacts = {}
        for contact in contact_list:
            self.contacts[contact.username] = contact
        self.current_contact = next(iter(self.contacts))

    def save_message_sent_to_current(self,msg : Message):
        self.save_message(self.current_contact,msg)

    def save_message(self,username : str, msg : Message):
        self.contacts[username].messages.append(msg)