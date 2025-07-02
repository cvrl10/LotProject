from data_base import df

from tkinter import *
from tkinter import ttk

class App:
    def __init__(self):
        self.root = Tk()

        self.root.geometry('300x200')
        self.root.resizable(False, False)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        self.root.rowconfigure(3, weight=1)

        self.search = ttk.Entry(self.root)
        self.search.grid(row=0, sticky='')

        self.list_box = Listbox(self.root, height=5, selectmode='multiple')
        self.list_box.grid(row=1)

        self.__searching()


        self.add_lot = Button(self.root, text='add')
        self.add_lot.grid(row=2, sticky='s')

        self.update_list = Button(self.root, text='update')
        self.update_list.grid(row=3, sticky='n')

    def __search(self):
        programmatic_modification_of_txt = StringVar()
        self.search.config(textvariable=programmatic_modification_of_txt)

        def filter(*args):
            query = programmatic_modification_of_txt.get()
            print(f'searching for: {query}')

        programmatic_modification_of_txt.trace('w', filter)
        self.search.bind('<Return>', filter)

    def __searching(self):
        def filter(*args):
            query = self.search.get()
            self.list_box.delete(0, END)
            for lot in df['standard'].unique():
                if lot.startswith(query):
                    self.list_box.insert(END, lot)

        self.search.bind('<Return>', filter)
        self.search.bind('<KeyRelease>', filter)


    def run(self):
        self.root.mainloop()
