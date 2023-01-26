from datetime import datetime
from flask import Flask, render_template, redirect, url_for,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['SECRET_KEY'] = 'mysecretkey'
db.init_app(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identifiant = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow().strftime("%d-%m-%Y"))


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service = db.Column(db.String(20))
    depense = db.relationship('Depense', backref='service', lazy=True)
    recette = db.relationship('Recette', backref='service', lazy=True)
    service = db.Column(db.String(255), nullable=False)
    depense = db.relationship('Depense', backref='service')
    recette = db.relationship('Recette', backref='Service')


class Depense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plan_compta = db.Column(db.Integer, nullable=False)
    beneficiaire = db.Column(db.Integer, nullable=False)
    montant = db.Column(db.Integer, nullable=False)
    motif = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow().strftime("%d-%m-%Y"))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    type_table = db.Column(db.String(10), default='depense')


class Recette(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plan_compta = db.Column(db.Integer, nullable=False)
    montant = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow().strftime("%d-%m-%Y"))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    type_table = db.Column(db.String(10), default='recette')


#
# @app.route("/login", methods=["POST", "GET"])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = Users.query.filter_by(identifiant=form.identifiant.data).first()
#         if user:
#             if bcrypt.check_password_hash(user.password, form.password.data):
#                 load_user(user)
#                 return redirect(url_for('tab_afficher_depense_abattage'))
#     return render_template('pages/betails/login.html', form=form)
#
#
# @app.route("/", methods=["POST", "GET"])
# def register():
#     form = RegisterForm()
#
#     if form.validate_on_submit():
#         hash_password = bcrypt.generate_password_hash(form.password.data)
#         new_identifiant = Users(identifiant=form.identifiant.data, password=hash_password)
#         db.session.add(new_identifiant)
#         db.session.commit()
#         return redirect(url_for('login'))
#     return render_template('pages/betails/register.html', form=form)
#
#
# @app.route("/logout", methods=["GET", "POST"])
# def logout():
#     logout_user()
#     return redirect(url_for('login'))
#


@app.route("/")
def index():
    return render_template('index.html')


'''Les pages abattage'''
@app.route("/add_depense_abattage", methods=["GET", "POST"])
def add_depense_abattage():
    if request.method == "POST":
        depense = Depense(
            plan_compta=request.form['plan_compta'],
            beneficiaire=request.form['beneficiaire'],
            montant=request.form['montant'],
            motif=request.form['motif'],
            service_id=request.form['service'])
        db.session.add(depense)
        db.session.commit()
    return render_template("pages/abattage/add_depense_abattage.html")


@app.route("/add_recette_abattage", methods=["GET", "POST"])
def add_recette_abattage():
    if request.method == "POST":
        recette = Recette(
            plan_compta=request.form['plan_compta'],
            montant=request.form['montant'],
            service_id=request.form['service'],
        )
        db.session.add(recette)
        db.session.commit()
    return render_template('pages/abattage/add_recette_abattage.html')


@app.route("/tab_depense_abattage")
def tab_depense_abattage():
    total_depense_abattage = db.session.query(func.sum(Depense.montant)).filter(
        Depense.service_id == 'abattage').scalar()
    depenses = db.session.query(Depense).filter(Depense.service_id == "abattage").all()
    return render_template("pages/abattage/tab_depense_abattage.html", depenses=depenses,total_depense_abattage=total_depense_abattage)


@app.route("/tab_recette_abattage")
def tab_recette_abattage():
    total_recette_abattage = db.session.query(func.sum(Recette.montant)).filter(
        Recette.service_id == 'abattage').scalar()
    recettes = db.session.query(Recette).filter(Recette.service_id == "abattage").all()
    return render_template('pages/abattage/tab_recette_abattage.html', recettes=recettes,total_recette_abattage=total_recette_abattage)


@app.route("/update_recette_abattage/<int:recette_id>", methods=["GET", "POST"])
def update_recette_abattage(recette_id):
    recette = Recette.query.filter_by(id=recette_id).first()
    if request.method == "POST":
        plan_compta = request.form['plan_compta']
        montant = request.form['montant']
        recette.plan_compta = plan_compta
        recette.montant = montant
        db.session.add(recette)
        db.session.commit()
        return redirect(url_for('tab_recette_abattage'))
    return render_template('pages/abattage/update_recette_abattage.html', recette=recette)


