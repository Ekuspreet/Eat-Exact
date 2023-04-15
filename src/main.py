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
    accepted = db.Column(db.Boolean,nullable=False)
    solly_key = db.Column(db.String,nullable=False)

    def __init__(self,customer_id,organisation_id,room_number,name,accepted,solly_key):
        self.customer_id = customer_id
        self.organisation_id = organisation_id
        self.room_number = room_number
        self.name = name
        self.accepted = accepted
        self.solly_key = solly_key

class Manager(db.Model):
    __tablename__ = 'managers'
    organisation_id = db.Column(db.String(100),unique=True,primary_key=True,nullable=False)
    organisation_name = db.Column(db.String(100),nullable=False)
    organisation_order_limit = db.Column(db.Integer,nullable=False)
    password = db.Column(db.String(100),nullable=False)

    def __init__(self,organisation_id,organisation_name,organisation_order_limit,password):
        self.organisation_id = organisation_id
        self.organisation_name = organisation_name
        self.organisation_order_limit = organisation_order_limit
        self.password = password

class Order(db.Model):
    __tablename__ = 'orders'
    customer_id = db.Column(db.String(100),unique=True,primary_key=True,nullable=False)
    order_source = db.Column(db.String(100),nullable=False)
    order_amount = db.Column(db.Float, nullable=False)
    order_string = db.Column(db.String(512),nullable=True)

    def __init__(self,customer_id,order_source,order_amount,order_string):
        self.customer_id = customer_id
        self.order_source = order_source
        self.order_amount = order_amount
        self.order_string = order_string

class Item(db.Model):
    __tablename__ = 'items'
    item_id = db.Column(db.String(100),unique=True,primary_key=True,nullable=False)
    item_source = db.Column(db.String(100),nullable=False)
    item_name = db.Column(db.String(100),nullable=False)
    item_type = db.Column(db.String(10),nullable=False)
    item_image = db.Column(db.String(50),nullable=True)
    item_price = db.Column(db.Float, nullable=False)
    item_limit = db.Column(db.Integer, nullable=False)

    def __init__(self,item_id,item_source,item_name,item_type,item_image,item_price,item_limit):
        self.item_id = item_id
        self.item_source = item_source
        self.item_name = item_name
        self.item_type = item_type
        self.item_image = item_image
        self.item_price = item_price
        self.item_limit = item_limit

@app.route('/<customer_id>/profile/',methods=["GET","POST"])
def customer_profile(customer_id):
    cstmr = Customer.query.filter_by(customer_id=customer_id).first()
    if request.method == "POST":
        name = request.form['name']
        room_number = request.form['room_number']
        solly_key = request.form['solly_key']
        cstmr.name = name
        cstmr.room_number = room_number
        cstmr.solly_key = solly_key
        db.session.commit()
    return render_template('profile_page.html',customer=cstmr)

@app.route('/<customer_id>/dashboard/',methods=["GET","POST"])
def customer_dashboard(customer_id):
    order = Order.query.filter_by(customer_id=customer_id).first()
    items = []
    balance_limit = Manager.query.filter_by(organisation_id=order.order_source).first().organisation_order_limit
    for item in order.order_string.split(','):
        quantity = item.split(' ')[1]
        itm = Item.query.filter_by(item_id=int(item.split(' ')[0])).first()
        if not itm:
            continue
        name = itm.item_name
        price = itm.item_price
        limit = itm.item_limit
        total = int(price) * int(quantity)
        items.append({"name":name,"quantity":quantity,"price":price,"limit":limit,"total":total})
    cstmr = Customer.query.filter_by(customer_id=customer_id).first()
    org_name = Manager.query.filter_by(organisation_id=int(cstmr.organisation_id)).first().organisation_name
    return render_template('customer_dashboard.html',order=order,items=items,balance_limit=balance_limit,customer_name=cstmr.name,institution_name=org_name,room_number=cstmr.room_number)

@app.route('/<organisation_id>/manager/dashboard/',methods=["GET","POST"])
def manager_dashboard(organisation_id):
    logins = Customer.query.filter_by(organisation_id=int(organisation_id))
    requests = logins.filter_by(accepted=False)
    items = Item.query.filter_by(item_source=int(organisation_id))
    orders = Order.query.filter_by(order_source=int(organisation_id))
    freq = {}
    names = {}
    if request.method == "POST":
        for req in requests:
            if not req.customer_id in request.form.keys():
                continue
            status = request.form[req.customer_id]
            if status == "accept":
                req.accepted = True
            else:
                db.session.delete(req)
        db.session.commit()
    for order in orders:
        for item in order.order_string.split(','):
            if item.split(' ')[0] == "":
                continue
            quantity = item.split(' ')[1]
            itm = Item.query.filter_by(item_id=int(item.split(' ')[0])).first()
            if not itm:
                continue
            if itm.item_id in freq:
                freq[itm.item_id] += int(quantity)
            else:
                freq[itm.item_id] = int(quantity)
    for item in items:
        if not item.item_id in freq:
            freq[item.item_id] = 0
        names[item.item_id] = item.item_name
    reqs = {}
    for order in orders:
        cstmr = Customer.query.filter_by(customer_id=order.customer_id).first()
        reqs[order.customer_id] = {}
        reqs[order.customer_id]['name'] = cstmr.name
        reqs[order.customer_id]['room'] = cstmr.room_number
        st = ""
        for pair in order.order_string.split(','):
            itm = Item.query.filter_by(item_id=int(pair.split()[0])).first()
            st += itm.item_name + " x" + pair.split()[1] + ", "
        reqs[order.customer_id]['string'] = st
    return render_template('manager_dashboard.html',logins=logins, freq=freq,names=names,orders=orders,reqs=reqs)

@app.route('/<organisation_id>/manager/menu/',methods=["GET","POST"])
def manager_menu(organisation_id):
    return render_template('manager_menu.html')

@app.route('/register/',methods=["GET","POST"])
def register():
    #register page
    if request.method == "POST":
        print("=> Posted registeration form")
        organisation_id = request.form["organisation_id"]
        organisation_name = request.form['organisation_name']
        organisation_order_limit = request.form['organisation_order_limit']
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        if password != confirm_password:
            return render_template('register.html')
        mngr = Manager(organisation_id,organisation_name,organisation_order_limit,password)
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
            organisation_id = request.form["organisation_id"]
            room_number = request.form["room_number"]
            customer_id = organisation_id + room_number
            cstmr = Customer.query.filter_by(customer_id=customer_id).first()
            if not cstmr:
                cstmr = Customer(customer_id,organisation_id,room_number,name,False)
                db.session.add(cstmr)
                db.session.commit()
                return render_template("login.html")
            if cstmr.accepted == False:
                print("NOT WELCOME")
                return render_template("login.html")
            if cstmr.name != name:
                return render_template("login.html")
            session['customer_id'] = customer_id
            session['type'] = 'customer'
            return redirect(url_for('customer_dashboard',customer_id=customer_id))
        elif form == "manager":
            organisation_id = request.form["organisation_id"]
            password = request.form["password"]
            mngr = Manager.query.filter_by(organisation_id=int(organisation_id)).first()
            if not mngr:
                return render_template("login.html")
            if mngr.password != password:
                return render_template("login.html")
            session['organisation_id'] = organisation_id
            session['type'] = 'manager'
            return redirect(url_for('manager_dashboard',organisation_id=organisation_id))
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
    print("=> Eat Exact is running")
