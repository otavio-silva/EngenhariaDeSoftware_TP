import flask
from flask import request, jsonify, make_response
import threading
from ui_lib import *
from contact_info import *
from rest_requests import *
import sys

#TODO Double tick: Enviar requsição informando que leu uma conversa com username X pque tinha novas msgs (LIDA)
# Receber requisições que um usuario leu ou recebeu mensagens.
#TODO Criar novo contato

app = flask.Flask(__name__)
#app.config["DEBUG"] = True #Quebra o uso de thread separada

'''
URL para recebimento de mensagens.
data:
    {'id' 
    'sender'
    'content'
    'created_at'}
'''
@app.route('/api/messages', methods=['POST'])
def receive_message_from_request():
    try:
        message_id = request.form['id']
        sender_username = request.form['sender']
        message_content = request.form['content']
        #created_at = request.form['created_at']
        #Escrever no arquivo e só depois enviar a resposta
        receive_message_from_server(message_id, sender_username, message_content)
        response = make_response(jsonify({"success": True}), 201)

    except Exception as e:
        print(e)
        response = make_response(jsonify({"success": False}), 500)
    
    return response

'''
Função chamada pela receive_message_from_request para efetivar o recebimento de uma mensagem
Requer que window, contact_info e msg_area sejam globais
'''
def receive_message_from_server(message_id, sender_username, message_content):
    contact_info = get_contact_info()#Pega variavel de ui_lib
    msg_area = get_msg_area()#Pega variavel de ui_lib

    msg : Message = Message(message_content, MessageOrigin.RECEIVED)
    sender_contact = contact_info.get_contact_from_username(sender_username)
    #Cria novo contato, consultando seu nome no servidor
    #TODO consultar servidor para saber o nome o usuario
    if sender_contact == None:
        contact_info.create_contact(sender_username, sender_username)
        sender_contact = contact_info.get_contact_from_username(sender_username)
        update_contact_area(window, msg_area, contact_info)

    if not msg.text.isspace() and msg:
        if contact_info.current_contact.username == sender_username:
            display_message(msg_area, msg)
        msg.set_message_id(message_id)
        contact_info.save_message(msg, sender_contact)
        contact_info.persist()

'''
URL para alterar o status de uma mensagem
data:
    {'received' : bool
    'read': bool}
'''
@app.route('/api/messages/<message_id>', methods=['PUT'])
def update_message_status_from_request(message_id):
    try:
        message_id = int(message_id)
        received = request.form['received'] #Alterar para ser opcional os campos
        read = request.form['read']
        #Escrever no arquivo e só depois enviar a resposta
        
        response = make_response(jsonify({"success": True}), 201)

    except Exception as e:
        print(e)
        response = make_response(jsonify({"success": False}), 500)
    
    return response


'''
Função main do programa
Possui uma variável global para ser acessada pelo Flask
'''
def main():
    #Começa o Servidor
    #print(" Go to http://127.0.0.1:5000/api/messages to see the request result")
    #app.run(host='0.0.0.0', port=80) #Escolher outra porta
    port = int(sys.argv[1])

    server_thread = threading.Thread(target=app.run, kwargs={'port': port}, daemon=True)
    server_thread.start()

    #User Interface
    global window

    window = Tk()
    window.withdraw()
 
    login_screen(window, port)
    #setup_chat(window, 'user1', '') #Para rodar sem login

    window.mainloop()


if __name__ == "__main__":
    main()