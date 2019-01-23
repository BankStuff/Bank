import databases
import tkinter
from tkinter import messagebox
import hashlib
from decimal import Decimal

# Globals


usernames =     {
                        'ADMIN' : 'c7ad44cbad762a5da0a452f9e854fdc1e0e7a52a38015f23f3eab1d80b931dd472634dfac71cd34ebc35d16ab7fb8a90c81f975113d6c7538dc69dd8de9077ec',
                        'BEN' : '5b722b307fce6c944905d132691d5e4a2214b7fe92b738920eb3fce3a90420a19511c3010a0e7712b054daef5b57bad59ecbd93b3280f210578f547f4aed4d25',
                }

users = {'ADMIN' : 0, 'BEN' : 0}

# Functions

def hash(password):

        '''Returns a hashed version of the input via SHA512'''
        
        return hashlib.sha512(password.encode('utf-8')).hexdigest()

def getBalance():

        '''Gets the balances of the users from the database and stores it in the users dictionary'''

        databases.createdatabase('balance','','.txt')

        for user in users:
                x = 0
                for databaseuser in databases.readto('balance',';','','.txt'):
                        if databaseuser == user:
                                users[user] = databases.readto('balance',';','','.txt')[x+1]
                        x += 1

def saveBalance():

        '''Gets the balances of the users from the users dictionary and stores it in the database'''

        databases.cleardatabase('balance','','.txt')
        
        for user in users:
                databases.writeto('balance',user,';','','.txt')
                databases.writeto('balance',users[user],';','','.txt')

def withdraw(amount, funds, username, bankingWindow):

        '''Withdraws money from the balance database'''

        global users

        # Validation
        
        try:
                float(amount)
                funds = float(funds)

                if abs(Decimal(str(amount)).as_tuple().exponent) > 2:
                        messagebox.showinfo('Withdrawal unsuccessful', 'Invalid fund entered')
                        return None
                elif abs(float(amount)) != float(amount):
                        messagebox.showinfo('Withdrawal unsuccessful', 'Invalid fund entered')
                        return None
        except:
                messagebox.showinfo('Withdrawal unsuccessful', 'Invalid fund entered')
                return None

        if not abs(float(funds) - float(amount)) == float(funds) - float(amount):
                messagebox.showinfo('Withdrawal unsuccessful', 'Insufficent Funds')
                return None

        # Withdraws Money

        users[username.upper()] = format(float(users[username.upper()]) - float(amount), '.2f')
        saveBalance()
        messagebox.showinfo('Withdrawal successful', 'Withdrawed a total of: £' + str(format(float(amount), '.2f')))

        # Reloads Window

        bankInfo(username, bankingWindow)

def deposit(amount, funds, username, bankingWindow):

        '''Deposits money from the balance database'''

        global users

        # Validation
        
        try:
                float(amount)
                funds = float(funds)

                if abs(Decimal(str(amount)).as_tuple().exponent) > 2:
                        messagebox.showinfo('Deposit unsuccessful', 'Invalid fund entered')
                        return None
                elif abs(float(amount)) != float(amount):
                        messagebox.showinfo('Deposit unsuccessful', 'Invalid fund entered')
                        return None
        except:
                messagebox.showinfo('Deposit unsuccessful', 'Invalid fund entered')
                return None        

        # Depsoits Money

        users[username.upper()] = format(float(users[username.upper()]) + float(amount), '.2f')
        saveBalance()
        messagebox.showinfo('Deposit successful', 'Desposited a total of: £' + str(format(float(amount), '.2f')))

        # Reloads Window

        bankInfo(username, bankingWindow)

def bankInfo(username, prevWindow):
        
        '''Creates the banking window'''

        global users
        
        prevWindow.destroy() # Destroys Previous Window

        # Creates Banking Window

        ## Window Configuration
        
        window = tkinter.Tk()
        window.title("Banking")
        window.geometry("250x250")
        window.configure(background='gray')

        ## Balance And Logout Creations

        label3 = tkinter.Label(window, text = username.title() + "'s Balance: " + str(users[username.upper()]))
        label3.place(x=125, y=20, anchor="center")
        logout = tkinter.Button(window, text='Logout',command=lambda: main(window))
        logout.grid()
        logout.place(x=125, y=250, anchor="s")

        ## Deposit Objects

        entry4 = tkinter.Entry(window)
        entry4.place(x=125, y=115, anchor="s")
        label4 = tkinter.Button(window, text="Deposit:", command=lambda: deposit(entry4.get(), str(users[username.upper()]), username, window))
        label4.place(x=125, y=95, anchor="s")

        ## Withdrawal Objects

        entry5 = tkinter.Entry(window)
        entry5.place(x=125, y=175, anchor="s")
        label5 = tkinter.Button(window, text="Withdraw:", command=lambda: withdraw(entry5.get(), str(users[username.upper()]), username, window))
        label5.place(x=125, y=155, anchor="s")

        ## Default Texts

        entry4.insert(0, '0.00')
        entry5.insert(0, '0.00')

        ## Mainloop
        
        window.mainloop()


