#!/usr/bin/python

# tutorial: https://likegeeks.com/python-gui-examples-tkinter-tutorial/

from tkinter import *
from tkinter import scrolledtext
from message import *
from functools import partial


def main() :

    window = Tk()

    window.title("Omicron Messenger")
    window.geometry('600x400')

    lbl = Label(window, text="PP", font=("Arial Bold", 50))
    lbl.grid(column=0, row=0, sticky="ew")


    # Messages

    msg_area = scrolledtext.ScrolledText(window,width=40,height=10,spacing1=4)
    msg_area.grid(column=1, row=1, columnspan=2, sticky="ew")
    msg_area.tag_configure('tag-center', justify='right')
    msg_area.tag_configure('tag-left', justify='left')
    msg_area.tag_configure('tag-right', justify='right')

    def clicked():
        print("O botão foi clicado!")

    txt = Entry(window,width=msg_area['width'])
    txt.grid(column=1, row=2, sticky="ew")
    txt.bind("<Return>", (lambda event: sendMessage()))

    def display_message(msg):
        if not msg.isspace():
            label = Label(msg_area, text=msg, background='#d0ffff', justify='right', padx=7, pady=7)
            msg_area.insert('end', '\n ', 'tag-right') # space to move Label to the right 
            msg_area.window_create('end', window=label)
            msg_area.yview_moveto( 1 )

    def sendMessage():
        msg = formatToDisplayV2(txt.get())
        display_message(msg)
        contacts[current_contact].append(msg)
        txt.delete(0, 'end')

    btn = Button(window, text="Send!", command=sendMessage)
    btn.grid(column=2, row=2, sticky="ew")

    # Contact Area

    contact_area = scrolledtext.ScrolledText(window,width=10,height=10)
    contact_area.grid(column=0, row=1, sticky="ew")
    contact_area.tag_configure('tag-center', justify='right')
    contact_area.tag_configure('tag-left', justify='left')
    contact_area.tag_configure('tag-right', justify='right')

    current_contact = "João Pedro"

    def change_current_conversation(contact_name):
        lbl['text'] = contact_name
        current_contact = contact_name
        msg_area.delete("1.0",END)
        for msg in contacts[contact_name]:
            display_message(msg)

    contacts = {
        "João Pedro" : [],
        "Maria" : [],
        "Pai" : [],
        "Mãe" : [],
        "Tio Julio" : [],
        "Marcelo" : [],
        "Bruna" : []
    }

    lbl = Label(window, text=next(iter(contacts)), font=("Arial Bold", 20))
    lbl.grid(column=1, row=0, sticky="s")

    for c in contacts:
        action_with_arg = partial(change_current_conversation, c)
        button = Button(window, width=contact_area["width"]-3, text=c,command= action_with_arg)
        contact_area.window_create('end', window=button)

    window.mainloop()


if __name__ == "__main__":
    main()