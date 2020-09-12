#!/usr/bin/python

# tutorial: https://likegeeks.com/python-gui-examples-tkinter-tutorial/

from tkinter import *
from tkinter import scrolledtext
from message import *
from contact import *
from contact_info import *
from functools import partial


def formatToDisplay(message, max_chars=25):
    count = 0
    formatted_msg = ""
    for word in message.split():
        count += len(word)
        formatted_msg += " " + word
        if count > max_chars :
            formatted_msg += "\n"
            count=0
    return formatted_msg


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

def display_message(msg_area,msg,tag = "tag-right"):
    if not msg.isspace() and msg:  
        label = Label(msg_area, text=msg, background='#d0ffff', justify='right', padx=7, pady=7)
        msg_area.insert('end', '\n ', tag) # space to move Label to the right 
        msg_area.window_create('end', window=label)
        msg_area.yview_moveto( 1 )

def sendMessage(msg_area,msg_form, contact_info : ContactInfo):
    msg = formatToDisplay(msg_form.get())
    if not msg.isspace() and msg:  
        display_message(msg_area,msg,"tag-right")
        print("Appending in: " + contact_info.current_contact)
        contact_info.save_message_sent_to_current(msg)
        msg_form.delete(0, 'end')

def receiveMessage(contact_info : ContactInfo):
    msg = formatToDisplay(msg_form.get())
    if not msg.isspace() and msg:  
        display_message(msg,"tag-left")
        print("Appending in: " + contact_info.current_contact)
        contacts[contact_info.current_contact].append(msg)
        msg_form.delete(0, 'end')

def change_current_conversation(msg_area,current_contact_lbl,contact_name : str,contact_info : ContactInfo):
    current_contact_lbl['text'] = contact_name
    contact_info.current_contact = contact_name
    msg_area.delete("1.0",END)
    for msg in contact_info.contacts[contact_name].messages:
        display_message(msg_area,msg)

def main() :

    # Dummy contact info

    contact_info = ContactInfo({
        Contact("joao_pedro23","João Pedro"),
        Contact("maria_aaaa","Maria"),
        Contact("melhorPai123","Pai"),
        Contact("motherOfAll","Mãeo"),
        Contact("juliao_tiozao","Tio Julio"),
        Contact("my_cello","Marcelo"),
        Contact("buhbuh54","Bruna")
    })

    window = Tk()
    window.title("Omicron Messenger")
    window.geometry('600x400')

    # Profile picture placeholder

    lbl = Label(window, text="PP", font=("Arial Bold", 50))
    lbl.grid(column=0, row=0, sticky="ew")


    # Message area where the messages appear
    msg_area = create_msg_area(window) 

    # Form to write messages
    msg_form = Entry(window,width=msg_area['width'])
    msg_form.grid(column=1, row=2, sticky="ew")
    msg_form.bind("<Return>", (lambda event: sendMessage(msg_area,msg_form,contact_info)))

    send_text_action = partial(sendMessage,msg_area,msg_form,contact_info)
    btn = Button(window, text="Send!", command=send_text_action)
    btn.grid(column=2, row=2, sticky="ew")

    # Contact Area

    contact_area = create_contact_area(window)

    current_contact_lbl = Label(window, text=contact_info.current_contact, font=("Arial Bold", 20))
    current_contact_lbl.grid(column=1, row=0, sticky="s")

    for c in contact_info.contacts:
        action_with_arg = partial(change_current_conversation, msg_area,current_contact_lbl, c, contact_info)
        button = Button(window, width=contact_area["width"]-3, text=c,command= action_with_arg)
        contact_area.window_create('end', window=button)

    window.mainloop()


if __name__ == "__main__":
    main()