def userValidate(userLogin, userPass, mainWindow):

        '''Checks if the username and corrosponding password are valid'''

        # Checks If The Usernames In The Database
        
        nameCorrect = False

        try:
                usernames[userLogin.upper()]
        except:
                messagebox.showinfo('FAILURE','Incorrect Username')
                nameCorrect = True

        # Checks If The Corrosponding Password Is Correct
        
        if nameCorrect == False:
                if usernames[userLogin.upper()] == hash(userPass):
                        bankInfo(userLogin, mainWindow)
                else:
                        messagebox.showinfo('Failure','Incorrect Password')

def creation(usernameTry, password1Try, password2Try, window):

        '''Registers the user to the database'''

        # Validation

        for user in users:
                if user == usernameTry.upper():
                        messagebox.showinfo('Failure', 'Username taken')
                        return None

        '''
        if not usernameTry.isalpha():
                messagebox.showinfo('Failure', 'Username must only contain characters')
                return None
        '''

        if password1Try != password2Try:
                messagebox.showinfo("Failure", "Passwords don't match")
                return None

        # Adds Data To Database

        databases.writeto('users',str(usernameTry.upper()),';','','.txt')
        databases.writeto('users',str(hash(password1Try)),';','','.txt')

        databases.writeto('balance',str(usernameTry.upper()),';','','.txt')
        databases.writeto('balance','0',';','','.txt')

        messagebox.showinfo("Success", "Account Created")

        # Loads Main Window

        main(window)

def usersSet():

        '''Sets users dictionary up, to match the database'''

        global users

        users = {}

        usersDatabase = databases.readto('users',';','','.txt')

        for x in range(int(len(usersDatabase)/2)):
                users[usersDatabase[2*x]] = 0

def usernamesSet():

    '''Sets users dictionary up, to match the database'''

    global usernames

    usersDatabase = databases.readto('users',';','','.txt')

    usernames = {}

    for x in range(int(len(usersDatabase)/2)):
        usernames[usersDatabase[2*x]] = usersDatabase[(2*x)+1]

def userCreate(window):

        '''Creates a user registration window'''

        window.destroy() # Destroys Inputted Window

        # Creates Login Window

        ## Window Configuration
        
        window = tkinter.Tk()
        window.title('Register')
        window.geometry("200x250")
        window.configure(background='grey')

        ## Object Creations

        label8 = tkinter.Label(window, text="Username:")
        entry8 = tkinter.Entry(window)

        label9 = tkinter.Label(window, text="Password:")
        entry9 = tkinter.Entry(window, show='*')

        label10 = tkinter.Label(window, text="Password Confirmation:")
        entry10 = tkinter.Entry(window, show='*')

        create = tkinter.Button(window, text='Create', command=lambda: creation(entry8.get(), entry9.get(), entry10.get(), window))
        exit = tkinter.Button(window, text='Exit', command=lambda: main(window))

        ## Object Placements

        label8.pack()
        label8.place(x=100, y=35, anchor="s")
        
        entry8.pack()
        entry8.place(x=100, y=55, anchor="s")
        
        label9.pack()
        label9.place(x=100, y=85, anchor="s")
        
        entry9.pack()
        entry9.place(x=100, y=105, anchor="s")

        label10.pack()
        label10.place(x=100, y=135, anchor="s")
        
        entry10.pack()
        entry10.place(x=100, y=155, anchor="s")        
        
        create.pack()
        create.place(x=100, y=200, anchor="s")

        exit.pack()
        exit.place(x=100, y=235, anchor="s")

        ## Mainloop

        window.mainloop()

def main(root=None):

        '''Creates the login window and performs an application setup'''

        try:
                root.destroy() # Destroys Inputted Window
        except:
                pass

        # Setup

        usersSet()
        usernamesSet()
        getBalance()

        # Creates Login Window

        ## Window Configuration
        
        window = tkinter.Tk()
        window.title('Login')
        window.geometry("200x180")
        window.configure(background='grey')

        ## Object Creations

        label1 = tkinter.Label(window, text="Username:")
        entry1 = tkinter.Entry(window)


        label2 = tkinter.Label(window, text="Password:")
        entry2 = tkinter.Entry(window, show='*')

        login = tkinter.Button(window, text='Login', command=lambda: userValidate(entry1.get(), entry2.get(), window))
        register = tkinter.Button(window, text='Register', command=lambda: userCreate(window))

        ## Object Placements

        label1.pack()
        label1.place(x=100, y=35, anchor="s")
        
        entry1.pack()
        entry1.place(x=100, y=55, anchor="s")
        
        label2.pack()
        label2.place(x=100, y=85, anchor="s")
        
        entry2.pack()
        entry2.place(x=100, y=105, anchor="s")
        
        login.pack()
        login.place(x=100, y=145, anchor="s")

        register.pack()
        register.place(x=100, y=175, anchor="s")

        ## Mainloop

        window.mainloop()


if __name__ == '__main__':
        main()
