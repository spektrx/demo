from flask import *
import sql

db = sql.DataBase()


app = Flask(__name__)

app.secret_key = "6bacdb23b74c2e8d9fdf88a7772f1df95706bccfe663a5f12ece1cfa03f2df42" #Тут можно указать любую строку. Этот ключ используется для подписи куки файлов

@app.route("/")
def index():
    
    return render_template("index.html",  username=session.get("username", None))

@app.route("/login", methods=["POST","GET"]) #Если не указывать методы, то будет доступен только GET
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        print(password)
        result = db.login(username, password)
        if result:
            session['username'] = result["username"]
            return render_template("index.html", username=session["username"])
        else:
            return render_template("login.html", result="Неверне имя пользователя или пароль!")
    else:
        return render_template("login.html")
@app.route("/logout")
def logout():
    session["username"] = None
    
    return render_template("index.html", username=session["username"])

@app.route("/reg", methods=["POST","GET"])
def reg():
    if request.method=="POST":
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        agree = request.form['agreeRules']  
        phone= request.form['phoneNumber'] 

        if agree != "on":
            return render_template("reg.html", result="NOT AGREE WITH RULES!")
        if password != request.form['confirmPassword']:
            return render_template("reg.html", result="Пароли не совпадают!")    
        result = db.register(username, password, email, phone)
        if result == "done":
            session['username'] = username
            return render_template("index.html", username=username)
        return render_template("reg.html", result=result)

    else:
        return render_template("reg.html")

@app.route("/createticket", methods=["POST","GET"])    
def createticket():
    tickets = eval(db.getTickets(session.get("username", None)))
    print(tickets, type(tickets))
    if request.method == "POST":
        num = request.form["number"]
        text = request.form["text"]
        db.createTicket(num, text, session["username"])
        tickets = eval(db.getAllTickets()) # В монго мы используем изменяемые Json, а в MySQL свой неизменяемый тип данных. Поэтому придётся вызывать db.getAllTickets() снова
        return render_template("createticket.html", username=session.get("username", None), result="Сообщение успешно доставленно!", tickets=tickets)

    else:
        return render_template("createticket.html", username=session.get("username", None), tickets=tickets)                                
                                                                                                                                            
@app.route("/admin", methods=["POST","GET"]) #дать права админа пользователю: UPDATE users SET permissions = 'admin' WHERE username = 'Имя пользователя';
def admin():
    print(session)
    username = session.get("username", None)
    user = db.getuser(username)
    print(user)
    print(user.get("permissions"))
    if user and "admin" == user.get("permissions"):
        tickets = eval(db.getAllTickets())
        print(tickets)
        if request.method == "POST":
            result = db.editTicket(request.form)
            if result:
                tickets = eval(db.getAllTickets())
                return render_template("admin.html", tickets=tickets)
            else:
                return "wrong query"
        else:
            return render_template("admin.html", tickets=tickets)
    else:
        return "access deny"
    
@app.route("/account", methods=["GET"])
def account():
    tickets = eval(db.getTickets(session.get("username", None)))
    
    user = db.getuser(session.get("username"))
    return render_template("account.html", user=user, tickets=tickets)

@app.route("/about")
def about():
    return render_template("about.html", username=session.get("username"))

@app.route("/rules")
def rules():
    return render_template("rules.html", username=session.get("username"))

@app.route("/contacts")
def contacts():
    return render_template("contacts.html", username=session.get("username"))

if __name__ == '__main__':
    app.run(debug=True, port=5500, host="0.0.0.0")
