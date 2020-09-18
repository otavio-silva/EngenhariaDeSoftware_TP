from typing import List
from contact import *
from message import *
from rest_requests import get_user_info_request
import os
from os.path import isfile, join

class ContactInfo :

    def old_init(self, contact_list : List[Contact]):
        self.contacts = {}
        self.current_contact = None
        for contact in contact_list:
            self.contacts[contact.username] = contact
            self.current_contact = contact

    def new_old_init(self):
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
    
    '''
    Recupera lista de contatos a partir dos arquivos persistidos.
    Caso seja o primeiro login, cria uma pasta com o username
    '''
    def __init__(self, username, access_token):
        self.contacts = {}
        self.current_contact = None
        self.username = username
        self.access_token = access_token
        contact_list = self.get_persisted_contact_list()
        for contact in contact_list:
            self.contacts[contact.username] = contact
            self.current_contact = contact


    def save_message(self, msg : Message, contact):
        contact.messages.append(msg)
        #Persistir essa mensagem

    def save_message_current(self, msg : Message):
        self.save_message(msg,self.current_contact)

    def persist(self):
        for contact in self.contacts:
            username = contact
            for msg in self.contacts[username].messages:
                if not msg.persisted :
                    csv_msg = msg.to_csv_line()
                    #file= open("resources/messages/" + str(username) +".txt", "a")
                    file= open("resources/messages/" + self.username + "/" + str(username) +".txt", "a")
                    file.write(csv_msg + "\n")
                    file.close()
                    msg.set_as_persisted()
    
    '''
    Busca pelos arquivos persistidos
    Caso não exista, cria uma pasta com o username
    '''
    def get_persisted_contact_list(self):
        user_folder_path = "resources/messages/" + str(self.username) + "/"
        if not os.path.isdir(user_folder_path):
            os.mkdir(user_folder_path)
        contact_list = []
        onlyfiles = [f for f in os.listdir(user_folder_path) if isfile(join(user_folder_path, f))]
        for filename in onlyfiles:
            contact_username = filename[:-4]
            contact_name = self.get_contact_name(contact_username)
            contact_list.append(Contact(contact_username, contact_name))
        return contact_list

    '''
    Faz uma requisição para descobrir o nome atual de um usuário
    '''
    def get_contact_name(self, username):
        name = ''
        try:
            req = get_user_info_request(username, self.access_token)
            first_name = req.json()['first_name']
            last_name = req.json()['last_name']
            if first_name == '' and last_name == '':
                raise
            if first_name != '':
                name = first_name
            if last_name != '':
                name += ' ' + last_name
        except:
            name = username
        return name

    
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

