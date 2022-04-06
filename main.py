from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import os
from forms import NewCandidate
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



@app.route('/', methods=["GET", "POST"])
def login_page():

    if request.method == "POST":
        login = request.form.get("email_input")
        user = Employee.query.filter_by(Email=login).first()
        password = request.form.get("password_input")
        is_password_ok = check_password_hash(user.Password, password)
        if is_password_ok:
            login_user(user)
            return redirect(url_for('menu_page', id=user.id))


    return render_template("login.html")



@app.route('/menu', methods=["GET", "POST"])
@login_required
def menu_page():
        id = current_user.id
        user = Employee.query.filter_by(id=id).first()
        return render_template("menu_page.html", user=user)

@login_required
@app.route("/add", methods=["GET", "POST"])
def add_candidate():
    id = current_user.id
    form = NewCandidate()
    user = Employee.query.filter_by(id=id).first()
    if request.method == "POST" and form.validate_on_submit():
        return render_template("menu_page.html", user=user)
    return render_template("add.html", form=form,user=user)



@app.route('/logout')
def logout():
    logout_user()
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)