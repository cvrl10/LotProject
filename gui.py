from data_base import df
import webbrowser

from tkinter import *
from tkinter import ttk

print(TkVersion)

class App:
    def __init__(self):
        self.root = Tk()

        self.root.geometry('325x250')
        self.root.resizable(False, False)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        self.root.rowconfigure(3, weight=1)

        self.frame = Frame(self.root)
        self.frame.grid(row=0, sticky='nsew')

        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)
        self.frame.columnconfigure(3, weight=1)
        self.frame.columnconfigure(4, weight=1)
        self.frame.columnconfigure(5, weight=1)

        self.search = ttk.Entry(self.frame)
        #self.search.grid(row=0, sticky='')
        self.search.grid(column=2, row=1, sticky='w', columnspan=4)

        self.dropdown_menu = ttk.Combobox(self.frame, state='readonly', values=['in use', 'expired', 'all'], width=7)
        self.dropdown_menu.set('in use')


        #self.dropdown_menu.grid(row=0)
        self.dropdown_menu.grid(column=0, row=1, sticky='e', columnspan=2)

        self.list_box = Listbox(self.root, height=5, selectmode='multiple', exportselection=False)
        self.list_box.grid(row=1)

        self.__searching()
        self.dropdown_menu.bind('<<ComboboxSelected>>', lambda _: self.search.event_generate('<Return>', when='head'))

        self.add_execute = Button(self.root, text='execute', command=lambda: self.__execute())
        self.add_execute.grid(row=2, sticky='s')

        self.update_list = Button(self.root, text='update')
        self.update_list.grid(row=3, sticky='n')

        self.data_frame = None

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
            self.list_box.delete(0, END)
            query = self.search.get()
            selected = self.dropdown_menu.get()

            self.data_frame = df

            if selected == 'expired':
                #print('expired')
                self.data_frame = df[df['expired'] == True]
                #print(f'{self.data_frame.to_string()}\n')
            elif selected == 'in use':
                self.data_frame = df[df['expired'] == False]
                #print('in use')
                #print(f'{self.data_frame.to_string()}\n')

            if ',' in query:
                query = query.split(',')
                query = set(map(lambda s: s.strip(), query))
                intersection = query & set(self.data_frame['standard'].unique())
                self.list_box.insert(END, *intersection)
            else:
                for lot in self.data_frame['standard'].unique():
                    if lot.startswith(query):
                        self.list_box.insert(END, lot)

            print('I firering this event')

        self.search.bind('<Return>', filter)
        self.search.bind('<KeyRelease>', filter)

    def __execute(self):
        selected_indices = self.list_box.curselection()
        selected_lots = [self.list_box.get(i) for i in selected_indices]
        print(selected_lots)
        self.data_frame[self.data_frame['standard'].isin(selected_lots)].to_csv('output.txt')
        #print('dataframe')
        #print(self.data_frame[self.data_frame['standard'].isin(selected_lots)])
        webbrowser.open('output.txt')

        #also fix the it to updated when the comboboxchange



    def run(self):
        self.root.mainloop()
