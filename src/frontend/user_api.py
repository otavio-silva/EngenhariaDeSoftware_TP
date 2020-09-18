import flask
from flask import request, jsonify, make_response
import threading
from ui_lib import *
from contact_info import *
from rest_requests import *

app = flask.Flask(__name__)
#app.config["DEBUG"] = True

'''
@app.route('/', methods=['GET'])
def home():
    return """<h1>Distant Reading Archive</h1><p>A prototype API for distant reading of science fiction novels.</p>"""
'''

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
        created_at = request.form['created_at']
        #Escrever no arquivo e só depois enviar a resposta
        receive_message_from_server(message_id, sender_username, message_content)
        response = make_response(jsonify({"success": "Mensagem enviada com sucesso"}), 201)

    except Exception as e:
        print(e)
        response = make_response(jsonify({"error": "Algo deu errado no processamento da mensagem"}), 500)
    
    return response


'''
Função chamada pela receive_message_from_request para efetivar o recebimento de uma mensagem
Requer que contact_info e msg_area sejam globais
'''
def receive_message_from_server(message_id, sender_username, message_content):
    msg : Message = Message(message_content, MessageOrigin.RECEIVED)
    sender_contact = contact_info.get_contact_from_username(sender_username)
    #Cria novo contato, consultando seu nome no servidor
    #TODO consultar servidor para saber o nome o usuario
    #TODO corrigir bug nesta parte
    if sender_contact == None:
        contact_info.create_contact(sender_username, sender_username)
        sender_contact = contact_info.get_contact_from_username(sender_username)

    if not msg.text.isspace() and msg:
        display_message(msg_area, msg)
        contact_info.save_message(msg, sender_contact)
        contact_info.persist()



def main():
    #Começa o Servidor
    #print(" Go to http://127.0.0.1:5000/api/messages to see the request result")
    server_thread = threading.Thread(target=app.run, args=tuple(), daemon=True)
    server_thread.start()

    #User Interface

    # Dummy contact info => Variável usada por outras funções
    global contact_info
    contact_info = ContactInfo()

    window = Tk()
    window.title("Omicron Messenger")
    window.geometry('600x400')

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
    contact_area = create_contact_area(window)
    current_contact_lbl = Label(window, text=contact_info.current_contact.name, font=("Arial Bold", 20))
    current_contact_lbl.grid(column=1, row=0, sticky="s")
    for c in contact_info.contacts:
        contact = contact_info.contacts[c]
        action_with_arg = partial(change_current_conversation, msg_area,contact,contact_info,current_contact_lbl)
        button = Button(window, width=contact_area["width"]-3, text=contact.name,command= action_with_arg)
        contact_area.window_create('end', window=button)
    
    # make the top right close button minimize (iconify) the main window
    on_close_args = partial(on_close, window,contact_info)
    window.protocol("WM_DELETE_WINDOW", on_close_args)

    #Isso gera erro na thread
    #while True: 
    #    window.after(2)
    #    window.update()

    window.mainloop()

if __name__ == "__main__":
    main()