@app.route("/update_depense_abattage/<int:depense_id>", methods=["GET", "POST"])
def update_depense_abattage(depense_id):
    depense = Depense.query.filter_by(id=depense_id).first()
    if request.method == "POST":
        beneficiaire = request.form['beneficiaire']
        plan_compta = request.form['plan_compta']
        motif = request.form['motif']
        montant = request.form['montant']
        depense.plan_compta = plan_compta
        depense.beneficiaire = beneficiaire
        depense.motif = motif
        depense.montant = montant
        db.session.add(depense)
        db.session.commit()
        return redirect(url_for('tab_depense_abattage'))
    return render_template('pages/abattage/update_depense_abattage.html', depense=depense)


'''Les pages betail'''
@app.route("/add_depense_betail", methods=["GET", "POST"])
def add_depense_betail():
    if request.method == "POST":
        depense = Depense(
            plan_compta=request.form['plan_compta'],
            beneficiaire=request.form['beneficiaire'],
            montant=request.form['montant'],
            motif=request.form['motif'],
            service_id=request.form['service'])
        db.session.add(depense)
        db.session.commit()
    return render_template("pages/betail/add_depense_betail.html")


@app.route("/add_recette_betail", methods=["GET", "POST"])
def add_recette_betail():
    if request.method == "POST":
        recette = Recette(
            plan_compta=request.form['plan_compta'],
            montant=request.form['montant'],
            service_id=request.form['service'],
        )
        db.session.add(recette)
        db.session.commit()
    return render_template('pages/betail/add_recette_betail.html')


@app.route("/tab_depense_betail")
def tab_depense_betail():
    total_depense_betail = db.session.query(func.sum(Depense.montant)).filter(Depense.service_id == 'betail').scalar()
    depenses = db.session.query(Depense).filter(Depense.service_id == "betail").all()
    return render_template("pages/betail/tab_depense_betail.html", depenses=depenses,total_depense_betail=total_depense_betail)

@app.route("/tab_recette_betail")
def tab_recette_betail():
    total_recette_betail = db.session.query(func.sum(Recette.montant)).filter(Recette.service_id == 'betail').scalar()
    recettes = db.session.query(Recette).filter(Recette.service_id == "betail").all()
    return render_template('pages/betail/tab_recette_betail.html', recettes=recettes,total_recette_betail=total_recette_betail)


@app.route("/update_recette_betail/<int:recette_id>", methods=["GET", "POST"])
def update_recette_betail(recette_id):
    recette = Recette.query.filter_by(id=recette_id).first()
    if request.method == "POST":
        plan_compta = request.form['plan_compta']
        montant = request.form['montant']
        recette.plan_compta = plan_compta
        recette.montant = montant
        db.session.add(recette)
        db.session.commit()
        return redirect(url_for('tab_recette_betail'))
    return render_template('pages/betail/update_recette_betail.html', recette=recette)


@app.route("/update_depense_betail/<int:depense_id>", methods=["GET", "POST"])
def update_depense_betail(depense_id):
    depense = Depense.query.filter_by(id=depense_id).first()
    if request.method == "POST":
        beneficiaire = request.form['beneficiaire']
        plan_compta = request.form['plan_compta']
        motif = request.form['motif']
        montant = request.form['montant']
        depense.plan_compta = plan_compta
        depense.beneficiaire = beneficiaire
        depense.motif = motif
        depense.montant = montant
        db.session.add(depense)
        db.session.commit()
        return redirect(url_for('tab_depense_betail'))
    return render_template('pages/betail/update_depense_betail.html', depense=depense)



'''Les pages loyer'''
@app.route("/add_depense_loyer", methods=["GET", "POST"])
def add_depense_loyer():
    if request.method == "POST":
        depense = Depense(
            plan_compta=request.form['plan_compta'],
            beneficiaire=request.form['beneficiaire'],
            montant=request.form['montant'],
            motif=request.form['motif'],
            service_id=request.form['service'])
        db.session.add(depense)
        db.session.commit()
    return render_template("pages/loyer/add_depense_loyer.html")


@app.route("/add_recette_loyer", methods=["GET", "POST"])
def add_recette_loyer():
    if request.method == "POST":
        recette = Recette(
            plan_compta=request.form['plan_compta'],
            montant=request.form['montant'],
            service_id=request.form['service'],
        )
        db.session.add(recette)
        db.session.commit()
    return render_template('pages/loyer/add_recette_loyer.html')


