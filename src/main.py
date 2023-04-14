from flask import Flask, redirect, render_template, url_for, request, session
from flask_sqlalchemy import SQLAlchemy

#setup flask
app = Flask(__name__)
app.secret_key = "#stop_food-wastage-AT_ANY_COST!"

#link db
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
db = SQLAlchemy(app)

#make database tables
class Customer(db.Model):
    __tablename__ = 'customers'
    customer_id = db.Column(db.String(100),unique=True,primary_key=True,nullable=False)
    organisation_id = db.Column(db.String(100),nullable=False)
    room_number = db.Column(db.String(100),nullable=False)
    name = db.Column(db.String(100),nullable=False)

    def __init__(self,customer_id,organisation_id,room_number,name):
        self.customer_id = customer_id
        self.organisation_id = organisation_id
        self.room_number = room_number
        self.name = name

class Manager(db.Model):
    __tablename__ = 'managers'
    organisation_id = db.Column(db.String(100),unique=True,primary_key=True,nullable=False)
    password = db.Column(db.String(100),nullable=False)

    def __init__(self,organisation_id,password):
        self.organisation_id = organisation_id
        self.password = password

#class Orders(db.Model):
    #__tablename__ = 'orders'
    #TODO

@app.route('/register/',methods=["GET","POST"])
def register():
    #register page
    if request.method == "POST":
        print("=> Posted registeration form")
        organisation_id = request.form["hotel_id"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        if password != confirm_password:
            return render_template('register.html')
        mngr = Manager(organisation_id,password)
        db.session.add(mngr)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login/',methods=["GET","POST"])
def login():
    #login page
    if request.method == "POST":
        print("=> Posted login form")
        form = request.form["form_id"]
        if form == 'customer':
            name = request.form["customer_name"]
            organisation_id = request.form["hotel_id"]
            room_number = request.form["room_number"]
            customer_id = organisation_id + room_number
            cstmr = Customer.query.filter_by(customer_id=customer_id).first()
            if not cstmr:
                #TODO request permission from manager
                return render_template("login.html")
            if cstmr.name != name:
                return render_template("login.html")
            session['customer_id'] = customer_id
            session['type'] = 'customer'
            return redirect(url_for('customer_dashboard'))
        elif form == "manager":
            organisation_id = request.form["hotel_id"]
            password = request.form["password"]
            mngr = Manager.query.filter_by(organisation_id=organisation_id).first()
            if not mngr:
                return render_template("login.html")
            if mngr.password != password:
                return render_template("login.html")
            session['organisation_id'] = organisation_id
            session['type'] = 'manager'
            return redirect(url_for('manager_dashboard'))
        return render_template("login.html")
    return render_template('login.html')

@app.route('/')
def root():
    #redirect website url to login page by default
    return redirect(url_for('login'))

if __name__ == '__main__':
    print("=> Starting flask app")
    with app.app_context():
        # create database
        db.create_all()
        print("=> Database created")
    app.run(debug=True)
    print("=> Unmessed is running")
