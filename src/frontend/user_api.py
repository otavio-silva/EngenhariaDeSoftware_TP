import flask
from flask import request, jsonify, make_response
import threading
from ui_lib import *
from contact_info import *
from rest_requests import *


#TODO Criação de usuário
#TODO enviar mensagens
#TODO Double tick
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
        response = make_response(jsonify({"success": "Mensagem enviada com sucesso"}), 201)

    except Exception as e:
        print(e)
        response = make_response(jsonify({"error": "Algo deu errado no processamento da mensagem"}), 500)
    
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
        contact_info.save_message(msg, sender_contact)
        contact_info.persist()

'''
Função main do programa
Possui uma variável global para ser acessada pelo Flask
'''
def main():
    #Começa o Servidor
    #print(" Go to http://127.0.0.1:5000/api/messages to see the request result")
    server_thread = threading.Thread(target=app.run, args=tuple(), daemon=True)
    server_thread.start()

    #User Interface
    global window

    window = Tk()
    window.withdraw()
 
    login_screen(window)
    #setup_chat(window, 'user1', '')

    window.mainloop()

    '''
    # Dummy contact info => Variável usada por outras funções
    global contact_info
    contact_info = ContactInfo()

    window.title("Omicron Messenger")
    window.geometry('600x400')

    #Tela de Login

    # Profile picture placeholder
    lbl = Label(window, text="PP", font=("Arial Bold", 50))
    lbl.grid(column=0, row=0, sticky="ew")

    # Message area where the messages appear
    global msg_area
    msg_area = create_msg_area(window) 
    # Form to write messages
    msg_send_form = create_msg_send_form(window,msg_area,contact_info)
    # Button to send the message 
    send_text_action = create_send_msg_button(window,msg_area,msg_send_form,contact_info)
    # Form to receive messages (will remove it once the rest method calls the receive_message function)
    #msg_receive_form = create_msg_receive_form(window,msg_area,contact_info)
    # Button to receive the message 
    #receive_text_action = create_receive_msg_button(window,msg_area,msg_receive_form,contact_info)
    # Contact Area
    #contact_area = create_contact_area(window)
    #current_contact_lbl = Label(window, text=contact_info.current_contact.name, font=("Arial Bold", 20))
    #current_contact_lbl.grid(column=1, row=0, sticky="s")
    #update_contact_area(contact_area, contact_info, window, msg_area, current_contact_lbl)
    # Contact Area
    update_contact_area(window, msg_area, contact_info)
    
    
    # make the top right close button minimize (iconify) the main window
    on_close_args = partial(on_close, window,contact_info)
    window.protocol("WM_DELETE_WINDOW", on_close_args)
    

    #Isso gera erro no uso de thread separada para o Flask
    #while True: 
    #    window.after(2)
    #    window.update()
    
    window.mainloop()
    '''

if __name__ == "__main__":
    main()