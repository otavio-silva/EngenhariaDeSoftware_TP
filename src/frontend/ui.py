#!/usr/bin/python

# tutorial: https://likegeeks.com/python-gui-examples-tkinter-tutorial/

from tkinter import *
from tkinter import scrolledtext


def main() :

    window = Tk()

    window.title("Welcome to LikeGeeks app")
    window.geometry('600x400')

    lbl = Label(window, text="PP", font=("Arial Bold", 50))
    lbl.grid(column=0, row=0)

    lbl = Label(window, text="Messages", font=("Arial Bold", 20))
    lbl.grid(column=1, row=0)

    msg_area = scrolledtext.ScrolledText(window,width=40,height=10)
    msg_area.grid(column=1, row=1)
    msg_area.tag_configure('tag-center', justify='right')
    msg_area.tag_configure('tag-left', justify='left')
    msg_area.tag_configure('tag-right', justify='right')

    def clicked():
        print("O botão foi clicado!")
    btn = Button(window, text="Click Me", command=clicked)
    btn.grid(column=0, row=1)

    btn = Button(window, text="Click Me too!")
    btn.grid(column=0, row=2)

    txt = Entry(window,width=40)
    txt.grid(column=1, row=2)

    def format(message):
        x=30 
        split = message.split()
        fmtMsg = []
        index = 0
        count = 0
        line = " "
        print("Split:")
        print(split)
        for word in split:
            count += len(word)
            if count <= x :
                line += " " + word
            else:
                print("Line: " + line)
                fmtMsg.append(line)
                line = " "
                index+=1
                count=0
        fmtMsg.append(line)
        print("Formated: ")
        print(fmtMsg)
        return fmtMsg


    def sendMessage():
        txtList = format(txt.get())
    
        for t in txtList:
            label = Label(msg_area, text=t, background='#d0ffff', justify='left', padx=10, pady=0)
            msg_area.insert('end', '\n ', 'tag-right') # space to move Label to the right 
            msg_area.window_create('end', window=label)
        txt.delete(0, 'end')

    btn = Button(window, text="Send!", command=sendMessage)
    btn.grid(column=2, row=2)

    window.mainloop()


if __name__ == "__main__":
    main()