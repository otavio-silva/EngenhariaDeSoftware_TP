

from tkinter import *
from tkinter import scrolledtext

root = Tk()
#text_widget = tk.Text()
text_widget = scrolledtext.ScrolledText()
# text_widget.pack(fill='both', expand=True)

label1 = Label(text_widget, text="Hello\nWorld!!!", background='#d0ffff', justify='left', padx=10, pady=5)
label2 = Label(text_widget, text="Hello\nWorld!!!", background='#ffffd0', justify='left', padx=10, pady=5)
label3 = Label(text_widget, text="Hello\nWorld!!!", background='#d0ffff', justify='left', padx=10, pady=5)

text_widget.tag_configure('tag-left', justify='left')
text_widget.tag_configure('tag-right', justify='right')


text_widget.insert('end', '\n')
text_widget.window_create('end', window=label1)

text_widget.insert('end', '\n ', 'tag-right') # space to move Label to the right 
text_widget.window_create('end', window=label2)

text_widget.insert('end', '\n')
text_widget.window_create('end', window=label3)

root.mainloop()