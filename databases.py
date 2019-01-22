'''

Databases Module: a database module for python
Version 1.1b - 1. 1. 2018

Copyright (C) 2018 Imaad Farooqui

This software is provided 'as-is', without any express or implied
warranty. In no event will the authors be held liable for any damages
arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it
freely, subject to the following restrictions:

1. The origin of this software must not be misrepresented; you must not
   claim that you wrote the original software. If you use this software
   in a product, an acknowledgment in the product documentation would be
   appreciated but is not required.
2. Altered source versions must be plainly marked as such, and must not be
   misrepresented as being the original software.
3. This notice may not be removed or altered from any source distribution.

'''

'''
'''

'''

How To Import:

from . import databases

Or choose which functions via:

import databases
from databases import createdatabase, cleardatabase, writeto, readto, copytoclipboard, pastefromclipboard, clearclipboard, deleteitemofclipboard

How to use functions:

initdatabase()
clearclipboard(1)
deleteitemofclipboard(1)
pastefromclipboard('test',1,'tester/','.json')
copytoclipboard('test',';','tester/','.json')
createdatabase('test','tester/','.json')
cleardatabase('test','tester/','.json')
writeto('test','Testing123',';','tester/','.json')
readto('test',';','tester/','.json')

How to use:

Add databases.py to the same directary as your main .py file
Then import the functions explained above
Then use the functions also explained above

'''

def initdatabase():

    '''Initalizes database module'''

    # Example: initdatabase()

    createdatabase('clipboard')
    cleardatabase('clipboard')
    
    writeto('clipboard','CLIPBOARD:\n')
        
def clearclipboard(newline=0):

    '''Clears the clipboard'''

    # Example: clearclipboard(1)

    cleardatabase('clipboard')

    if(str(newline) == '1'):
        writeto('clipboard','CLIPBOARD:')
    else:
        writeto('clipboard','CLIPBOARD:\n')

def deleteitemofclipboard(item=1):

    '''Deletes a certain item from the clipboard'''

    # Example: deleteitemofclipboard(1)

    try:
        int(item)
    except:
        return None

    _data = readto('clipboard')
    
    if(item == 0 or item > len(_data)-1):
       return None
       
    del _data[int(item)]
    del _data[0]
       
    clearclipboard(1)
       
    for items in _data:
        writeto('clipboard',items)

    _data = None
    
def copytoclipboard(name,key='\n',directory='',filetype='.txt'):

    '''Copies a database to the clipboard'''

    # Example: copytoclipboard('test',';','tester/','.json')

    name = str(name)
    key = str(key)
    directory = str(directory)
    filetype = str(filetype)

    _data = readto(name,key,directory,filetype)
    
    if(key == '\n'):
        writeto('clipboard','/n',';')
    else:
        writeto('clipboard',str(key),';')
    
    for items in _data:
        writeto('clipboard',str(items),';')
        
    writeto('clipboard','')

    _data = None

def pastefromclipboard(name,item=1,directory='',filetype='.txt'):

    '''Pastes an item from the clipboard to a new database'''

    # Example: pastefromclipboard('test',1,'tester/','.json')

    try:
        int(item)
    except:
        return None

    _data = readto('clipboard')
    
    if(item == 0 or item > len(_data)-1):
       return None

    _data = _data[int(item)]

    writeto(name,'','\n',directory,filetype)

    _data = _data.split(';')
    del _data[0]

    key = _data[0]
    
    if(key == '/n'):
        key = '\n'

    del _data[0]

    for items in _data:
        writeto(name,items,key,directory,filetype)

    _data = None        

def createdatabase(name,directory='',filetype='.txt'):

    '''Creates a database which stores infomation'''

    # Example: createdatabase('test','tester/','.json')

    name = str(name)
    directory = str(directory)
    filetype = str(filetype)
    
    try:
        open(directory+name+filetype, 'a')
    except:
        pass

def cleardatabase(name,directory='',filetype='.txt'):

    '''Clears a database which stores infomation'''

    # Example: cleardatabase('test','tester/','.json')

    name = str(name)
    directory = str(directory)
    filetype = str(filetype)

    try:
        open(directory+name+filetype, 'w')
    except:
        pass

def writeto(name,text,key='\n',directory='',filetype='.txt'):

    '''Writes infomation to a given database'''

    # Example: writeto('test','Testing123',';','tester/','.json')

    name = str(name)
    directory = str(directory)
    filetype = str(filetype)
    text = str(text)

    empty = []
    repeat = 0

    try:
        with open(directory+name+filetype,'r') as file:
            for line in file:
                for word in line.split():
                    if(repeat < 3):
                        empty.append(word)
                        repeat += 1
                    else:
                        break
                        empty = ['fail','fail']
                   

        if(not empty):
            with open(directory+name+filetype,'a') as file:
                file.write(text)
                file.close()
        else:
            with open(directory+name+filetype,'a') as file:
                file.write(key+text)
                file.close()
    except:
        pass

def readto(name,key='\n',directory='',filetype='.txt'):

    '''Reads infomation to a given database'''

    # Example: readto('test',';','tester/','.json')

    
    name = str(name)
    directory = str(directory)
    filetype = str(filetype)

    data = []
    repeat = 0

    try:
        with open(directory+name+filetype,'r') as file:
            for line in file:
                for word in line.split(key):
                    if(key == '\n'):
                        if(repeat % 2 == 0):
                            data.append(word)
                        repeat += 1
                    else:
                        data.append(word)
        return data
    except:
        pass
    


if(__name__ == '__main__'):
    pass
    



    
