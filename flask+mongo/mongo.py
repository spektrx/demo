from pymongo import *
import datetime
import random
import hashlib
from bson.objectid import ObjectId


def hash_password(password):
    #Создаём объект хэша каждый раз!
    hash_object = hashlib.sha256()
    # Преобразуем пароль в байтовую строку, так как объект хэша принимает только байты
    password_bytes = password.encode('utf-8')
    # Обновляем объект хэша с байтами пароля
    hash_object.update(password_bytes)
    # Получаем хэш в шестнадцатеричном формате
    hashed_password = hash_object.hexdigest()
    return hashed_password


class DataBase:
        def __init__(self):
                
                cluster = MongoClient("тут укажите ссылку на кластер")


                self.db = cluster["stuk-stuk"] #Имя базы данных
                   # В безе данных нужно создать 2 коллекции "users" и "tickets" Их заполнять не нужно, только создать. (спасибо Монго)
                self.users = self.db["users"] 
                self.tickets = self.db["tickets"]
         

                print("db_init")
            
        def login(self, username, password):
            print(password)
            password = hash_password(password)
            print(password)
            return self.users.find_one({"username":username, "password":password})
        
        def register(self, username, password, email, phone):

            if (self.users.find_one({"username":username})):
                  return "Данное имя пользователя уже используется!"
            if (self.users.find_one({"email":email})):
                  return "Данная почта уже используется!"
            if (self.users.find_one({"phone":phone})):
                  return "Данный номер телефона уже используется!"

            user = {
                    "username":username,
                    "email":email,
                    "password": hash_password(password),
                    "phone":phone,
                    "permissions":[]
              }
            self.users.insert_one(user)

            return "done"
        def getuser(self, username):
              return self.users.find_one({"username":username})
        
        def createTicket(self, number, text, username):
              ticket = {
                    "username":username,
                    "text":text,
                    "number":number,
                    "status":"New",
                    "date":datetime.datetime.now()
              }
              self.tickets.insert_one(ticket)

        def getTickets(self, username):
              return self.tickets.find({"username":username})
        
        def getAllTickets(self):
              return self.tickets.find({})
        
        def editTicket(self, data):
            print(data)
            todo = data["select"]
            print(data["_id"])
            print(todo)
            if todo == "done" or todo == "reject":
                  self.tickets.find_one_and_update({"_id": ObjectId(data["_id"])}, {"$set":{"status":todo}})
                  return True
            elif todo == "delete":
                  self.tickets.delete_one({"_id": ObjectId(data["_id"])})
                  return True
            
            