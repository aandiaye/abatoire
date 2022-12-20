<<<<<<< Updated upstream
from flask import Flask, render_template, request, redirect
from datetime import datetime
=======
from flask import Flask, render_template, flash
from flask import  request
>>>>>>> Stashed changes
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.app_context()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
# initialize the app with the extension
db.init_app(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identifiant = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)






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
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    def __init__(self, plan_compta,beneficiaire,montant,motif,date):
        self.plan_compta = plan_compta
        self.beneficiaire = beneficiaire
        self.montant = montant
        self.motif = motif



class Recette(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plan_compta = db.Column(db.Integer, nullable=False)
    montant = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))


<<<<<<< Updated upstream
=======
@app.route("/add_service", methods=["GET", "POST"])
def add_service():
    if request.method == "POST":
        service = Service(
            service=request.form["firstname"])
        db.session.add(service)
        db.session.commit()
        flash("You are registered and can now login", "success")
        # return redirect(url_for('login'))
    else:
        flash("user already existed, please login or contact admin", "danger")


>>>>>>> Stashed changes
@app.route("/")
def home():
    return render_template('index.html')

@app.route("/form")
def form():
    return render_template('pages/form.html')


@app.route("/service")
def service():
    return render_template('pages/service.html')

@app.route("/form_depense",methods=['GET', 'POST'])
def form_depense():
    if request.method=="POST":
        plan_compta= request.form["plan_compta"]
        beneficiaire= request.form["beneficiaire"]
        montant= request.form["montant"]
        motif = request.form["motif"]
        depense_form=Depense(plan_compta=plan_compta, beneficiaire=beneficiaire, montant=montant, motif=motif)
        try:
            db.session.add(depense_form)
            db.session.commit()
            return redirect('/')
        except Exception:
            return "Une erreure s'est produite"
    else:
        return render_template('pages/form_depense.html')

@app.route("/form_recette")
def form_recette():
    return render_template('pages/form_recette.html')

@app.route("/depense",methods=['GET', 'POST'])
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

'''Les pages loyer'''
@app.route("/list_recette")
def list_recette():
    return render_template('pages/loyer/list_recette.html')

@app.route("/list_depense")
def list_depense():
    return render_template('pages/loyer/list_depense.html')

@app.route("/loyer_form_depense")
def loyer_form_depense():
    return render_template('pages/loyer/loyer_form_depense.html')

@app.route("/loyer_form_recette")
def loyer_form_recette():
    return render_template('pages/loyer/loyer_form_recette.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)