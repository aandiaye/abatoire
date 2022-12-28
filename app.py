from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
# app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
# app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# initialize the app with the extension
# db.init_app(app)
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identifiant = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.today())


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service = db.Column(db.String(20))
    depense = db.relationship('Depense', backref='service', lazy=True)
    recette = db.relationship('Recette', backref='service', lazy=True)


class Depense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plan_compta = db.Column(db.Integer, nullable=False)
    beneficiaire = db.Column(db.Integer, nullable=False)
    montant = db.Column(db.Integer, nullable=False)
    motif = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))

    # def __init__(self,plan_compta,beneficiaire,montant,motif,service):
    #     self.plan_compta=plan_compta
    #     self.beneficiaire=beneficiaire
    #     self.montant=montant
    #     self.motif=motif
    #     self.service_id=Service.depense
        

class Recette(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plan_compta = db.Column(db.Integer, nullable=False)
    montant = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.today())
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))

@app.route("/add_service", methods=["GET", "POST"])
def add_service():
    if request.method == "POST":
        service = Service(
            service=request.form["service"])
        db.session.add(service)
        db.session.commit()

        return render_template('pages/loyer/loyer_form_recette.html')
    else:
        return render_template('pages/loyer/loyer_form_recette.html')


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/form")
def form():
    return render_template('pages/form.html')


@app.route("/service")
def service():
    return render_template('pages/service.html')


@app.route("/form_depense", methods=['GET', 'POST'])
def form_depense():
    if request.method == "POST":
        plan_compta = request.form["plan_compta"]
        beneficiaire = request.form["beneficiaire"]
        montant = request.form["montant"]
        motif = request.form["motif"]
        depense_form = Depense(plan_compta=plan_compta, beneficiaire=beneficiaire, montant=montant, motif=motif)
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


@app.route("/depense", methods=['GET', 'POST'])
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

'''Les pages loyer'''


@app.route("/list_recette")
def list_recette():
    return render_template('pages/loyer/list_recette.html')


@app.route("/loyer_form_recette")
def loyer_form_recette():
    return render_template('pages/loyer/loyer_form_recette.html')


@app.route("/list_depense")
def list_depense():
    depenses = Depense.query.all()
    return render_template('pages/loyer/list_depense.html', depenses=depenses)


@app.route("/loyer_form_depense")
def loyer_form_depense():
    return render_template('pages/loyer/loyer_form_depense.html')


@app.route("/form_update_depense")
def form_update():
    return render_template('pages/loyer/form_update_depense.html')


@app.route("/add_loyer_depense", methods=["GET", "POST"])
def add_loyer_depense():
    if request.method == "POST":
        service=Service(service)
        depense = Depense(
            
            plan_compta=request.form["plan_compta"],
            beneficiaire=request.form['beneficiaire'],
            montant=request.form['montant'],
            motif=request.form['motif'],
            service_id =request.form['service'],
        )
        db.session.add(depense)
        db.session.commit()
        return redirect('list_depense')
    return render_template('pages/loyer/loyer_form_depense.html')


@app.route("/delete/<int:id>", methods=["GET", "POST"])
def delete(id):
    if request.method == "GET":
        delete_depense = Depense.query.filter_by(id=id).first()
        db.session.delete(delete_depense)
        db.session.commit()
        return redirect('/list_depense')
    return render_template('pages/loyer/list_depense.html')


# @app.route("/update_depense_loyer/<int:id>")
# def update_depense_loyer(id):
#     update = Depense.query.filter_by(id=id).first()
#     return render_template('pages/loyer/loyer_form_depense.html', update=update)

@app.route("/update_depense_loyer/<int:id>/", methods=["GET", "POST"])
def update(id):
    depenses = Depense.query.get_or_404(id)
    if request.method == "POST":
        updates = Depense.query.filter_by(id=id).first()
        updates.id = id
        updates.beneficiaire = request.form['beneficiaire']
        updates.plan_compta = request.form['plan_compta']
        updates.motif = request.form['motif']
        updates.montant = request.form['montant']
        updates.service_id = request.form['service']
        db.session.commit()
        return redirect('/list_depense')
    elif request.method == "GET":
        return render_template('pages/loyer/update_depense_loyer.html', depenses=depenses)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
