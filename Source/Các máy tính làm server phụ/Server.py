import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
from datetime import date

import time
import socket
import threading
from threading import Timer
import pyodbc
import urllib.request, json
import requests
import pickle

# Server info
MAINHOST = "::"
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

listen = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
listen.bind((MAINHOST,PORT))
listen.listen(5)

CLIENTS = [] # Clients that has been connected to server
curAccounts = [] # Clients that are connecting to server

#* Search with just 1 currency information
def searchCurr(conn):
    currency = conn.recv(1024).decode(FORMAT)
    print(currency)
    # Find currency
    cur.execute("Select * from currencyvcb where currency = ?", currency)
    sql_data = cur.fetchall()
    # Send data
    result = pickle.dumps(sql_data)
    conn.send(result)

#* Search with just 1 date information
def searchDate(conn):
    date = conn.recv(1024).decode(FORMAT)
    print(date)
    # Find currency
    cur.execute("Select * from currencyvcb where date = ?", date)
    sql_data = cur.fetchall()
    # Send data
    result = pickle.dumps(sql_data)
    conn.send(result)

#* Search with both currency and date information
def searchBoth(conn):
    currency = conn.recv(1024).decode(FORMAT)
    conn.sendall(currency.encode(FORMAT))
    date = conn.recv(1024).decode(FORMAT)
    conn.sendall(date.encode(FORMAT))
    print(date + " " + currency)
    # Find currency
    cur.execute("Select * from currencyvcb where currency = ? and date = ?", (currency, date))
    sql_data = cur.fetchall()
    # Send data
    result = pickle.dumps(sql_data)
    conn.send(result)

#* Update data
def updateData(data):
    # Set up data to send request
    apikey = list(data.values())[0]
    url = "https://vapi.vnappmob.com/api/v2/exchange_rate/vcb"
    data = {"Accept": "application/json"}
    auth = "Bearer" + " " +  apikey
    headers = {'Authorization': auth}
    # Get data
    apidata = requests.get(url,data = data, headers = headers).json()
    currency_exchange_rate = list(apidata.values())[0]
    
    today = date.today()
    for val in currency_exchange_rate:
        # Update when on the same day
        cur.execute(
            "UPDATE TOP (1) currencyvcb SET buy_cash = ?,\
            buy_transfer = ?,\
            sell = ? WHERE date = ? AND currency = ?",\
            (val['buy_cash'], val['buy_transfer'], val['sell'], today, val['currency']))
        cur.commit()

#* Delete accounts in curAccounts[]
def removeAccounts(addr):
    size = len(curAccounts)
    i = 0
    while i < size:
        for row in curAccounts:
            if (str(addr) in row) or (END in row):
                curAccounts.remove(row)
        i = i + 1
    curAccounts.append(str(addr) + " " + END)

#* Shut the server down (by admin account)
def shutDown():
    num = len(CLIENTS)
    i = 0
    while i < num:
        for client in CLIENTS:
            client.sendall(SHUTDOWN.encode(FORMAT))
            CLIENTS.remove(client)
            client.close()
        i = i+1
    app.serverExit()

#* Sign up 
def clientSignup(conn:socket,addr):
    # Receive username and password from client...
    username = conn.recv(1024).decode(FORMAT)
    conn.sendall(username.encode(FORMAT))
    password = conn.recv(1024).decode(FORMAT)
    conn.sendall(username.encode(FORMAT))
    # ...and pint them on the console
    print(username)
    print(password)

    # Find password in database
    cur.execute("Select password from loginserver where username = ?", username)
    sql_pass = cur.fetchone()
    msg = None
    
    if(sql_pass == None): # Can't find password in database
        msg = NONE
        cur.execute("insert into loginserver(username, password) values(?,?)", (username,password))
        cur.commit()
        print("account added")
        curAccounts.append(username + " at " + str(addr) + " " + SIGNUP)
    elif (password == sql_pass[0]):# Password and Username are correct
        msg = CORRECT
        print("Account already exist")
    else: # Wrong password
        msg = INCORRECT
        print("Username already exist")
    conn.sendall(msg.encode(FORMAT))

#* Log in
def clientLogin(conn:socket,addr):
    # Receive username and password from client...
    username = conn.recv(1024).decode(FORMAT)
    conn.sendall(username.encode(FORMAT))
    password = conn.recv(1024).decode(FORMAT)
    conn.sendall(username.encode(FORMAT))
    # ...and pint them on the console
    print(username)
    print(password)

    # Find password in database
    cur.execute("Select password from loginserver where username = ?", username)
    sql_pass = cur.fetchone()
    msg = None
    
    if(sql_pass == None): # Can't find password in database
        msg = NONE
        print("Account does not exist")
    elif (password == sql_pass[0]): # Password and Username are correct
        curAccounts.append(username + " at " + str(addr) + " " + LOGIN)
        msg = CORRECT
        print("Login successfully")
    else: # Wrong password
        msg = INCORRECT
        print("Invalid password")
    conn.sendall(msg.encode(FORMAT))

