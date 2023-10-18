import os
import socket
import sys
from time import sleep
import csv
import datetime
from cryptography.fernet import Fernet
import base64

#class PersonDetials:
#    def __init__(self,username, passw, name, age, status, dob):
#        """ This is where the persons information are stored may be a database that every information of users stored"""
#        self.username = username
#        self.passw = passw
#        self.name = name
#        self.age = age
#        self.status = status
#        self.dob = dob



#display = Display()   -  This class will perform the display the
#after_login = After_Login()
#log_file_func = Log_File_Func()
#encryption = Encryption()
#
#

Author = 'Naoh-Hcl'




class Display:
    def info_of_user(self, username, password, name, age, status, dob):
        """This section used to display all the info of the new Registrated user to confirm their sign up"""
        print("\n")
        print(f"Username:      {username}")
        print(f"Password:      {password}")
        print(f"Name:          {name}")
        print(f"Age:           {age}")
        print(f"status:        {status}")
        print(f"Date Of Brith: {dob}")
        print("\n")

display = Display()

##This is class is used to for the registation for new users
class Registration:
    def __init__(self):
        """This used to store the temparory details of the new user and write the details in the database"""
        self.newuser = None
        pass
    def NewPersonDetail(self):
        username = str(input("Enter Your username:  "))
        password = str(input("Enter Your Password: "))
        name = str(input("Enter Your Name: "))
        age = int(input("Enter Your Age: "))
        status = str(input("Enter Your Status: "))
        dob = input("Enter Your Date Of Birth: ")

        sleep(4)


        display.info_of_user(username, password, name, age, status, dob) ## Display all the info of registation


        ##Confirming the Registration
        confirm = input("Do you want to confirm the Registration(yes/no):  ").lower()
        if confirm == "yes":
            #self.newuser = PersonDetials(username, password, name, age, status, dob)
            sleep(1)
            print("Hold on a second")
            sleep(3)
            print('\n')
            print("Your are Now Registrated in the hands of protector. The DownStream")
            sleep(2)

            cipher_text = encryption.create_key(username, password)

            with open('userdetails.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([username, cipher_text, name, age, status, dob])


            log_file_func.register_log(username, name)


        elif confirm == "no":
            print("Yeah, Let's say Good Byes")
            sleep(2)
            sys.exit()
        else:
            sleep(1)
            print("This is not a joke. Your details are deleted. Follow everystep once again ")
            print("or quit")
            sleep(2)
            sys.exit()


class After_Login:
    """Used for what are the things must occurs after the user is login """
    def test(self, username):
        print(f"it worked {username}")

after_login = After_Login()


class Encryption:
    def __init__(self):
        pass
    def create_key(self, username, password):
        """This function will create a key and save that key for the corresponding user in the user_key.csv file"""
        key = Fernet.generate_key()#Create a random create_key
        with open('user_key.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, key])
        cipher_suit = Fernet(key)
        data_to_encrypt = password.encode()
        cipher_text = cipher_suit.encrypt(data_to_encrypt)
        return cipher_text

encryption = Encryption()



class Decryption:
    def __init__(self):
        pass

    def decrypt_passw(self, username, encrypted_passw):
        with open('user_key.csv', 'r') as user_key:
            user_key_reader = csv.reader(user_key)
            for row in user_key_reader:
                if row[0] == username:
                    key = row[1]
                    cipher_suit = Fernet(key)
                    decrypted_pass = cipher_suit.decrypt(encrypted_passw)
                    decoded_passw = decrypted_pass.decode()
        return decoded_passw

decryption = Decryption()





class Log_File_Func:
    """This class is stored every log function that are used"""
    def __init__(self):
        now = datetime.datetime.now()
        self.exact_time = now.strftime('%Y-%m-%d %H:%M:%S')


    def login_log(self, username):
        """This function will write loging log details in the login_log.txt"""
        now = datetime.datetime.now()
        log_entry = f"{self.exact_time} - User '{username}'"
        with open('login_log.txt', 'a', encoding='utf-8') as log_file:
            log_file.write(log_entry + "\n")

    def register_log(self, username, name):
        """Ehis function will write the new registration log details in the register_log.txt"""
        log_entry = f"{self.exact_time} Username: '{username}' Name: '{name}' "
        with open('register_log.txt', 'a', encoding='utf-8') as register_log:
            register_log.write(log_entry + "\n")



log_file_func = Log_File_Func()




class Main:
    def __init__(self):
        """This section shows what a user can see and can't see"""
        pass
    def choose(self):
        old_or_new = input("Enter 'n' for new registration or 'o' for login to existing account (n/o):  ").lower()
        if old_or_new == "n":
            registration = Registration()
            registration.NewPersonDetail()
        elif old_or_new == "o":
            login_username = input("Enter Your Username: ")
            login_password = input("Enter Your Passowrd: ")
            with open('userdetails.csv',  'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == login_username:
                            encrypted_passw = row[1]
                            decoded_passw = decryption.decrypt_passw(login_username, encrypted_passw)
                            if decoded_passw == login_password:
                                print("successfully logined in")
                                log_file_func.login_log(login_username)
                                return True




if __name__ == '__main__':
    DownStream = Main()
    DownStream.choose()
