from sqlite3 import DatabaseError
from idgenerator import generate
import csv
import os

class Features:
    def user_input(names):

        print('Enter name: ')
        name = basic_input()
        if name == 'exit':
            return

        id = generate(16)
    
        if name in names:
            del names[name]
        names[name] = id

        print('Enter username: ')
        username = basic_input()
        if username == 'exit':
            return

        print('Enter age: ')
        age = basic_input()
        if age == 'exit':
            return

        print('School: ')
        school = basic_input()
        if school == 'exit':
            return

        print('Area of academic specialty: ')
        faculty = basic_input()
        if faculty == 'exit':
            return

        data = {
            'Name': name,
            'Username': username,
            'Age': age,
            'School': school,
            'Faculty': faculty
        }
        return names, name, data, id

    def lookup(names, database):
        tempname = input('Enter name, or "all" to see all existing entries: ')
        if tempname in names.keys():
            id = names[tempname]
            data = database[id]
            print('-'*120)
            for key, value in data.items():
                print(key + ':', value)
            print('-'*120, '\n\n')
            return
        if tempname == 'all':
            print('Existing entries:\n' + '-'*120)
            for name, id in names.items():
                print(name, '\n')
            return
        if tempname not in names.keys():
            print('Name not found.\n\n')

    def delete_entry(names, database):
        tempname = input('Enter name: ')
        if tempname in names.keys():
            id = names[tempname]
            print('Entry found, press y to confirm, n to cancel.')
            if input() == 'y':
                del(database[id])
                del(names[tempname])
                print('-'*120, '\nEntry deleted.\n\n')
                return 

            if input() == 'n':
                return
        else:
            print('Name not found.')
        return

    def wipe(names, database):
        while True:
            print(f'{len(names)} entries found. Enter "Wipe" to confirm, "n" to cancel. Note: this is irreversible.')
            if input() == 'Wipe':
                del database
                del names
                database = {}
                names = {}
                Filemanage.wipe(names, database)
                print('-'*120, '\nEntries deleted.\n\n')
                return database, names

            if input() == 'n':
                break

class Filemanage:
    def save(names, database):
        nameheader = ['Name', 'ID #']
        with open('NameList.csv', 'w+') as f1:
            writer = csv.writer(f1)
            writer.writerow(nameheader) # write the header
            for key, val in names.items():
                writer.writerow([key, val])
        f1.close

        with open('DataList.csv', 'w+') as f2:
            writer = csv.writer(f2)
            for id, data in database.items():
                writer.writerow([id])
                for key, value in data.items():
                    writer.writerow([key, value])
        f2.close
                
        print('Data saved successfully.')

    def read_data():
        database = {}
        data = {}
        id = None
        f1 = open('DataList.csv', 'r')
        length = len(f1.readlines())
        if length > 1:
            f1.seek(0)
            for i in range(0, length):
                info = f1.readline()
                info = info.replace('\n','')
                if info == '' or info == ',': 
                    pass
                elif info != ',' or info != '':
                    if ',' in info:
                        key, val = info.split(',')
                    else:
                        key = info; val = ''
                    if val == '':
                        if id != None:
                            database[id] = data
                            del data
                            data = {}
                        id = key
                    else:
                        data[key] = val
            database[id] = data
            f1.close
        else:
            database = {}
        return database

    def read_names():
        names = {}
        id = None
        f1 = open('NameList.csv', 'r')
        length = len(f1.readlines())
        if length > 3:
            f1.seek(0)
            for i in range(0, length):
                info = f1.readline()
                info = info.replace('\n','')

                if info != '':
                    key, val = info.split(',')
                    if val != 'ID #':
                        name = key
                        id = val
                        names[name] = id
            f1.close
        else:
            names = {}
            print('No existing Database.')
        return names

    def wipe(names, database):
        os.remove('NameList.csv')
        os.remove('DataList.csv')
        Filemanage.save(names, database)

def Directory(names, database):
    direct = {
        '"lookup"': 'Checking for existing entries using the exact name entered.',
        '"input"': 'Create a new entry, if a current entry exists under the same name, new entry will replace older one.',
        '"save"': 'Save all new entries. Adviced if any new entries are made.',
        '"delete"': 'Delete a specific entry using the exact name entered.',
        '"wipe"': 'Clear all existing entries, cannot be undone.',
        '"exit"': 'Exit out the program.'
    }
    while True:
        main = input('Enter command: ')
        print('\n\n')

        if main == 'help':
            print('DIRECTORY\n', '-'*120)
            for key, val in direct.items():
                print(key, '=>', val,)
            print('\n\n')

        elif main == 'input':
            (names, name, data, id) = Features.user_input(names)
            while True:
                    print('-'*150)
                    for key, val in data.items():
                        print(key + ':', val)
                    print('-'*150)

                    print('Is everything correct? (y/n)')
                    logic = input()
                    if logic == 'n':
                        del data
                        del names[name]
                        (names, name, data, id) = Features.user_input(names)

                    if logic == 'y':
                        database[id] = data
                        print('\n\nEntry saved.\n\n')
                        break

        elif main == 'lookup':
            Features.lookup(names, database)

        elif main == 'save':
            Filemanage.save(names, database)
            print(f'There are now {len(names)} entries.')

        elif main == 'exit':
            out = 'exit'
            break

        elif main == 'delete':
            Features.delete_entry(names, database)
        
        elif main == 'wipe':
            names, database = Features.wipe(names, database)

        else:
            pass
    return out

def basic_input():
    ans = input()
    if ans == 'exit' or ans == 'quit' or ans == 'cancel':
        ans = 'exit'
    return ans


if __name__ == '__main__':
    names = Filemanage.read_names()
    database = Filemanage.read_data()
    size = len(names)
    print(
            f'\n\n\nWelcome to the database! \nThere are {size} entries. \n'+'-'*120
    )
    while True:
        print('Enter "help" for directory.\n')
        if Directory(names, database) == 'exit':
            break
    




        
        
