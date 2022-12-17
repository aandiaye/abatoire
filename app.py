from flask import Flask, render_template
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


@app.route("/service")
def service():
    return render_template('pages/service.html')


@app.route("/form_depense")
def form_depense():
    return render_template('pages/form_depense.html')


@app.route("/form_recette")
def form_recette():
    return render_template('pages/form_recette.html')


@app.route("/service_depense")
def service_depense():
    return render_template('pages/service_depense.html')


@app.route("/service")
def service():
    return render_template('pages/service.html')

@app.route("/form_depense")
def form_depense():
    return render_template('pages/form_depense.html')

@app.route("/form_recette")
def form_recette():
    return render_template('pages/form_recette.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
<<<<<<< HEAD
    app.run(debug=True)
=======
    app.run(debug=True)
>>>>>>> main
