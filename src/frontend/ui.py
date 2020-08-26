#!/usr/bin/python

# tutorial: https://likegeeks.com/python-gui-examples-tkinter-tutorial/

from tkinter import *
from tkinter import scrolledtext


def main() :

    window = Tk()

    window.title("Welcome to LikeGeeks app")
    window.geometry('800x600')

    lbl = Label(window, text="PP", font=("Arial Bold", 50))
    lbl.grid(column=0, row=0)

    lbl = Label(window, text="Messages", font=("Arial Bold", 20))
    lbl.grid(column=1, row=0)

    msg_area = scrolledtext.ScrolledText(window,width=40,height=10)
    msg_area.grid(column=1, row=1)

    def clicked():
        print("O botão foi clicado!")
    btn = Button(window, text="Click Me", command=clicked)
    btn.grid(column=0, row=1)

    btn = Button(window, text="Click Me too!")
    btn.grid(column=0, row=2)

    txt = Entry(window,width=40)
    txt.grid(column=1, row=2)

    def sendMessage():
        msg_area.insert(INSERT,'\n' + txt.get())

    btn = Button(window, text="Send!", command=sendMessage)
    btn.grid(column=2, row=2)

    window.mainloop()


if __name__ == "__main__":
    main()