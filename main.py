import databases
import tkinter
from tkinter import messagebox
import hashlib

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

def bankInfo(username, mainWindow):
        
        '''Creates the banking window'''

        global users
        
        mainWindow.destroy() # Destroys Login Window

        # Creates Banking Window
        
        window = tkinter.Tk()
        window.title("Banking")
        window.geometry("250x250")
        window.configure(background='gray')
        label3 = tkinter.Label(window, text = username.title() + "'s Balance: " + str(users[username.upper()]))
        label3.place(x=125, y=80, anchor="center")
        logout = tkinter.Button(window, text='Logout',command=lambda: main(window))
        logout.grid(row=0)
        window.mainloop()


def userValidate(userLogin, userPass, mainWindow):

        '''Checks if the username and corrosponding password are valid'''
        
        nameCorrect = False

        try:
                usernames[userLogin.upper()]
        except:
                messagebox.showinfo('FAILURE','Incorrect Username')
                nameCorrect = True

        
        if nameCorrect == False:
                if usernames[userLogin.upper()] == hash(userPass):
                        bankInfo(userLogin, mainWindow)
                else:
                        messagebox.showinfo('FAILURE','Incorrect Password')

def main(root=None):

        '''Creates the login window and performs an application setup'''

        try:
                root.destroy() # Destroys Inputted Window
        except:
                pass

        # Setup

        getBalance()

        # Creates Login Window
        
        window = tkinter.Tk()
        window.title('Login')
        window.geometry("200x150")
        window.configure(background='grey')

        label1 = tkinter.Label(window, text="Username:")


        entry1 = tkinter.Entry(window)


        label2 = tkinter.Label(window, text="Password:")
        entry2 = tkinter.Entry(window, show='*')

        login = tkinter.Button(window, text='Login', command=lambda: userValidate(entry1.get(), entry2.get(), window))

        label1.pack()
        entry1.pack()
        label2.pack()
        entry2.pack()
        login.pack()

        window.mainloop()


if __name__ == '__main__':
        main()
