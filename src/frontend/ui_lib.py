from tkinter import *
from tkinter import scrolledtext
from message import *
from contact import *
from contact_info import *
from functools import partial
from rest_requests import *

'''
Função que cria a tela principal.
Também cria as variáveis globais msg_area e contact_info
Recebe o username
'''
def setup_chat(window, username):
    # Dummy contact info => Variável usada por outras funções
    contact_info = ContactInfo()

    window.title("Omicron Messenger")
    window.geometry('600x400')
    # Profile picture placeholder
    lbl = Label(window, text="PP", font=("Arial Bold", 50))
    lbl.grid(column=0, row=0, sticky="ew")
    # Message area where the messages appear
    msg_area = create_msg_area(window) 
    # Form to write messages
    msg_send_form = create_msg_send_form(window,msg_area,contact_info)
    # Button to send the message 
    send_text_action = create_send_msg_button(window,msg_area,msg_send_form,contact_info)
    # Contact Area
    update_contact_area(window, msg_area, contact_info)

    # make the top right close button minimize (iconify) the main window
    on_close_args = partial(on_close, window,contact_info)
    window.protocol("WM_DELETE_WINDOW", on_close_args)

    return contact_info, msg_area


def create_contact_area(window):
    contact_area = scrolledtext.ScrolledText(window,width=15,height=10)
    contact_area.grid(column=0, row=1, sticky="ew")
    return contact_area

def create_msg_area(window):
    msg_area = scrolledtext.ScrolledText(window,width=40,height=10,spacing1=4)
    msg_area.grid(column=1, row=1, columnspan=2, sticky="ew")
    msg_area.tag_configure('tag-center', justify='right')
    msg_area.tag_configure('tag-left', justify='left')
    msg_area.tag_configure('tag-right', justify='right')
    return msg_area

def create_msg_send_form(window,msg_area,contact_info):
    msg_send_form = Entry(window,width=msg_area['width'])
    msg_send_form.grid(column=1, row=2, sticky="ew")
    msg_send_form.bind("<Return>", (lambda event: send_message(msg_area,msg_send_form,contact_info)))
    return msg_send_form

def create_send_msg_button(window,msg_area,msg_form,contact_info):
    send_text_action = partial(send_message,msg_area,msg_form,contact_info)
    send_text_button = Button(window, text=" > ", command=send_text_action)
    send_text_button.grid(column=2, row=2, sticky="ew")
    return send_text_action

def create_msg_receive_form(window,msg_area,contact_info):
    msg_receive_form = Entry(window,width=msg_area['width'])
    msg_receive_form.grid(column=1, row=3, sticky="ew")
    msg_receive_form.bind("<Return>", (lambda event: receive_message(msg_area,msg_receive_form,contact_info)))
    return msg_receive_form

def create_receive_msg_button(window,msg_area,msg_form,contact_info):
    receive_text_action = partial(receive_message,msg_area,msg_form,contact_info)
    receive_text_button = Button(window, text=" < ", command=receive_text_action)
    receive_text_button.grid(column=2, row=3, sticky="ew")
    return receive_text_action

def display_message(msg_area,msg : str):
    txt = msg.format_to_display()
    if msg.origin == MessageOrigin.SENT:
        justify = "right" 
        tag = "tag-right"
        color = "#d0ffff"
    else:
        justify = "left" 
        tag = "tag-left"
        color = "#ffeda2"
    print("Message: " + txt)
    if not txt.isspace() and txt:  
        label = Label(msg_area, text=txt, background=color, justify=justify, padx=7, pady=7)
        msg_area.insert('end', '\n ', tag) # space to move Label to the right 
        msg_area.window_create('end', window=label)
        msg_area.yview_moveto( 1 )

def send_message(msg_area,msg_form, contact_info : ContactInfo):
    #Tenta enviar para o backend, caso dê errado retorna

    msg : Message = Message(msg_form.get(),MessageOrigin.SENT)
    if not msg.text.isspace() and msg:  
        display_message(msg_area,msg)
        msg_form.delete(0, 'end')
        contact_info.save_message_current(msg)
        contact_info.persist()

def receive_message(msg_area,msg_form, contact_info : ContactInfo):
    msg : Message = Message(msg_form.get(),MessageOrigin.RECEIVED)
    if not msg.text.isspace() and msg:  
        display_message(msg_area,msg)
        msg_form.delete(0, 'end')
        contact_info.save_message_current(msg)
        contact_info.persist()

def change_current_conversation(msg_area,contact,contact_info,current_contact_lbl):
    current_contact_lbl['text'] = contact.name
    #contact_info.current_contact = contact.username
    contact_info.current_contact = contact
    msg_area.delete("1.0",END)
    for msg in contact.messages:
        display_message(msg_area,msg)

def update_contact_area(window, msg_area, contact_info):
    contact_area = create_contact_area(window)
    current_contact_lbl = Label(window, text=contact_info.current_contact.name, font=("Arial Bold", 20))
    current_contact_lbl.grid(column=1, row=0, sticky="s")
    contact_area.delete("1.0",END)
    for c in contact_info.contacts:
        contact = contact_info.contacts[c]
        action_with_arg = partial(change_current_conversation, msg_area,contact,contact_info,current_contact_lbl)
        button = Button(window, width=contact_area["width"]-3, text=contact.name,command= action_with_arg)
        contact_area.window_create('end', window=button)

def on_close(window,contact_info):
        print("Fechando...")
        window.destroy()
        contact_info.persist()


#Funções para lidar com criação de usuário


#Funções para lidar com login de usuário
