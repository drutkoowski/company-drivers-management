import webbrowser

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import NewCandidate, EditCandidate
from flask_bootstrap import Bootstrap
import os

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
    FirstName = db.Column(db.String(25))
    LastName = db.Column(db.String(25))
    Pesel = db.Column(db.Integer)
    Email = db.Column(db.String(80))
    Nationality = db.Column(db.String(25))
    BirthCity = db.Column(db.String(80))
    BirthDate = db.Column(db.Date)
    City = db.Column(db.String(80))
    Address = db.Column(db.String(80))
    CityPostalCode = db.Column(db.Integer)
    driver_card_number = db.Column(db.Integer)
    driver_card_number_expires_date = db.Column(db.Date)
    form1_status = db.Column(db.Integer)
    form2_status = db.Column(db.Integer)
    form3_status = db.Column(db.Integer)
    form4_status = db.Column(db.Integer)






@app.route('/', methods=["GET", "POST"])
def login_page():
    if current_user.is_authenticated:
        user = Employee.query.filter_by(id=current_user.id).first()
        return redirect(url_for('menu_page', id=user.id))
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
        data_wygasniecia_karty_kierowcy = form.data_wygasniecia_karty_kierowcy.data
        form1_status = form.form1.data
        form2_status = form.form2.data
        form3_status = form.form3.data
        form4_status = form.form4.data
        new_candidate = Candidates(FirstName=imie_kandydata, LastName=nazwisko_kandydata, Pesel=pesel_kandydata,
                                   Email=email_kandydata, Nationality=narodowosc_kandydata,
                                   BirthCity=miasto_urodzenia_kandydata,BirthDate=data_urodzenia_kandydata,
                                   City=miejscowosc_zamieszkania_kandydata,Address=adres_zamieszkania_kandydata,
                                   CityPostalCode=kod_pocztowy_kandydata,
                                   driver_card_number=numer_karty_kierowcy_kandydata,
                                   driver_card_number_expires_date=data_wygasniecia_karty_kierowcy,
                                   form1_status=form1_status,form2_status=form2_status,form3_status=form3_status,
                                   form4_status=form4_status,
                                   )
        db.session.add(new_candidate)
        db.session.commit()
        #Tworzenie folderu kandydata
        cwd = rf"{os.getcwd()}"
        newpath = rf"{cwd}/{pesel_kandydata}"
        if not os.path.exists(newpath):
            folder_name = f"{pesel_kandydata}"
            os.mkdir(f"{folder_name}")
            if form.skan_dowodu.data:
                form.skan_dowodu.data.save(os.path.join(f'{pesel_kandydata}/skandowodu.pdf'))
            if form.karta_kierowcy.data:
                form.karta_kierowcy.data.save(os.path.join(f'{pesel_kandydata}/kartakierowcy.pdf'))
        return render_template("menu_page.html")
    return render_template("add.html", form=form)

@login_required
@app.route("/show", methods=["GET", "POST"])
def show_candidates():
    candidates = Candidates.query.all()
    if request.method == "POST":
        surname_to_search = request.form.get('surname_search')
        candidate_to_search = Candidates.query.filter_by(LastName=surname_to_search).first()
        return render_template('showcandidates.html', candidates=candidates, candidate_search=candidate_to_search)
    return render_template("showcandidates.html", candidates=candidates)

@login_required
@app.route("/show-docs/karta", methods=["GET"])
def show_docs_karta():
    candidates = Candidates.query.all()
    id = request.args.get("id")
    candidate = Candidates.query.filter_by(id=id).first()
    pesel = candidate.Pesel
    path = rf"{os.getcwd()}\{pesel}\kartakierowcy.pdf"
    webbrowser.open(rf'{path}')
    return render_template("showcandidates.html", candidates=candidates)

@login_required
@app.route("/show-docs/dowod", methods=["GET"])
def show_docs_dowod():
    candidates = Candidates.query.all()
    id = request.args.get("id")
    candidate = Candidates.query.filter_by(id=id).first()
    pesel = candidate.Pesel
    path = rf"{os.getcwd()}\{pesel}\skandowodu.pdf"
    webbrowser.open(rf'{path}')
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
        candidate.driver_card_number = form.numer_karty_kierowcy.data
        candidate.driver_card_number_expires_date = form.data_wygasniecia_karty_kierowcy.data
        candidate.form1_status = form.form1.data
        candidate.form2_status = form.form2.data
        candidate.form3_status = form.form3.data
        candidate.form4_status = form.form4.data
        db.session.commit()
        cwd = rf"{os.getcwd()}"
        pesel_kandydata = candidate.Pesel
        newpath = rf"{cwd}/{pesel_kandydata}"
        if not os.path.exists(newpath):
            folder_name = f"{pesel_kandydata}"
            os.mkdir(f"{folder_name}")
            if form.skan_dowodu.data:
                form.skan_dowodu.data.save(os.path.join(f'{pesel_kandydata}/skandowodu.pdf'))
            if form.karta_kierowcy.data:
                form.karta_kierowcy.data.save(os.path.join(f'{pesel_kandydata}/kartakierowcy.pdf'))
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
        form.numer_karty_kierowcy.data = candidate.driver_card_number
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
