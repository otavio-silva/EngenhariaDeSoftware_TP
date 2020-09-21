from tkinter import *
from tkinter import scrolledtext
from message import *
from contact import *
from contact_info import *
from functools import partial
from rest_requests import *

'''
Funções para que o Flask possa modificar a UI
Essas variáveis só são criadas pela setup_chat
'''
def get_contact_info():
    return contact_info
def get_msg_area():
    return msg_area

'''
Função que cria a tela principal.
Também preenche as variáveis globais msg_area e contact_info
Recebe o username
'''
def setup_chat(window, username, access_token, port):
    global msg_area
    global contact_info
    # Dummy contact info => Variável usada por outras funções
    contact_info = ContactInfo(username, access_token)
    window.deiconify() #Mostra a window que estava escondida
    window.title("Omicron Messenger")
    window.geometry('600x400')
    # Profile picture placeholder
    lbl = Label(window, text="PP", font=("Arial Bold", 50))
    lbl.grid(column=0, row=0, sticky="ew")
    # Message area where the messages appear
    msg_area = create_msg_area(window) 
    # Form to write messages
    msg_send_form = create_msg_send_form(window,msg_area,contact_info,access_token)
    # Button to send the message 
    send_text_action = create_send_msg_button(window,msg_area,msg_send_form,contact_info,access_token)
    # Contact Area
    update_contact_area(window, msg_area, contact_info)
    #Display current messages
    msg_area.delete("1.0",END)
    for msg in contact_info.current_contact.messages:
        display_message(msg_area,msg)

    send_keep_active(access_token, port, window)
    # make the top right close button minimize (iconify) the main window
    on_close_args = partial(on_close, window,contact_info)
    window.protocol("WM_DELETE_WINDOW", on_close_args)

'''
Função recursiva com timer
Envia uma requisição a cada 4 segundos
'''
def send_keep_active(access_token, port, window):
    try:
        req = keep_active_request(port, access_token)
    except:
        print("Algo deu errado no keep active")

    window.after(4000, send_keep_active, access_token, port, window)  


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

def create_msg_send_form(window,msg_area,contact_info, access_token):
    msg_send_form = Entry(window,width=msg_area['width'])
    msg_send_form.grid(column=1, row=2, sticky="ew")
    msg_send_form.bind("<Return>", (lambda event: send_message(msg_area,msg_send_form,contact_info,access_token)))
    return msg_send_form

def create_send_msg_button(window,msg_area,msg_form,contact_info,access_token):
    send_text_action = partial(send_message,msg_area,msg_form,contact_info,access_token)
    send_text_button = Button(window, text=" > ", command=send_text_action)
    send_text_button.grid(column=2, row=2, sticky="ew")
    return send_text_action
'''
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
'''

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

def send_message(msg_area,msg_form, contact_info : ContactInfo, access_token):
    #Tenta enviar para o backend, caso dê errado retorna
    msg : Message = Message(msg_form.get(),MessageOrigin.SENT)
    if not msg.text.isspace() and msg:
        try:
            req = send_message_request(contact_info.current_contact.username, msg.text, access_token)
            print(req.json())
            message_id = req.json()['created_id']
        except Exception as e:
            print(e)
            return  
        msg.set_message_id(message_id)
        display_message(msg_area,msg)
        msg_form.delete(0, 'end')
        contact_info.save_message_current(msg)
        contact_info.persist()
'''
def receive_message(msg_area,msg_form, contact_info : ContactInfo):
    msg : Message = Message(msg_form.get(),MessageOrigin.RECEIVED)
    if not msg.text.isspace() and msg:  
        display_message(msg_area,msg)
        msg_form.delete(0, 'end')
        contact_info.save_message_current(msg)
        contact_info.persist()
'''

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

#Funções para lidar com login de usuário

