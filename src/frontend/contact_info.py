from typing import List
from contact import *
from message import *

class ContactInfo :

    def old_init(self, contact_list : List[Contact]):
        self.contacts = {}
        self.current_contact = None
        for contact in contact_list:
            self.contacts[contact.username] = contact
            self.current_contact = contact


    def __init__(self):
        self.contacts = {}
        self.current_contact = None
        contact_list = [
                Contact("joao_pedro23","João Pedro"),
                Contact("maria_aaaa","Maria"),
                Contact("melhorPai123","Pai"),
                Contact("motherOfAll","Mãe"),
                Contact("juliao_tiozao","Tio Julio"),
                Contact("my_cello","Marcelo"),
                Contact("buhbuh54","Bruna")
        ]
        for contact in contact_list:
            self.contacts[contact.username] = contact
            self.current_contact = contact


    def save_message(self, msg : Message, contact):
        contact.messages.append(msg)

    def save_message_current(self, msg : Message):
        self.save_message(msg,self.current_contact)

    def persist(self):
        for contact in self.contacts:
            username = contact
            for msg in self.contacts[username].messages:
                if not msg.persisted :
                    csv_msg = msg.to_csv_line()
                    file= open("resources/messages/" + str(username) +".txt", "a")
                    file.write(csv_msg + "\n")
                    file.close()
                    msg.set_as_persisted()
    
    '''
    Método que cria um novo contato, caso não exista
    '''
    def create_contact(self, name, username):
        if username in self.contacts:
            return
        new_contact = Contact(username, name)
        self.contacts[new_contact.username] = new_contact

    '''
    Método que retorna objeto Contact correspondente a um username.
    '''
    def get_contact_from_username(self, username):
        if username in self.contacts:
            return self.contacts[username]
        else:
            return None