#* Handle multi clients
def handle_multi_clients(conn,addr):
    try:
        while True:
            control = conn.recv(1024).decode(FORMAT)

            if control == LOGIN:
                clientLogin(conn,addr)

            elif control == WELCOME:
                # curAccounts.append("Someone at " + str(addr) + " connected ")
                curAccounts.append(str(addr) + " connected")
                conn.sendall(CONNECT.encode(FORMAT))

            elif control == SIGNUP:
                clientSignup(conn,addr)

            elif control == DATE:
                searchDate(conn)

            elif control == CURR:
                searchCurr(conn)

            elif control == BOTH:
                searchBoth(conn)

            elif control == LISTEN:
                CLIENTS.append(conn)

            elif control == END:
                print(END)
                # User exit, close socket , empty information in content box
                removeAccounts(addr)
                conn.close()
                break

            elif control == SHUTDOWN:
                shutDown()
    except:
        num = len(CLIENTS)
        j = 0
        while j < num:
            for client in CLIENTS:
                if client == conn:
                    CLIENTS.remove(client)
        j = j+1
        
        removeAccounts(addr)
        conn.close()
        
#* Start server
def startServer():
    try:
        print(MAINHOST) # Server's information

        while True:
        # Start loop to handle clients
            print("enter loop")
            connection, address = listen.accept()
            cThread = threading.Thread(target = handle_multi_clients, args = (connection, address))
            cThread.daemon=True
            cThread.start()
            print("end server")
    except:
        print("Error")
        listen.close()

#* Run application every interval of second
class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.next_call = time.time()
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self.next_call += self.interval
            self._timer = threading.Timer(self.next_call - time.time(), self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

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
        self.background_img = PhotoImage(file = f"images/server/background.png")
        background = canvas.create_image(
            599.5, 300.0,
            image=self.background_img)

        # INSERT button
        self.button_insert_img = PhotoImage(file = f"images/server/button_insert.png")
        self.button_insert = tk.Button(
            image = self.button_insert_img,
            borderwidth = 0,
            highlightthickness = 0,
            command = lambda: self.insertData(data),
            relief = "flat")
        self.button_insert.place(
            x = 65, y = 280,
            width = 127,
            height = 41)

        # Refresh button
        self.button_refresh_img = PhotoImage(file = f"images/server/button_refresh.png")
        self.button_refresh = tk.Button(
            image = self.button_refresh_img,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.refreshContent,
            relief = "flat")
        self.button_refresh.place(
            x = 307, y = 280,
            width = 127,
            height = 41)

        # Exit button
        self.button_exit_img = PhotoImage(file = f"images/server/button_exit.png")
        self.button_exit = tk.Button(
            image = self.button_exit_img,
            borderwidth = 0,
            highlightthickness = 0,
            command = Control.serverExit,
            relief = "flat")
        self.button_exit.place(
            x = 228, y = 385,
            width = 43,
            height = 43)

        # Content box/scrollbars
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
            relx = 0.75, rely = 0.56,
            anchor="center")

    def insertData(self,data):
        # Set up data to send request
        apikey = list(data.values())[0]
        url = "https://vapi.vnappmob.com/api/v2/exchange_rate/vcb"
        data = {"accept": "application/json"}
        auth = "bearer" + " " +  apikey
        headers = {'authorization': auth}
        # Get data
        apidata = requests.get(url,data = data, headers = headers).json()
        currency_exchange_rate = list(apidata.values())[0]
        
        today = date.today() # The INSERT button can only be pressed ONCE A DAY
        for val in currency_exchange_rate:
            # Insert when on a different day
            cur.execute("insert into currencyvcb(date, currency, buy_cash, buy_transfer, sell) values(?,?,?,?,?)",
                       (today, val['currency'], val['buy_cash'], val['buy_transfer'], val['sell']))
            cur.commit()
        self.content.insert(0,"Inserted new data!")
        
    def refreshContent(self):
        self.content.delete(0,len(curAccounts))
        for account in range(len(curAccounts)):
            self.content.insert(account,curAccounts[account])

#* Main GUI section
class Main(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.title("Currency Exchange Rate")
        self.iconbitmap('images/currencies.ico')
        self.geometry("1000x600")
        self.resizable(width=False, height=False)
        self.protocol("WM_DELETE_WINDOW", self.serverExit)

        container = tk.Frame()
        container.configure(bg="orange")

        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        frame_home = HomePage(container,self)
        frame_home.grid(row=0, column=0, sticky="nsew")
        frame_home.tkraise()

    def serverExit(self):
        app.destroy()

#* Connect to database
sql_dat = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};\
        SERVER=42.119.66.162,1433;\
            # PORT=1433;\
                Database=socketserver;\
                    UID=dhlogin;\
                        PWD=seaways456;'
                        )
cur = sql_dat.cursor()

#* Get data from API
data = None
with urllib.request.urlopen("https://vapi.vnappmob.com/api/request_api_key?scope=exchange_rate") as url:
    data = json.load(url)

auto_repeat = RepeatedTimer(1800, updateData, data) # Update data every 1800 seconds

try:
    # Keep GUI window running while executing functions
    mThread = threading.Thread(target = startServer)
    mThread.daemon = True # Kill every single thread when the application is turned off
    mThread.start()
    app = Main()
    app.mainloop()
finally:
    auto_repeat.stop()
    cur.close()