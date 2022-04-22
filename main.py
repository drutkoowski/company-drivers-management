import string
import webbrowser

import werkzeug
from flask import Flask, render_template, request, redirect, url_for, flash, Response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.utils import secure_filename

from forms import NewCandidate, EditCandidate
from flask_bootstrap import Bootstrap
import os
import smtplib
import random
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///aplikacja-pz.db"
# Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = "sajS(dsah@!@dhax3x4jop[xas]uy@Su2yy6a*73^s6"
Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)
code = ""
email_to_change = ""


def set_status():
    candidates = Candidates.query.all()
    now = datetime.datetime.now()
    for candidate in candidates:
        if candidate.form1_status == 0 or candidate.form2_status == 0 or candidate.form3_status == 0 or candidate.form4_status == 0:
            candidate.status = 0
        if candidate.form1_status == 1 and candidate.form2_status == 1 and candidate.form3_status == 1 and candidate.form4_status == 1:
            candidate.status = 1
        if candidate.form1_status == 3 and candidate.form2_status == 3 and candidate.form3_status == 3 and candidate.form4_status == 3:
            candidate.status = 3
        if candidate.form1_status == 4 or candidate.form2_status == 4 or candidate.form3_status == 4 or candidate.form4_status == 4:
            candidate.status = 4
        is_alert, diff = alerting(candidate.driver_card_number_expires_date)
        if is_alert and (2 > diff > 0):
            candidate.alert = 1
        if is_alert and diff < 0:
            candidate.alert = 2
        elif is_alert is False:
            candidate.alert = 0
    db.session.flush()
    db.session.commit()


def months(d1, d2):
    return d1.month - d2.month + 12 * (d1.year - d2.year)


def alerting(d2):
    d1 = datetime.datetime.now()
    diff = months(d1=d2, d2=d1)
    if diff < 2:
        return True, diff
    else:
        return False, diff


def code_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))


class Employee(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(250))
    LastName = db.Column(db.String(250))
    Email = db.Column(db.String(250), unique=True)
    Password = db.Column(db.String(250))


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
    status = db.Column(db.Integer, default=0)
    alert = db.Column(db.Integer, default=0)
    documents = db.relationship('Documents', backref="candidates")
    documentscard = db.relationship('DocumentsCard', backref="candidates")


class Documents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doc = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


class DocumentsCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doc = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        user = Employee.query.filter_by(id=current_user.id).first()
        return redirect(url_for('menu_page', id=user.id))
    if request.method == "POST":
        email = request.form.get("email_signup")
        firstname = request.form.get("firstname_signup")
        secondname = request.form.get("secondname_signup")
        password = request.form.get("password_signup")
        is_user_in_database = Employee.query.filter_by(Email=email).first()
        print(is_user_in_database)
        if is_user_in_database:
            flash("Użytkownik z podanym adresem email już istnieje!")
            return render_template("signup.html")
        elif is_user_in_database is None:
            flash("Konto założone pomyślnie!")
            employee = Employee(FirstName=firstname, LastName=secondname,Email=email, Password=generate_password_hash(password))
            db.session.add(employee)
            db.session.commit()
            redirect(url_for('login_page'))
    return render_template("signup.html")

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
                flash("Pomyślnie zalogowano!")
                return redirect(url_for('menu_page', id=user.id))
            else:
                flash("Błędne dane do logowania!")
                return render_template("login.html")
        else:
            flash("Błędne dane do logowania!")
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
                                   BirthCity=miasto_urodzenia_kandydata, BirthDate=data_urodzenia_kandydata,
                                   City=miejscowosc_zamieszkania_kandydata, Address=adres_zamieszkania_kandydata,
                                   CityPostalCode=kod_pocztowy_kandydata,
                                   driver_card_number=numer_karty_kierowcy_kandydata,
                                   driver_card_number_expires_date=data_wygasniecia_karty_kierowcy,
                                   form1_status=form1_status, form2_status=form2_status, form3_status=form3_status,
                                   form4_status=form4_status,
                                   )
        db.session.add(new_candidate)
        db.session.commit()
        if form.skan_dowodu.data:
            filename = secure_filename(form.skan_dowodu.data.filename)
            mimetype = form.skan_dowodu.data.mimetype
            if not filename or not mimetype:
                flash("Nie udało się dodać skanu!")
                return render_template("add.html", form=form)
            doc = Documents(doc=form.skan_dowodu.data.read(), name=filename, mimetype=mimetype,
                            candidate_id=new_candidate.id)
            db.session.add(doc)
            db.session.commit()
            if form.karta_kierowcy.data:
                filename = secure_filename(form.karta_kierowcy.data.filename)
                mimetype = form.karta_kierowcy.data.mimetype
                if not filename or not mimetype:
                    flash("Nie udało się dodać skanu!")
                    return render_template("add.html", form=form)
                docCard = DocumentsCard(doc=form.karta_kierowcy.data.read(), name=filename, mimetype=mimetype,
                                        candidate_id=new_candidate.id)
                db.session.add(docCard)
                db.session.commit()

        return render_template("menu_page.html")
    return render_template("add.html", form=form)