'''
Função que cria a tela de login
Pega username e token de autenticação
Pode redirecionar para tela de criação de usuário
'''
def login_screen(window, port):
    login = Toplevel()
    login.title("Login") 
    login.geometry('600x400')

    pls = Label(login, text = "Faça seu login", justify = CENTER, font = "Helvetica 14 bold")
    pls.place(relheight = 0.15, relx = 0.2, rely = 0.07)

    label_username = Label(login, text = "Username: ", font = "Helvetica 12")   
    label_username.place(relheight = 0.2, relx = 0.1, rely = 0.2)  
    entry_username = Entry(login, font = "Helvetica 14") 
    entry_username.place(relwidth = 0.4, relheight = 0.12, relx = 0.35, rely = 0.2)
    entry_username.focus()

    label_password = Label(login, text = "Senha: ", font = "Helvetica 12")   
    label_password.place(relheight = 0.2, relx = 0.1, rely = 0.4)
    entry_password = Entry(login, font = "Helvetica 14")
    entry_password.place(relwidth = 0.4, relheight = 0.12, relx = 0.35, rely = 0.4)

    #Será usada pelo authenticate_user para falar que um erro ocorreu
    label_error = Label(login, text = "Um erro ocorreu ! Tente novamente.", font = "Helvetica 12")

    login_action = partial(authenticate_user, entry_username , entry_password, label_error, window, login, port)
    go = Button(login, text = "LOGAR", font = "Helvetica 14 bold", command = login_action)
    go.place(relx = 0.4, rely = 0.55)

    create_user_action = partial(new_user_window)
    create_user_button = Button(login, text = "CRIAR NOVO USUÁRIO", font = "Helvetica 16 bold", command = create_user_action)
    create_user_button.place(relx = 0.4, rely = 0.7)

    on_close_login_action = partial(on_close_login, window, login)
    login.protocol("WM_DELETE_WINDOW", on_close_login_action)


def on_close_login(window, login):
    print("Fechando...")
    login.destroy()
    window.destroy()

'''
Função chamada ao clicar no botão de Logar
Caso a autenticação dê errado, não vai para frente
Caso dê certo, chama a função de trocar de janela
'''
def authenticate_user(username_form, password_form, label_error, window, login, port):
    username = username_form.get()
    password = password_form.get()
    try:
        req = authenticate_user_request(username, password)
        access_token = req.json()['token']
    except Exception as e:
        label_error.place(relx = 0.4, rely = 0.6)
        print(e)
        return
    login_to_chat(window, login, username, access_token, port)

'''
Função que troca de janelas do login para o chat
'''
def login_to_chat(window, login, username, access_token, port):
    login.destroy() 
    setup_chat(window, username, access_token, port)

#Funções para lidar com criação de usuário

'''
Função que abre janela para criar novo usuário
'''
def new_user_window():
    new_user_window = Toplevel()
    new_user_window.title("Novo Usuário")
    new_user_window.geometry('600x400')

    pls = Label(new_user_window, text = "Preencha seus dados:", justify = CENTER, font = "Helvetica 14 bold")
    pls.place(relheight = 0.15, relx = 0.2, rely = 0.07)

    label_username = Label(new_user_window, text = "Username*: ", font = "Helvetica 12")   
    label_username.place(relheight = 0.2, relx = 0.1, rely = 0.15)  
    entry_username = Entry(new_user_window, font = "Helvetica 14") 
    entry_username.place(relwidth = 0.4, relheight = 0.12, relx = 0.35, rely = 0.2)
    entry_username.focus()

    label_password = Label(new_user_window, text = "Senha*: ", font = "Helvetica 12")   
    label_password.place(relheight = 0.2, relx = 0.1, rely = 0.35)
    entry_password = Entry(new_user_window, font = "Helvetica 14")
    entry_password.place(relwidth = 0.4, relheight = 0.12, relx = 0.35, rely = 0.4)

    label_first_name = Label(new_user_window, text = "Primeiro Nome: ", font = "Helvetica 12")   
    label_first_name.place(relheight = 0.2, relx = 0.1, rely = 0.55)
    entry_first_name = Entry(new_user_window, font = "Helvetica 14")
    entry_first_name.place(relwidth = 0.4, relheight = 0.12, relx = 0.35, rely = 0.6)

    label_last_name = Label(new_user_window, text = "Último Nome: ", font = "Helvetica 12")   
    label_last_name.place(relheight = 0.2, relx = 0.1, rely = 0.75)
    entry_last_name = Entry(new_user_window, font = "Helvetica 14")
    entry_last_name.place(relwidth = 0.4, relheight = 0.12, relx = 0.35, rely = 0.8)

    create_action = partial(try_create_new_user, entry_username, entry_password, entry_first_name, entry_last_name, new_user_window)
    go = Button(new_user_window, text = "CRIAR", font = "Helvetica 14 bold", command = create_action)
    go.place(relx = 0.8, rely = 0.5)


'''
Função que tenta criar novo usuário
'''
def try_create_new_user(username_form, password_form, first_name_form, last_name_form, new_user_window):
    username = username_form.get()
    password = password_form.get()
    first_name = first_name_form.get()
    last_name = last_name_form.get()
    try:
        req = create_user_request(username, password, first_name, last_name)
        if not 'id' in req.json() or not 'username' in req.json():
            raise Exception
    except Exception as e:
        print(e)
        return
    
    print('Usuário Criado')
    new_user_window.destroy()



