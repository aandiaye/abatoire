<<<<<<< Updated upstream
from datetime import datetime
from flask import Flask, render_template, request, redirect
=======

from flask import Flask, render_template, redirect, url_for
from flask import request
>>>>>>> Stashed changes
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

<<<<<<< Updated upstream
# basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
# app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
# app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# initialize the app with the extension
# db.init_app(app)
db = SQLAlchemy(app)
=======
db = SQLAlchemy()
app = Flask(__name__)
bcrypt = Bcrypt(app)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['SECRET_KEY'] ='mysecretkey'
# initialize the app with the extension
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(str(Users))

>>>>>>> Stashed changes



class Users(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    identifiant = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.today())

class RegisterForm(FlaskForm):
    identifiant = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Identifiant"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")
def validate_on_submit(self, identifiant):
    existing_user_identifiant = Users.query.filter_by(identifiant=identifiant.data).first()
    if existing_user_identifiant:
            raise ValidationError("errore")

class LoginForm(FlaskForm):
        identifiant = StringField(validators=[InputRequired(), Length(min=4, max=20)],
                                      render_kw={"placeholder": "Identifiant"})
        password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)],
                                     render_kw={"placeholder": "Password"})

        submit = SubmitField("Login")




class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
<<<<<<< Updated upstream
    service = db.Column(db.String(20))
    depense = db.relationship('Depense', backref='service', lazy=True)
    recette = db.relationship('Recette', backref='service', lazy=True)
=======
    service = db.Column(db.String(255), nullable=False)
    depense = db.relationship('Depense', backref='service')
    recette = db.relationship('Recette', backref='Service')
>>>>>>> Stashed changes


class Depense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plan_compta = db.Column(db.Integer, nullable=False)
    beneficiaire = db.Column(db.Integer, nullable=False)
    montant = db.Column(db.Integer, nullable=False)
    motif = db.Column(db.String(255), nullable=False)
<<<<<<< Updated upstream
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
=======
    service_id = db.Column(db.String, db.ForeignKey('service.id'))
>>>>>>> Stashed changes

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



<<<<<<< Updated upstream

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

