import databases
import tkinter
from tkinter import messagebox
import hashlib

# Globals

usernames = {
                        'ADMIN' : 'c7ad44cbad762a5da0a452f9e854fdc1e0e7a52a38015f23f3eab1d80b931dd472634dfac71cd34ebc35d16ab7fb8a90c81f975113d6c7538dc69dd8de9077ec',
                        'BEN' : '5b722b307fce6c944905d132691d5e4a2214b7fe92b738920eb3fce3a90420a19511c3010a0e7712b054daef5b57bad59ecbd93b3280f210578f547f4aed4d25',
                        }

users = {'ADMIN' : 0, 'BEN' : 0}

# Functions

def hash(password):
        return hashlib.sha512(password.encode('utf-8')).hexdigest()

def getBalance():

        databases.createdatabase('balance','','.txt')

        for user in users:
                x = 0
                for databaseuser in databases.readto('balance',';','','.txt'):
                        if databaseuser == user:
                                users[user] = databases.readto('balance',';','','.txt')[x+1]
                        x += 1

def saveBalance():

        databases.cleardatabase('balance','','.txt')
        
        for user in users:
                databases.writeto('balance',user,';','','.txt')
                databases.writeto('balance',users[user],';','','.txt')

def bankInfo(username, mainWindow):
        
        '''Banking Details'''

        global users
        
        mainWindow.destroy()
        
        window = tkinter.Tk()
        window.title("Banking")
        window.geometry("250x250")
        window.configure(background='gray')
        label3 = tkinter.Label(window, text = username.title() + "'s Balance: " + str(users[username.upper()]))
        label3.place(x=125, y=80, anchor="center")
        logout = tkinter.Button(window, text='Logout',command=lambda: main(window))
        logout.grid(row=0)
        window.mainloop()


def checkPass(userLogin, userPass, mainWindow):

        '''Checks the password'''
        
        nonce = False

        try:
                userLogin.upper()
        except:
                messagebox.showinfo('FAILURE','Incorrect Username')
                nonce = True

        

        if usernames[userLogin.upper()] == hash(userPass) and nonce == False:
                bankInfo(userLogin, mainWindow)
        else:
                messagebox.showinfo('FAILURE','Incorrect Password')

def main(root=None):

        '''Main Function'''

        try:
                root.destroy()
        except:
                pass

        getBalance()
        
        window = tkinter.Tk()
        window.title('Login')
        window.geometry("200x150")
        window.configure(background='grey')

        label1 = tkinter.Label(window, text="Username:")


        entry1 = tkinter.Entry(window)


        label2 = tkinter.Label(window, text="Password:")
        entry2 = tkinter.Entry(window, show='*')

        login = tkinter.Button(window, text='Login', command=lambda: checkPass(entry1.get(), entry2.get(), window))

        label1.pack()
        entry1.pack()
        label2.pack()
        entry2.pack()
        login.pack()

        window.mainloop()


if __name__ == '__main__':
        main()
