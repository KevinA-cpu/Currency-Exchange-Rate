import tkinter as tk
from tkinter import * 
from tkinter import messagebox
from tkinter import ttk
from tkinter.ttk import *

import pyodbc
import urllib.request, json
import time
import socket
import threading
from threading import Timer
import pickle
import datetime
from datetime import date

# Connection info
PORT = 54321
# Commands
FORMAT = "utf8"
LOGIN = "login"
SIGNUP = "signup"
END = "exit"
CORRECT = "correct"
INCORRECT = "Incorrect"
CONNECT = "openconn"
WELCOME = "hello"
NONE = "none"
SHUTDOWN = "shutdown"
DATE = "date"
CURR = "currency"
BOTH = "both"
LISTEN = "listen"

#* Listen to the shutdown message from server
#listen
def listenSocket():
    try:
        listen.sendall(LISTEN.encode(FORMAT))
        lismsg = listen.recv(1024).decode(FORMAT)
        if(lismsg == SHUTDOWN):
            print(lismsg)
            messagebox.showinfo("SERVER OFFLINE", "Server has been shut down, press exit to leave.")
    except:
        listen.close()        

#* Startup page
class StartPage(tk.Frame):
    def __init__(self, parent, Control):
        tk.Frame.__init__(self, parent)
        
        canvas = Canvas(
                    self,
                    bg = "#1d3c45",
                    height = 600,
                    width = 1000,
                    bd = 0,
                    highlightthickness = 0,
                    relief = "ridge")
        canvas.place(x = 0, y = 0)
        
        # Background
        self.background_img = tk.PhotoImage(file = f"images/startPage/background.png")
        background = canvas.create_image(
            522.5, 300.0,
            image=self.background_img)

        # IP text box
        self.entry_img = tk.PhotoImage(file = f"images/startPage/textBox.png")
        entry0_bg = canvas.create_image(
            757.0, 300.5,
            image = self.entry_img)
        self.box_ip = tk.Entry(
            self,
            bd = 0,
            bg = "#fff1e1",
            font = ('Roboto 13'),
            fg = '#D2601A',
            highlightthickness = 0)
        self.box_ip.place(
            x = 572.0, y = 274,
            width = 370.0,
            height = 51)

        # "Let's go" button
        self.img = tk.PhotoImage(file = f"./images/startPage/button.png")
        button_log = tk.Button(
            self,
            image = self.img,
            borderwidth = 0,
            highlightthickness = 0,
            command = lambda: Control.ServerIP(self, client),
            relief = "flat")
        button_log.place(
            x = 686, y = 347,
            width = 127,
            height = 41)

        # Notification box
        self.label_notice = tk.Label(
            self,
            text="",
            font="13",
            fg="#1D3C45",
            bg="#FFF1E1")
        self.label_notice.pack()

