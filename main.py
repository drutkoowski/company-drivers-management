from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import NewCandidate, EditCandidate
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///aplikacja-pz.db"
# Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = "sajdsahdhasuyu2yy6as6"
Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))


class Employee(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(250), nullable=False)
    LastName = db.Column(db.String(250), nullable=False)
    Email = db.Column(db.String(250), nullable=False)
    Password = db.Column(db.String(250), nullable=False)



class Candidates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(25), nullable=False)
    LastName = db.Column(db.String(25), nullable=False)
    Pesel = db.Column(db.Integer, nullable=False)
    Email = db.Column(db.String(80), nullable=False)
    Nationality = db.Column(db.String(25), nullable=False)
    BirthCity = db.Column(db.String(80), nullable=False)
    BirthDate = db.Column(db.Date, nullable=False)
    City = db.Column(db.String(80), nullable=False)
    Address = db.Column(db.String(80), nullable=False)
    CityPostalCode = db.Column(db.Integer, nullable=False)
    numer_karty_kierowcy_kandydata = db.Column(db.Integer, nullable=False)

# db.create_all()
# password = generate_password_hash("a")
# new = Employee(FirstName="Damian", LastName="Rutkowski", Email="a@o2.pl", Password=password)
# db.session.add(new)
# db.session.commit()

@app.route('/', methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        login = request.form.get("email_input")
        user = Employee.query.filter_by(Email=login).first()
        if user is not None:
            password = request.form.get("password_input")
            is_password_ok = check_password_hash(user.Password, password)
            if is_password_ok:
                login_user(user)
                return redirect(url_for('menu_page', id=user.id))
            else:
                return render_template("login.html")

    return render_template("login.html")


@app.route('/menu', methods=["GET", "POST"])
@login_required
def menu_page():
    return render_template("menu_page.html")


@login_required
@app.route("/add", methods=["GET", "POST"])
def add_candidate():

    form = NewCandidate()
    if request.method == "POST" and form.validate_on_submit():
        imie_kandydata = form.imie_kandydata.data
        nazwisko_kandydata = form.nazwisko_kandydata.data
        pesel_kandydata = form.pesel_kandydata.data
        email_kandydata = form.email_kandydata.data
        narodowosc_kandydata = form.narodowosc_kandydata.data
        miasto_urodzenia_kandydata = form.miasto_urodzenia_kandydata.data
        data_urodzenia_kandydata = form.data_urodzenia_kandydata.data
        miejscowosc_zamieszkania_kandydata = form.miejscowosc_zamieszkania_kandydata.data
        adres_zamieszkania_kandydata = form.adres_zamieszkania_kandydata.data
        kod_pocztowy_kandydata = form.kod_pocztowy_kandydata.data
        numer_karty_kierowcy_kandydata = form.numer_karty_kierowcy.data
        new_candidate = Candidates(FirstName=imie_kandydata, LastName=nazwisko_kandydata, Pesel=pesel_kandydata, Email=email_kandydata, Nationality=narodowosc_kandydata,BirthCity=miasto_urodzenia_kandydata,BirthDate=data_urodzenia_kandydata,City=miejscowosc_zamieszkania_kandydata,Address=adres_zamieszkania_kandydata,CityPostalCode=kod_pocztowy_kandydata, numer_karty_kierowcy_kandydata=numer_karty_kierowcy_kandydata)
        db.session.add(new_candidate)
        db.session.commit()
        return render_template("menu_page.html")
    return render_template("add.html", form=form)

@login_required
@app.route("/show", methods=["GET"])
def show_candidates():
    candidates = Candidates.query.all()
    return render_template("showcandidates.html", candidates=candidates)

@login_required
@app.route("/edit-candidate", methods=["GET", "POST"])
def edit_candidate():
    id = request.args.get("id")
    candidate = Candidates.query.filter_by(id=id).first()
    form = EditCandidate()
    if request.method == "POST":
        candidate.FirstName = form.imie_kandydata.data
        candidate.LastName = form.nazwisko_kandydata.data
        candidate.Pesel = form.pesel_kandydata.data
        candidate.Email = form.email_kandydata.data
        candidate.Nationality = form.narodowosc_kandydata.data
        candidate.BirthCity = form.miasto_urodzenia_kandydata.data
        candidate.BirthDate = form.data_urodzenia_kandydata.data
        candidate.City = form.miejscowosc_zamieszkania_kandydata.data
        candidate.Address = form.adres_zamieszkania_kandydata.data
        candidate.CityPostalCode = form.kod_pocztowy_kandydata.data
        candidate.numer_karty_kierowcy_kandydata = form.numer_karty_kierowcy.data
        db.session.commit()
        return redirect(url_for('menu_page'))

    if candidate is not None:
        form.imie_kandydata.data = candidate.FirstName
        form.nazwisko_kandydata.data = candidate.LastName
        form.pesel_kandydata.data = candidate.Pesel
        form.email_kandydata.data = candidate.Email
        form.narodowosc_kandydata.data = candidate.Nationality
        form.miasto_urodzenia_kandydata.data = candidate.BirthCity
        form.data_urodzenia_kandydata.data = candidate.BirthDate
        form.miejscowosc_zamieszkania_kandydata.data = candidate.City
        form.adres_zamieszkania_kandydata.data = candidate.Address
        form.kod_pocztowy_kandydata.data = candidate.CityPostalCode
        form.numer_karty_kierowcy.data = candidate.numer_karty_kierowcy_kandydata
    return render_template("editcandidate.html", form=form)

@login_required
@app.route("/delete-candidate", methods=["GET", "POST"])
def delete_candidate():
    id = request.args.get("id")
    candidate = Candidates.query.filter_by(id=id).first()
    db.session.delete(candidate)
    db.session.commit()
    return redirect(url_for('show_candidates'))



@app.route('/logout')
def logout():
    logout_user()
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
