import mysql.connector
import hashlib
import datetime
import json

def hash_password(password):
    hash_object = hashlib.sha256()
    password_bytes = password.encode('utf-8')
    hash_object.update(password_bytes)
    hashed_password = hash_object.hexdigest()
    return hashed_password

class DataBase:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="stuk_stuk"
        )
        self.cursor = self.db.cursor(dictionary=True)

    def login(self, username, password):
        password = hash_password(password)
        self.cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        result = self.cursor.fetchone()
        if result:
            return json.dumps({"username": result["username"]})
        else:
            return json.dumps(None)

    def register(self, username, password, email, phone):
        password = hash_password(password)
        self.cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if self.cursor.fetchone():
            return json.dumps("Данное имя пользователя уже используется!")

        self.cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if self.cursor.fetchone():
            return json.dumps("Данная почта уже используется!")

        self.cursor.execute("SELECT * FROM users WHERE phone = %s", (phone,))
        if self.cursor.fetchone():
            return json.dumps("Данный номер телефона уже используется!")

        query = "INSERT INTO users (username, password, email, phone) VALUES (%s, %s, %s, %s)"
        values = (username, password, email, phone)
        self.cursor.execute(query, values)
        self.db.commit()
        return json.dumps("done")

    def getuser(self, username):
      self.cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
      result = self.cursor.fetchone()
      if result:
            return {"username": result["username"], "email": result["email"], "phone": result["phone"], "permissions":result["permissions"]}
      else:
            return None

    def createTicket(self, number, text, username):
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = "INSERT INTO tickets (number, text, username, status, date) VALUES (%s, %s, %s, %s, %s)"
        values = (number, text, username, "New", date)
        self.cursor.execute(query, values)
        self.db.commit()

    def getTickets(self, username):
        self.cursor.execute("SELECT * FROM tickets WHERE username = %s", (username,))
        result = self.cursor.fetchall()
        return json.dumps([{"id": ticket["id"], "number": ticket["number"], "text": ticket["text"], "username": ticket["username"], "status": ticket["status"], "date": str(ticket["date"])} for ticket in result])

    def getAllTickets(self):
        self.cursor.execute("SELECT * FROM tickets")
        result = self.cursor.fetchall()
        return json.dumps([{"id": ticket["id"], "number": ticket["number"], "text": ticket["text"], "username": ticket["username"], "status": ticket["status"], "date": str(ticket["date"])} for ticket in result])

    def editTicket(self, data):
      todo = data["select"]
      if todo == "done" or todo == "reject":
            query = "UPDATE tickets SET status = %s WHERE id = %s"
            values = (todo, data["_id"])
            self.cursor.execute(query, values)
            self.db.commit()
            return True
      elif todo == "delete":
            query = "DELETE FROM tickets WHERE id = %s"
            values = (data["_id"],)
            self.cursor.execute(query, values)
            self.db.commit()
            return True
      else:
            return False
