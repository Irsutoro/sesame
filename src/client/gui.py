import tkinter as tk
from tkinter import messagebox
from client import Client
import pyperclip

class GUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Sesame')
        self.root.pack_propagate(True)
        self.root.resizable(False, False)
        self.client = Client()

    def reset_root(self):
        for widget in self.root.pack_slaves():
            widget.destroy()

    def auth_view(self):
        self.reset_root()
        container = tk.Frame(master=self.root, height=100, width=300)
        container.pack_propagate(False)
        container.pack()
        button_login = tk.Button(master=container, text='Zaloguj', command=self.login_view)
        button_register = tk.Button(master=container, text='Zarejestruj', command=self.register_view)
        button_login.pack(side=tk.LEFT, expand=True)
        button_register.pack(side=tk.LEFT, expand=True)

    def login_view(self):
        self.reset_root()
        container = tk.Frame(master=self.root, height=200, width=300)
        container.pack_propagate(False)
        container.pack()

        frame_login = tk.Frame(master=container)
        frame_password = tk.Frame(master=container)
        frame_button = tk.Frame(master=container)

        frame_login.pack(expand=True)
        frame_password.pack(expand=True)
        frame_button.pack(expand=True)

        label_login = tk.Label(master=frame_login, text='Nazwa użytkownika')
        label_login.pack(side=tk.LEFT)
        entry_login = tk.Entry(master=frame_login)
        entry_login.pack(side=tk.LEFT)

        label_password = tk.Label(master=frame_password, text='Hasło')
        label_password.pack(side=tk.LEFT)
        entry_password = tk.Entry(master=frame_password, show='*')
        entry_password.pack(side=tk.LEFT)

        button_confirm = tk.Button(master=frame_button, text='Zaloguj', command=lambda: self.login(entry_login.get(), entry_password.get()))
        button_confirm.pack()

    def login(self, login, password):
        #TODO informacja o pustym polu
        try:
            self.client.login(login, password)
            messagebox.showinfo(title='Sukces', message='Poprawnie zalogowano')
            self.main_view()
            #TODO mainview
        except ValueError:
            messagebox.showwarning(title='Błąd', message='Użytkownik o podanej nazwie użytkownika i haśle nie istnieje')

    def register_view(self):
        self.reset_root()
        container = tk.Frame(master=self.root, height=300, width=300)
        container.pack_propagate(False)
        container.pack()

        frame_login = tk.Frame(master=container)
        frame_password = tk.Frame(master=container)
        frame_confirm = tk.Frame(master=container)
        frame_email = tk.Frame(master=container)
        frame_button = tk.Frame(master=container)

        frame_login.pack(expand=True)
        frame_password.pack(expand=True)
        frame_confirm.pack(expand=True)
        frame_email.pack(expand=True)
        frame_button.pack(expand=True)

        label_login = tk.Label(master=frame_login, text='Nazwa użytkownika')
        label_login.pack(side=tk.LEFT)
        entry_login = tk.Entry(master=frame_login)
        entry_login.pack(side=tk.LEFT)

        label_password = tk.Label(master=frame_password, text='Hasło')
        label_password.pack(side=tk.LEFT)
        entry_password = tk.Entry(master=frame_password, show='*')
        entry_password.pack(side=tk.LEFT)

        label_confirm = tk.Label(master=frame_confirm, text='Powtórz hasło')
        label_confirm.pack(side=tk.LEFT)
        entry_confirm = tk.Entry(master=frame_confirm, show='*')
        entry_confirm.pack(side=tk.LEFT)

        label_email = tk.Label(master=frame_email, text='Adres email')
        label_email.pack(side=tk.LEFT)
        entry_email = tk.Entry(master=frame_email)
        entry_email.pack(side=tk.LEFT)

        button_confirm = tk.Button(master=frame_button, text='Zarejestruj', command=lambda: self.register(entry_login.get(), entry_password.get(), entry_confirm.get(), entry_email.get()))
        button_confirm.pack()

    def register(self, login, password, confirmation, email):
        #TODO password = confirmation, długość hasła itd
        try:
            self.client.register(login, password, email)
            messagebox.showinfo(title='Sukces', message=f'Poprawnie zarejestrowano użytkownika {login}')
            self.auth_view()
        except ValueError:
            messagebox.showwarning(title='Błąd', message='Użytkownik o podanej nazwie użytkownika lub adresie email już istnieje')

    def main_view(self):
        self.reset_root()

        container = tk.Frame(master=self.root, height=250, width=300)
        container.pack_propagate(False)
        container.pack()

        frame_options = tk.Frame(master=container)
        frame_passwords = tk.Frame(master=container)

        frame_options.pack()
        frame_passwords.pack()
        scrollbar = tk.Scrollbar(master=frame_passwords)
        passwords = tk.Listbox(master=frame_passwords, yscrollcommand=scrollbar.set)

        button_add_password = tk.Button(master=frame_options, text='Dodaj hasło', command=self.add_password_view)
        button_add_password.pack(side=tk.RIGHT)

        button_copy_selected_pass = tk.Button(master=frame_options, text='Kopiuj hasło', command=lambda: pyperclip.copy(self.get_password(self.get_label(passwords))))
        button_copy_selected_pass.pack(side=tk.RIGHT)
        button_copy_selected_login = tk.Button(master=frame_options, text='Kopiuj login', command=lambda: pyperclip.copy(self.get_login(self.get_label(passwords))))
        button_copy_selected_login.pack(side=tk.RIGHT)

        scrollbar.config(command=passwords.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        passwords.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        for password in self.client.get_password_labels():
            passwords.insert(tk.END, password)

    def get_label(self, list):
        try:
            return list.get(list.curselection()[0])
        except IndexError:
            messagebox.showwarning(title='Błąd', message='Zaznacz etykietę z listy aby skopiować')

    def get_password(self, label):
        if label is None:
            return ''
        return self.client.get_password(label)[0]

    def get_login(self, label):
        if label is None:
            return ''
        return self.client.get_password(label)[1]


    def add_password_view(self):
        self.reset_root()
        container = tk.Frame(master=self.root, height=300, width=300)
        container.pack_propagate(False)
        container.pack()

        frame_label = tk.Frame(master=container)
        frame_password = tk.Frame(master=container)
        frame_username = tk.Frame(master=container)
        frame_button = tk.Frame(master=container)

        frame_label.pack(expand=True)
        frame_password.pack(expand=True)
        frame_username.pack(expand=True)
        frame_button.pack(expand=True)

        label_label = tk.Label(master=frame_label, text='Etykieta')
        label_label.pack(side=tk.LEFT)
        entry_label = tk.Entry(master=frame_label)
        entry_label.pack(side=tk.LEFT)

        label_password = tk.Label(master=frame_password, text='Hasło')
        label_password.pack(side=tk.LEFT)
        entry_password = tk.Entry(master=frame_password, show='*')
        entry_password.pack(side=tk.LEFT)

        label_username = tk.Label(master=frame_username, text='Nazwa użytkownika')
        label_username.pack(side=tk.LEFT)
        entry_username = tk.Entry(master=frame_username)
        entry_username.pack(side=tk.LEFT)

        button_confirm = tk.Button(master=frame_button, text='Dodaj', command=lambda: self.add_password(entry_label.get(), entry_password.get(), entry_username.get()))
        button_confirm.pack()

    def add_password(self, label, password, username):
        try:
            print(label, password, username)
            self.client.add_password(password, label, username)
            messagebox.showinfo(title='Sukces', message='Poprawnie dodano hasło')
            self.main_view()
        except ValueError as e:
            messagebox.showwarning(title='Błąd', message='Ups! Coś poszło nie tak')
            print(e)

    def run(self):
        self.auth_view()
        self.root.mainloop()

GUI().run()