@login_required
@app.route("/show", methods=["GET", "POST"])
def show_candidates():
    set_status()
    candidates = Candidates.query.all()
    if request.method == "POST":
        surname_to_search = request.form.get('surname_search')
        candidate_to_search = Candidates.query.filter_by(LastName=surname_to_search).first()
        if candidate_to_search is None:
            flash("Brak kandydata z takim nazwiskiem!")
        return render_template('showcandidates.html', candidates=candidates, candidate_search=candidate_to_search)
    return render_template("showcandidates.html", candidates=candidates)


@login_required
@app.route("/show-docs/karta", methods=["GET"])
def show_docs_karta():
    candidates = Candidates.query.all()
    id = request.args.get("id")
    doc = DocumentsCard.query.filter_by(candidate_id=id).first()
    if doc:
        return Response(doc.doc, mimetype=doc.mimetype)
    else:
        flash("Brak odpowiedniego dokumentu w bazie!")
        return render_template("showcandidates.html", candidates=candidates)


@login_required
@app.route("/show-docs/dowod", methods=["GET"])
def show_docs_dowod():
    candidates = Candidates.query.all()
    id = request.args.get("id")
    doc = Documents.query.filter_by(candidate_id=id).first()
    if doc:
        return Response(doc.doc, mimetype=doc.mimetype)
    else:
        flash("Brak odpowiedniego dokumentu w bazie!")
        return render_template("showcandidates.html", candidates=candidates)


@login_required
@app.route("/edit-candidate", methods=["GET", "POST"])
def edit_candidate():
    id = request.args.get("id")
    candidate = Candidates.query.filter_by(id=id).first()
    form = EditCandidate()
    if request.method == "POST" and form.validate_on_submit():
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
            else:
                flash("Dodawanie dokumentu nie powiodło się!")
        return redirect(url_for('menu_page'))
    elif request.method == "POST" and not form.validate_on_submit():
        flash("Edytowanie kandydata nie powiodło się!")
        return render_template("editcandidate.html", form=form)
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
        form.data_wygasniecia_karty_kierowcy.data = candidate.driver_card_number_expires_date
        form.form1.data = candidate.form1_status
        form.form2.data = candidate.form2_status
        form.form3.data = candidate.form3_status
        form.form4.data = candidate.form4_status
    return render_template("editcandidate.html", form=form)


@login_required
@app.route("/delete-candidate", methods=["GET", "POST"])
def delete_candidate():
    id = request.args.get("id")
    candidate = Candidates.query.filter_by(id=id).first()
    try:
        db.session.delete(candidate)
    except:
        flash("Usuwanie kandydata nie powiodło się!")
    else:
        flash("Usuwanie kandydata powiodło się!")
    finally:
        db.session.commit()
    return redirect(url_for('show_candidates'))


@app.route('/password-lost', methods=["GET", "POST"])
def password_lost():
    email_input = request.form.get("email_input_remind")
    global code
    code = code_generator()
    if request.method == "POST":
        user_to_remind_password = Employee.query.filter_by(Email=email_input).first()
        if user_to_remind_password and user_to_remind_password is not None:
            my_email = "firmaprojektzespolowy@gmail.com"
            password = "Firma123"
            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(user=my_email, password=password)
                connection.sendmail(from_addr=my_email, to_addrs=email_input,
                                    msg=f"Subject:Przypomnienie adresu email!\n\nTwoj kod do przypomnienia hasla:{code}")
                connection.close()
            return redirect(url_for('email_code', email_input=email_input))
        else:
            flash("Nie znaleziono konta powiązanego z tym adresem email!")
            return render_template("password_lost.html")
    return render_template("password_lost.html")


@app.route('/email-lost', methods=["GET", "POST"])
def email_code():
    email = request.args.get('email_input')
    if request.method == "GET":
        global email_to_change
        email_to_change = email
    global code
    if request.method == "POST":
        code_typed = request.form.get("code_sent")
        password = request.form.get("password_new")
        if code == code_typed:
            employee = Employee.query.filter_by(Email=email_to_change).first()
            employee.Password = generate_password_hash(password)
            db.session.commit()
            flash("Pomyślnie zmieniono hasło!")
            return redirect(url_for('login_page'))
        else:
            flash("Podany przez Ciebie kod jest błędny!")
            return redirect(url_for('email_code', email_input=email))
    if email is None or email.strip() == "" or email == "":
        return redirect(url_for('login_page'))
    if email is not None:
        return render_template("email_code.html")


@app.route('/logout')
def logout():
    logout_user()
    flash("Wylogowano!")
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
