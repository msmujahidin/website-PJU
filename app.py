from flask import Flask, render_template, request, redirect, url_for, flash, g,  session
from flask_sqlalchemy import SQLAlchemy
import psycopg2


app = Flask(__name__)
app.secret_key = "Secret Key"

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user


#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:D4n0v4@2020@danova.id/smartpju_v1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='nakpisang', password='password'))
users.append(User(id=2, username='zul', password='password'))
users.append(User(id=3, username='rizal', password='password'))

#Creating model table for our CRUD database
class sensor_ac(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    no_gateway = db.Column(db.String(100))
    id_gateway = db.Column(db.String(100))
    no_mc = db.Column(db.String(100))
    id_mc = db.Column(db.String(100))
    tegangan = db.Column(db.String(100))
    arus = db.Column(db.String(100))
    frequensi = db.Column(db.String(100))
    power_factor = db.Column(db.String(100))
    daya = db.Column(db.String(100))
    energi = db.Column(db.String(100))
    status = db.Column(db.String(100))
    waktu = db.Column(db.String(100))



    def __init__(self, no_gateway, id_gateway, no_mc, id_mc, tegangan, arus, frequensi, power_factor, daya, energi, status, waktu):

        self.no_gateway = no_gateway
        self.id_gateway = id_gateway
        self.no_mc = no_mc
        self.id_mc = id_mc
        self.tegangan = tegangan
        self.arus =  arus
        self.frequensi = frequensi
        self.power_factor = power_factor
        self.daya = daya
        self.energi = energi
        self.status = status
        self.waktu = waktu





#This is the index route where we are going to
#query on all our employee data
# @app.route('/')
# def Index():
#     if not g.user:
#         return redirect(url_for('login'))
        
#     all_data = sensor_ac.query.all()

#     return render_template("index.html", employees = all_data)

@app.route('/profile')
def profile():
    all_data = sensor_ac.query.all()
    if not g.user:
        
        return redirect(url_for('login'))
    
    return render_template('index.html', employees = all_data)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        
        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('profile'))

        return redirect(url_for('login'))

    return render_template('login.html')

#this route is for inserting data  to mysql database via html forms
@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == 'POST':

        no_gateway = request.form['no_gateway']
        id_gateway = request.form['id_gateway']
        no_mc = request.form['no_mc']
        id_mc = request.form['id_mc']
        tegangan = request.form['tegangan']
        arus = request.form['arus']
        frequensi = request.form['frequensi']
        power_factor = request.form['power_factor']
        daya = request.form['daya']
        energi = request.form['energi']
        status = request.form['status']
        waktu = request.form['waktu']


        my_data = sensor_ac(no_gateway, id_gateway, no_mc, id_mc, tegangan, atus, frequensi, power_factor, daya, energi, status, waktu)
        db.session.add(my_data)
        db.session.commit()

        flash("Employee Inserted Successfully")

        return redirect(url_for('Index'))


#this is our update route where we are going to update our employee
@app.route('/update', methods = ['GET', 'POST'])
def update():

    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.no_gateway = request.form['no_gateway']
        my_data.id_gateway = request.form['id_gateway']
        my_data.no_mc = request.form['no_mc']
        my_data.id_mc = request.form['id_mc']
        my_data.tegangan = request.form['tegangan']
        my_data.arus = request.form['arus']
        my_data.frequensi = request.form['frequensi']
        my_data.power_factor = request.form['power_factor']
        my_data.daya = request.form['daya']
        my_data.energi = request.form['energi']
        my_data.status = request.form['status']
        my_data.waktu = request.form['waktu']

        db.session.commit()
        flash("Employee Updated Successfully")

        return redirect(url_for('Index'))


#This route is for deleting our employee
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully")

    return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run()
