from flask import Flask, render_template
from flask import  request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identifiant = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service = db.Column(db.String(255), nullable=False)
    depense = db.relationship('service', backref='depense')
    recette = db.relationship('service', backref='recette')


class Depense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plan_compta = db.Column(db.Integer, nullable=False)
    beneficiaire = db.Column(db.Integer, nullable=False)
    montant = db.Column(db.Integer, nullable=False)
    motif = db.Column(db.String(255), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))



class Recette(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plan_compta = db.Column(db.Integer, nullable=False)
    montant = db.Column(db.Integer, nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))



@app.route("/")
def home():
    return render_template('index.html')

@app.route("/form")
def form():
    return render_template('pages/form.html')

@app.route("/service")
def service():
    return render_template('pages/service.html')

@app.route("/form_depense")
def form_depense():
    return render_template('pages/form_depense.html')

@app.route("/form_recette")
def form_recette():
    return render_template('pages/form_recette.html')

@app.route("/depense")
def service_depense():
    return render_template('pages/tab_depense.html')

@app.route("/recette")
def service_recette():
    return render_template('pages/tab_recette.html')

'''Les pages services'''
@app.route("/abattage")
def abattage():
    return render_template('pages/abattage.html')

@app.route("/betail")
def betail():
    return render_template('pages/betail.html')

@app.route("/loyer")
def loyer():
    return render_template('pages/loyer.html')

@app.route("/generale")
def generale():
    return render_template('pages/generale.html')

'''Les pages services'''


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)