@app.route("/tab_depense_loyer")
def tab_depense_loyer():
    total_depense_loyer = db.session.query(func.sum(Depense.montant)).filter(Depense.service_id == 'loyer').scalar()
    depenses = db.session.query(Depense).filter(Depense.service_id == "loyer").all()
    return render_template("pages/loyer/tab_depense_loyer.html", depenses=depenses,total_depense_loyer=total_depense_loyer)


@app.route("/tab_recette_loyer")
def tab_recette_loyer():
    total_recette_loyer = db.session.query(func.sum(Recette.montant)).filter(Recette.service_id == 'loyer').scalar()
    recettes = db.session.query(Recette).filter(Recette.service_id == "loyer").all()
    return render_template('pages/loyer/tab_recette_loyer.html', recettes=recettes,total_recette_loyer=total_recette_loyer)


@app.route("/update_recette_loyer/<int:recette_id>", methods=["GET", "POST"])
def update_recette_loyer(recette_id):
    recette = Recette.query.filter_by(id=recette_id).first()
    if request.method == "POST":
        plan_compta = request.form['plan_compta']
        montant = request.form['montant']
        recette.plan_compta = plan_compta
        recette.montant = montant
        db.session.add(recette)
        db.session.commit()
        return redirect(url_for('tab_recette_loyer'))
    return render_template('pages/loyer/update_recette_loyer.html', recette=recette)


@app.route("/update_depense_loyer/<int:depense_id>", methods=["GET", "POST"])
def update_depense_loyer(depense_id):
    depense = Depense.query.filter_by(id=depense_id).first()
    if request.method == "POST":
        beneficiaire = request.form['beneficiaire']
        plan_compta = request.form['plan_compta']
        motif = request.form['motif']
        montant = request.form['montant']
        depense.plan_compta = plan_compta
        depense.beneficiaire = beneficiaire
        depense.motif = motif
        depense.montant = montant
        db.session.add(depense)
        db.session.commit()
        return redirect(url_for('tab_depense_loyer'))
    return render_template('pages/loyer/update_depense_loyer.html', depense=depense)


#
# @app.route("/update_loyer/<int:id>", methods=["GET", "POST"])
# def update_loyer(id):
#     depense =Depense.query.filter(and_(Depense.id == id, Depense.type_table=='depense',Depense.service_id=='loyer')).first()
#     if depense:
#         if request.method == "POST":
#             beneficiaire = request.form['beneficiaire']
#             plan_compta = request.form['plan_compta']
#             motif = request.form['motif']
#             montant = request.form['montant']
#             depense.plan_compta = plan_compta
#             depense.beneficiaire = beneficiaire
#             depense.motif = motif
#             depense.montant = montant
#             db.session.add(depense)
#             db.session.commit()
#             return redirect(url_for('tab_depense_loyer'))
#         return render_template('pages/loyer/update_depense_loyer.html', depense=depense)
#     recette = Recette.query.filter(and_(Recette.id == id, Recette.type_table=='recette',Recette.service_id=='loyer')).first()
#     if recette:
#         if request.method == "POST":
#             plan_compta = request.form['plan_compta']
#             montant = request.form['montant']
#             recette.plan_compta = plan_compta
#             recette.montant = montant
#             db.session.add(recette)
#             db.session.commit()
#             return redirect(url_for('tab_recette_loyer'))
#         return render_template('pages/loyer/update_recette_loyer.html', recette=recette)
#     return "Traitement non éffectué"

@app.route("/delete/<int:depense_id>", methods=["GET", "POST"])
def delete_depense(depense_id):
    if request.method == "GET":
        depense = Depense.query.filter_by(id=depense_id).first()
        db.session.delete(depense)
        db.session.commit()
        return redirect('/tab_depense_loyer')
    return render_template("pages/loyer/tab_depense_loyer.html")


@app.route("/delete_recette/<int:recette_id>", methods=["GET", "POST"])
def delete_recette(recette_id):
    if request.method == "GET":
        recette = Recette.query.filter_by(id=recette_id).first()
        db.session.delete(recette)
        db.session.commit()
        return redirect('/tab_recette_loyer')
    return render_template("pages/loyer/tab_recette_loyer.html")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
