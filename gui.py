from data_base import read_data
import webbrowser
import subprocess
import os

from tkinter import *
from tkinter import ttk

df = read_data()

class App:
    def __init__(self):
        self.root = Tk()

        self.root.iconbitmap(os.path.abspath('img/Clariant.ico'))
        self.root.title('lot inventory')
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
        self.dropdown_menu.bind('<<ComboboxSelected>>', lambda _: (self.search.focus_set(), self.search.event_generate('<Return>')))
        #s
        self.add_execute = Button(self.root, text='execute', command=lambda: self.__execute(), width=8)
        self.add_execute.grid(row=2, sticky='s')

        self.update_list = Button(self.root, text='update', command=lambda: self.__update(), width=8)
        self.update_list.grid(row=3, sticky='n')

        self.data_frame = None

    def __searching(self):
        def filter(*args):
            self.list_box.delete(0, END)
            query = self.search.get()
            selected = self.dropdown_menu.get()

            self.data_frame = df

            if selected == 'expired':
                self.data_frame = df[df['expired'] == True]
            elif selected == 'in use':
                self.data_frame = df[df['expired'] == False]

            if ',' in query:
                query = query.split(',')
                query = set(map(lambda s: s.strip(), query))
                intersection = query & set(self.data_frame['standard'].unique())
                self.list_box.insert(END, *intersection)
            else:
                for lot in self.data_frame['standard'].unique():
                    if lot.startswith(query):
                        self.list_box.insert(END, lot)

        self.search.bind('<Return>', filter)
        self.search.bind('<KeyRelease>', filter)

    def __execute(self):
        selected_indices = self.list_box.curselection()
        selected_lots = [self.list_box.get(i) for i in selected_indices]
        print(selected_lots)
        self.data_frame[self.data_frame['standard'].isin(selected_lots)].drop('expired', axis=1).to_csv('temp_data_frame.txt', index=False)

        f = open('temp_data_frame.txt', 'r')
        output = open('output.txt', 'w')
        f.readline()

        for line in f.readlines():
            token = line.split(',')
            token[1] = f'lot: {token[1]}'
            token[2] = f'exp: {token[2]}'.replace('\n', '')
            print(' '.join(token), file=output)

        f.close()
        output.close()
        webbrowser.open('output.txt')

    def __update(self):
        subprocess.run([r'C:\Windows\System32\notepad.exe', r'data\inventory.txt'])
        global df
        df = read_data()

    def run(self):
        self.root.mainloop()