#* Login page
class LoginPage(tk.Frame):
    def __init__(self, parent, Control):
        tk.Frame.__init__(self, parent)
        
        canvas = Canvas(
            self,
            bg = "#1d3c45",
            height = 600,
            width = 1000,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        canvas.place(x = 0, y = 0)

        # Background
        self.background_img = tk.PhotoImage(file = f"images/loginPage/background.png")
        background = canvas.create_image(
            577.0, 300.0,
            image=self.background_img)

        # Username text box
        self.box_username_img = tk.PhotoImage(file = f"images/loginPage/textBox_username.png")
        box_username_bg = canvas.create_image(
            757.0, 159.5,
            image = self.box_username_img)
        self.box_username = tk.Entry(
            self,
            bd = 0,
            bg = "#fff1e1",
            font = ('Roboto 13'),
            fg = '#D2601A',
            highlightthickness = 0)
        self.box_username.place(
            x = 572.0, y = 133,
            width = 370.0,
            height = 51)

        # Password text box
        self.box_password_img = tk.PhotoImage(file = f"images/loginPage/textBox_password.png")
        box_password_bg = canvas.create_image(
            757.0, 272.5,
            image = self.box_password_img)
        self.box_password = tk.Entry(
            self,
            bd = 0,
            bg = "#fff1e1",
            font = ('Roboto 13'),
            fg = '#D2601A',
            highlightthickness = 0)
        self.box_password.place(
            x = 572.0, y = 246,
            width = 370.0,
            height = 51)

        # Sign in button
        self.button_signin_img = tk.PhotoImage(file = f"images/loginPage/button_signin.png")
        button_signin = tk.Button(
            self,
            image = self.button_signin_img,
            borderwidth = 0,
            highlightthickness = 0,
            command = lambda: Control.LoginUser(self, client),
            relief = "flat")
        button_signin.place(
            x = 686, y = 337,
            width = 127,
            height = 41)

        # Sign up button
        self.button_signup_img = tk.PhotoImage(file = f"images/loginPage/button_signup.png")
        button_signup = tk.Button(
            self,
            image = self.button_signup_img,
            borderwidth = 0,
            highlightthickness = 0,
            command = lambda: Control.switchPage(SignupPage),
            relief = "flat")
        button_signup.place(
            x = 776, y = 431,
            width = 140,
            height = 41)

        # Exit button
        self.button_exit_img = tk.PhotoImage(file = f"images/loginPage/button_exit.png")
        button_exit = tk.Button(
            self,
            image = self.button_exit_img,
            borderwidth = 0,
            highlightthickness = 0,
            command = Control.clientExit,
            relief = "flat")
        button_exit.place(
            x = 728, y = 514,
            width = 43,
            height = 43)

        # Notification box
        self.label_notice = tk.Label(
            self,
            text="",
            font="13",
            fg="#1D3C45",
            bg="#FFF1E1")
        self.label_notice.pack()

#* Sign up page
class SignupPage(tk.Frame):
     def __init__(self, parent, Control):
        tk.Frame.__init__(self, parent)

        canvas = Canvas(
            self,
            bg = "#1d3c45",
            height = 600,
            width = 1000,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        canvas.place(x = 0, y = 0)

        # Background
        self.background_img = tk.PhotoImage(file = f"images/signupPage/background.png")
        background = canvas.create_image(
            574.0, 300.0,
            image=self.background_img)

        # Username text box
        self.box_username_img = tk.PhotoImage(file = f"images/signupPage/textBox_username.png")
        box_username_bg = canvas.create_image(
            757.0, 159.5,
            image = self.box_username_img)
        self.box_username = tk.Entry(
            self,
            bd = 0,
            bg = "#fff1e1",
            font = ('Roboto 13'),
            fg = '#D2601A',
            highlightthickness = 0)
        self.box_username.place(
            x = 572.0, y = 133,
            width = 370.0,
            height = 51)

        # Password text box
        self.box_password_img = tk.PhotoImage(file = f"images/signupPage/textBox_password.png")
        box_password_bg = canvas.create_image(
            757.0, 272.5,
            image = self.box_password_img)
        self.box_password = tk.Entry(
            self,
            bd = 0,
            bg = "#fff1e1",
            font = ('Roboto 13'),
            fg = '#D2601A',
            highlightthickness = 0)
        self.box_password.place(
            x = 572.0, y = 246,
            width = 370.0,
            height = 51)

        # Sign up button
        self.button_signup_img = tk.PhotoImage(file = f"images/signupPage/button_signup.png")
        self.button_sign_up = tk.Button(
            self,
            image = self.button_signup_img,
            borderwidth = 0,
            highlightthickness = 0,
            command = lambda: Control.SignupUser(self,client),
            relief = "flat")

        self.button_sign_up.place(
            x = 686, y = 337,
            width = 127,
            height = 41)

        # Sign in button
        self.button_signin_img = tk.PhotoImage(file = f"images/signupPage/button_signin.png")
        self.button_signin = tk.Button(
            self,
            image = self.button_signin_img,
            borderwidth = 0,
            highlightthickness = 0,
            command = lambda: Control.switchPage(LoginPage),
            relief = "flat")

        self.button_signin.place(
            x = 776, y = 431,
            width = 140,
            height = 41)

        # Exit button
        self.button_exit_img = tk.PhotoImage(file = f"images/signupPage/button_exit.png")
        self.button_exit = tk.Button(
            self,
            image = self.button_exit_img,
            borderwidth = 0,
            highlightthickness = 0,
            command = Control.clientExit,
            relief = "flat")

        self.button_exit.place(
            x = 728, y = 514,
            width = 43,
            height = 43)

        # Notification box
        self.label_notice = tk.Label(
            self,
            text="",
            font="13",
            fg="#1D3C45",
            bg="#FFF1E1")
        self.label_notice.pack()

#* Admin page
class AdminPage(tk.Frame):
    def __init__(self, parent, Control):
        tk.Frame.__init__(self, parent)

        canvas = Canvas(
            self,
            bg = "#1d3c45",
            height = 600,
            width = 1000,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        canvas.place(x = 0, y = 0)

        # Background
        self.background_img = tk.PhotoImage(file = f"images/adminPage/background.png")
        background = canvas.create_image(
            572.5, 300.0,
            image=self.background_img)

        # SHUT DOWN button
        self.button_shutdown_img = PhotoImage(file = f"images/adminPage/button_shutdown.png")
        button_shutdown = tk.Button(
            self,
            image = self.button_shutdown_img,
            borderwidth = 0,
            highlightthickness = 0,
            command = lambda: Control.shutDown(client),
            relief = "flat")
        button_shutdown.place(
            x = 560, y = 284,
            width = 140,
            height = 41)

        # Log out button
        self.button_logout_img = PhotoImage(file = f"images/adminPage/button_logout.png")
        button_logout = tk.Button(
            self,
            image = self.button_logout_img,
            borderwidth = 0,
            highlightthickness = 0,
            command = lambda: Control.switchPage(LoginPage),
            relief = "flat")
        button_logout.place(
            x = 802, y = 284,
            width = 127,
            height = 41)

        # Exit button
        self.button_exit_img = tk.PhotoImage(file = f"images/adminPage/button_exit.png")
        button_exit = tk.Button(
            self,
            image = self.button_exit_img,
            borderwidth = 0,
            highlightthickness = 0,
            command = Control.clientExit,
            relief = "flat")
        button_exit.place(
            x = 728, y = 367,
            width = 43,
            height = 43)

#* Home page
class HomePage(tk.Frame):
    def __init__(self, parent, Control):
        tk.Frame.__init__(self, parent)

        canvas = Canvas(
            self,
            bg = "#1d3c45",
            height = 600,
            width = 1000,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        canvas.place(x = 0, y = 0)

        # Background
        self.background_img = PhotoImage(file = f"images/homePage/background.png")
        background = canvas.create_image(
            534.5, 300.0,
            image=self.background_img)

        # Currency text box
        self.box_currency_img = PhotoImage(file = f"images/homePage/textBox_currency.png")
        box_currency_bg = canvas.create_image(
            257.0, 159.5,
            image = self.box_currency_img)
        self.box_currency = tk.Entry(
            self,
            bd = 0,
            bg = "#fff1e1",
            font = ('Roboto 13'),
            fg = '#D2601A',
            highlightthickness = 0)
        self.box_currency.place(
            x = 72.0, y = 133,
            width = 370.0,
            height = 51)

        # Date text box
        self.box_date_img = PhotoImage(file = f"images/homePage/textBox_date.png")
        box_date_bg = canvas.create_image(
            257.0, 272.5,
            image = self.box_date_img)
        self.box_date = tk.Entry(
            self,
            bd = 0,
            bg = "#fff1e1",
            font = ('Roboto 13'),
            fg = '#D2601A',
            highlightthickness = 0)
        self.box_date.place(
            x = 72.0, y = 246,
            width = 370.0,
            height = 51)

        # Search button
        self.button_search_img = PhotoImage(file = f"images/homePage/button_search.png")
        button_search = tk.Button(
            self,
            image = self.button_search_img,
            borderwidth = 0,
            highlightthickness = 0,
            command = lambda: self.search(client),
            relief = "flat")
        button_search.place(
            x = 186, y = 337,
            width = 127,
            height = 41)

        # Log out button
        self.button_logout_img = PhotoImage(file = f"images/homePage/button_logout.png")
        button_logout = tk.Button(
            self,
            image = self.button_logout_img,
            borderwidth = 0,
            highlightthickness = 0,
            command = lambda: Control.switchPage(LoginPage),
            relief = "flat")
        button_logout.place(
            x = 186, y = 441,
            width = 127,
            height = 41)

        # Exit button
        self.button_exit_img = PhotoImage(file = f"images/homePage/button_exit.png")
        button_exit = tk.Button(
            self,
            image = self.button_exit_img,
            borderwidth = 0,
            highlightthickness = 0,
            command = Control.clientExit,
            relief = "flat")
        button_exit.place(
            x = 228, y = 514,
            width = 43,
            height = 43)

        # Notification box
        self.label_notice = tk.Label(
            self,
            text="",
            font="13",
            fg="#1D3C45",
            bg="#FFF1E1")
        self.label_notice.pack()

        # Content box/scrollbar
        self.frame = tk.Frame(self)
        self.content = tk.Listbox(
            self.frame,
            height = 25,
            width = 45, 
            bg='#FFF1E1',
            activestyle='dotbox', 
            font="Courier",
            fg='#D2601A')

        # Vertical scrollbar
        self.vertical_scrollbar = tk.Scrollbar(self.frame)
        self.vertical_scrollbar.pack(side = RIGHT, fill = BOTH)
        self.content.config(yscrollcommand = self.vertical_scrollbar.set)
        self.vertical_scrollbar.config(command = self.content.yview)
        # Horizontal scrollbar
        self.horizontal_scrollbar = tk.Scrollbar(self.frame, orient='horizontal')
        self.horizontal_scrollbar.pack(side = BOTTOM, fill = 'x')
        self.content.config(xscrollcommand = self.horizontal_scrollbar.set)
        self.horizontal_scrollbar.config(command = self.content.xview)

        self.content.pack()
        self.frame.place(
            relx = 0.75, rely = 0.55,
            anchor="center")

    def search(self, Socket:socket):
        try:
            # Empty the content box
            self.content.delete(0, tk.END)
            date = self.box_date.get()
            currency = self.box_currency.get()
            if date == "" and currency == "":
                self.label_notice["text"] = "Fields can't be empty"
                return
            # Check the date format
            elif date != "":
                try:
                    datetime.datetime.strptime(date,"%Y-%m-%d")
                except:
                    self.label_notice["text"] = "Not a valid date format"
                    return

            if date == "": # If the date text box is empty
               msg = CURR
            elif currency == "": # If the currency text box is empty
               msg = DATE
            else:
               msg = BOTH

            # Send command when the Search button is pressed
            Socket.sendall(msg.encode(FORMAT))
            if msg == CURR: # Send currency
                Socket.sendall(currency.encode(FORMAT))
            elif msg == DATE: # Send date
                Socket.sendall(date.encode(FORMAT))
            elif msg == BOTH: # Send both date and currency
                Socket.sendall(currency.encode(FORMAT))
                Socket.recv(1024).decode(FORMAT)
                Socket.sendall(date.encode(FORMAT))
                Socket.recv(1024).decode(FORMAT)

            # Receive data from server
            currency = Socket.recv(4096)
            recv_currency = pickle.loads(currency)
            for row in recv_currency:
                row[0] = row[0].strftime("%Y-%m-%d")
            for val in range(len(recv_currency)):
                self.content.insert(val, recv_currency[val])
            self.label_notice["text"] = "Search completed"

        except:
             messagebox.showinfo("SERVER SHUTDOWN","Server is offline, press exit to leave.")

#* Main class
class Main(tk.Tk):
    def __init__(self): 
        tk.Tk.__init__(self)

        self.title("Currency Exchange Rates")
        self.iconbitmap('images/currencies.ico')
        self.geometry("1000x600")
        self.resizable(width=False, height=False)
        self.protocol("WM_DELETE_WINDOW", self.clientExit)

        container = tk.Frame()
        container.configure(bg="#1d3c45")

        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, LoginPage, SignupPage, HomePage, AdminPage):
            frame = F(container, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[F] = frame

        self.frames[StartPage].tkraise()

    #* Switch between frames
    def switchPage(self, Frame): 
        self.frames[Frame].tkraise()

    #* Shut the server down, only for admin account
    def shutDown(self, Socket:socket):
        Socket.sendall(SHUTDOWN.encode(FORMAT)) # Tell the server to shut down

    def clientExit(self):
        self.destroy()
        try:
            client.sendall(END.encode(FORMAT))
        except:
            pass

    #* Get the server IP and let clients connect to the server
    def ServerIP(self, Frame, Socket: socket):
        try:
            server_ip = Frame.box_ip.get()
            if server_ip == "":
                Frame.label_notice["text"] = "This field can't be empty"
                return

            # Connect to server via IP
            Socket.connect((server_ip,PORT))
            Socket.sendall(WELCOME.encode(FORMAT))
            msg = Socket.recv(1024).decode(FORMAT)

            if (msg == CONNECT):
                #*Socket listen to the shutdown message from server
                listen.connect((server_ip,PORT))
                cThread = threading.Thread(target = listenSocket)
                cThread.daemon = True
                cThread.start()
                self.switchPage(LoginPage)
        except:
            Frame.label_notice["text"] = "Server is unavailable!"

    def LoginUser(self,Frame,Socket: socket):
        try:
            username = Frame.box_username.get()
            password = Frame.box_password.get()
            if username == "" or password == "":
                Frame.label_notice["text"] = "These fields can't be empty"
                return
            
            # Send command when the Signup button is pressed
            Socket.sendall(LOGIN.encode(FORMAT))

            # Send account information
            Socket.sendall(username.encode(FORMAT))
            msg = Socket.recv(1024).decode(FORMAT)
            print(msg)
            Socket.sendall(password.encode(FORMAT))
            msg = Socket.recv(1024).decode(FORMAT)
            print(msg)

            # Check username and password in database
            msg = Socket.recv(1024).decode(FORMAT)
            if (msg == CORRECT):
                Frame.label_notice["text"] = "Login Success!"
                if (username=="admin" and password =="admin"):
                    self.switchPage(AdminPage)
                else:
                    self.switchPage(HomePage)
            elif (msg == INCORRECT):
                Frame.label_notice["text"] = "Wrong password"
                return
            elif (msg == NONE):
                Frame.label_notice["text"] = "Account does not exist"
                return

        except:
            messagebox.showinfo("SERVER SHUTDOWN","Server is offline, press exit to leave.")
             
    def SignupUser(self,Frame,Socket:socket):
        try:
            username = Frame.box_username.get()
            password = Frame.box_password.get()
            if username == "" or password == "":
                Frame.label_notice["text"] = "Fields can't be empty"
                return
            # Send command when the Signup button is pressed
            Socket.sendall(SIGNUP.encode(FORMAT))

            # Send account information
            Socket.sendall(username.encode(FORMAT))
            Socket.recv(1024).decode(FORMAT)
            Socket.sendall(password.encode(FORMAT))
            Socket.recv(1024).decode(FORMAT)

            # Check username and password in database
            msg = Socket.recv(1024).decode(FORMAT)
            if(msg == NONE):
                Frame.label_notice["text"] = "Signup success!"
                self.switchPage(LoginPage)
            elif(msg == INCORRECT):
                Frame.label_notice["text"] = "Username already exist"
                return
            elif(msg == CORRECT):
                Frame.label_notice["text"] = "Account already exist."
                return
        except:
            messagebox.showinfo("SERVER SHUTDOWN","Server is offline, press exit to leave.")

#! MAIN SECTION !#
client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
listen = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

app = Main()
# Run the application
try:
    app.mainloop()
except:
    print("Error! Server is not responding!")
    client.close()
    listen.close()
finally:
    client.close()
    listen.close()