=======
@app.route("/login", methods=["POST", "GET"])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(identifiant=form.identifiant.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                load_user(user)
                return redirect(url_for('tab_afficher_depense_abattage'))
    return render_template('pages/betails/login.html', form=form)

@app.route("/", methods=["POST", "GET"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        new_identifiant=Users(identifiant=form.identifiant.data, password=hash_password)
        db.session.add(new_identifiant)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('pages/betails/register.html', form=form)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/form_ajout_depense_betails", methods=["GET", "POST"])
def form_ajout_depense_betails():
        if request.method == "POST":
            depense=Depense(
            plan_compta = request.form['plan_compta'],
            beneficiaire = request.form['beneficiaire'],
            montant = request.form['montant'],
            motif = request.form['motif'],
            service_id = request.form['service'])
            db.session.add(depense)
            db.session.commit()
        return render_template('./pages/betails/form_ajout_depense_betails.html')

@app.route("/tab_afficher_depense")
def tab_afficher_depense():
    depense=Depense.query.all()
    return render_template('pages/betails/tab_afficher_depense.html', depense=depense)

@app.route("/<int:depense_id>", methods=["GET", "POST"])
def modifier_depense_betails(depense_id):
    depense = Depense.query.get_or_404(depense_id)
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
        return redirect(url_for('tab_afficher_depense'))
    return render_template('pages/betails/modifier_depense_betails.html', depense=depense)


@app.route("/delete/<int:id>" , methods=['GET', 'POST'])
def delete_depense_betails(id):
    if request.method=="GET":
        depense = Depense.query.filter_by(id=id).first()
        db.session.delete(depense)
        db.session.commit()
        return redirect('/tab_afficher_depense')
    return render_template("pages/betails/tab_afficher_depense.html")









@app.route("/form_ajout_recette_betails", methods=["GET", "POST"])
def form_ajout_recette_betails():
    if request.method == "POST":
        recette = Recette(
        plan_compta=request.form['plan_compta'],
        montant=request.form['montant'])
        db.session.add(recette)
        db.session.commit()
    return render_template('./pages/betails/form_ajout_recette_betails.html')

@app.route("/tab_afficher_recette")
def tab_afficher_recette():
        recette = Recette.query.all()
        return render_template('pages/betails/tab_afficher_recette.html', recette=recette)


@app.route("/<int:recette_id>/modifier_recette_betails", methods=["GET", "POST"])
def modifier_recette_betails(recette_id):
    recette = Recette.query.get_or_404(recette_id)
    if request.method =="POST":

        plan_compta = request.form['plan_compta']
        montant = request.form['montant']

        recette.plan_compta = plan_compta
        recette.montant = montant

        db.session.add(recette)
        db.session.commit()

        return redirect(url_for('tab_afficher_recette'))
    return render_template('pages/betails/modifier_recette_betails.html', recette=recette)


@app.route("/delete/<int:id>", methods=('GET', 'POST'))
def delete_recette_betails(id):
    if request.method=="GET":
        recette = Recette.query.filter_by(id=id).first()
        db.session.delete(recette)
        db.session.commit()
        return redirect('/tab_afficher_recette')
    return render_template("pages/betails/tab_afficher_recette.html")






@app.route("/form_ajout_depense_abattage", methods=["GET", "POST"])
def form_ajout_depense_abattage():
    if request.method == "POST":
            depense = Depense(
            plan_compta = request.form['plan_compta'],
            beneficiaire = request.form['beneficiaire'],
            montant = request.form['montant'],
            motif=request.form['motif'],
            service_id = request.form['service'])
            db.session.add(depense)
            db.session.commit()
    return render_template("pages/abattage/form_ajout_depense_abattage.html")



@app.route("/tab_afficher_depense_abattage")
def tab_afficher_depense_abattage():
    depense=Depense.query.all()
    return render_template('pages/abattage/tab_afficher_depense_abattage.html', depense=depense)


@app.route("/<int:depense_id>", methods=["GET", "POST"])
def modifier_depense_abattage(depense_id):
    depense = Depense.query.get_or_404(depense_id)
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
        return redirect(url_for('tab_afficher_depense_abattage'))
    return render_template('pages/betails/ modifier_depense_abattage.html', depense=depense)



@app.route("/delete/<int:id>", methods=["GET", "POST"])

def delete_depense_abattage(id):
    if request.method=="GET":
        depense = Depense.query.filter_by(id=id).first()
        db.session.delete(depense)
        db.session.commit()
        return redirect('/tab_afficher_depense_abattage')
    return render_template("pages/abattage/tab_afficher_depense_abattage.html")


@app.route("/form_ajout_recette_abattage", methods=["GET", "POST"])
def form_ajout_recette_abattage():
    if request.method == "POST":
            recette = Recette(
            plan_compta=request.form['plan_compta'],
            montant=request.form['montant'])
            db.session.add(recette)
            db.session.commit()
    return render_template("pages/abattage/form_ajout_recette_abattage.html")


@app.route("/tab_afficher_recette_abattage")
def tab_afficher_recette_abattage():
    recette=Recette.query.all()
    return render_template("pages/abattage/tab_afficher_recette_abattage.html", recette=recette)



@app.route("/<int:recette_id>/modifier_recette_abattage", methods=["GET", "POST"])
def modifier_recette_abattage(recette_id):
    recette = Recette.query.get_or_404(recette_id)
    if request.method == "POST":
        plan_compta = request.form['plan_compta']
        montant = request.form['montant']

        recette.plan_compta = plan_compta
        recette.montant = montant

        db.session.add(recette)
        db.session.commit()
        return redirect(url_for('tab_afficher_recette_abattage'))
    return render_template("pages/abattage/modifier_recette_abattage.html", recette=recette)


@app.route("/delete<int:id>", methods=["GET", "POST"])
def delete_recette_abattage(id):
    if request.method == "GET":
        recette = Recette.query.filter_by(id=id).first()
        db.session.delete(recette)
        db.session.commit()
        return redirect(url_for('tab_afficher_recette_abattage'))
    return render_template("pages/abattage/tab_afficher_recette_abattage.html")


@app.route("/form_ajout_depense_loyer", methods=["GET", "POST"])
def form_ajout_depense_loyer():
    if request.method == "POST":
            depense=Depense(
            plan_compta=request.form['plan_compta'],
            beneficiaire=request.form['beneficiaire'],
            montant =request.form['montant'],
            motif=request.form['motif'],
            service_id =request.form['service'])
            db.session.add(depense)
            db.session.commit()
    return render_template("pages/loyer/form_ajout_depense_loyer.html")


@app.route("/tab_afficher_depense_loyer")
def tab_afficher_depense_loyer():
    depense=Depense.query.all()
    return render_template("pages/loyer/tab_afficher_depense_loyer.html", depense=depense)

@app.route("/<int:depense_id>", methods=["GET", "POST"])
def modifier_depense_loyer(depense_id):
    depense=Depense.query.get_or_404(depense_id)
    if request.method =="POST":
        beneficiaire=request.form['beneficiaire']
        plan_compta=request.form['plan_compta']
        motif=request.form['motif']
        montant=request.form['montant']

        depense.plan_compta=plan_compta
        depense.beneficiaire=beneficiaire
        depense.motif=motif
        depense.montant=montant

        db.session.add(depense)
        db.session.commit()
        return redirect(url_for('tab_afficher_depense_loyer'))
    return render_template('pages/loyer/modifier_depense_loyer.html', depense=depense)



@app.route("/delete/<int:id>", methods=["GET", "POST"])
def delete_depense_loyer(id):
    if request.method=="GET":
        depense = Depense.query.filter_by(id=id).first()
        db.session.delete(depense)
        db.session.commit()
        return redirect('/tab_afficher_depense_loyer')
    return render_template("pages/loyer/tab_afficher_depense_loyer.html")



@app.route("/form_ajout_recette_loyer", methods=["GET", "POST"])
def form_ajout_recette_loyer():
    if request.method=="POST":
            recette= Recette(
            plan_compta=request.form['plan_compta'],
            montant=request.form['montant'])
            db.session.add(recette)
            db.session.commit()
    return render_template('pages/loyer/form_ajout_recette_loyer.html')


@app.route("/tab_afficher_recette_loyer")
def tab_afficher_recette_loyer():
    recette=Recette.query.all()
    return render_template('pages/loyer/tab_afficher_recette_loyer.html', recette=recette)


@app.route("/<int:recette_id>/modifier_recette_loyer", methods=["GET","POST"])
def modifier_recette_loyer(recette_id):
    recette=Recette.query.get_or_404(recette_id)
    if request.method=="POST":
        plan_compta=request.form['plan_compta']
        montant=request.form['montant']
>>>>>>> Stashed changes

        recette.plan_compta=plan_compta
        recette.montant=montant

<<<<<<< Updated upstream

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
=======
        db.session.add(recette)
        db.session.commit()
        return redirect((url_for('tab_afficher_recette_loyer')))
    return render_template('pages/loyer/modifier_recette_loyer.html', recette=recette)



@app.route("/delete/<int:id>", methods=["GET","POST"])
def delete_recette_loyer(id):
    if request.method =="GET":
        recette = Recette.query.filter_by(id=id).first()
        db.session.delete(recette)
        db.session.commit()
        return redirect('/tab_afficher_recette_loyer')
    return render_template("pages/loyer/tab_afficher_recette_loyer.html")



>>>>>>> Stashed changes


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
