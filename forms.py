from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField,IntegerField, DateField
from wtforms.validators import DataRequired, URL,NumberRange, Email

class NewCandidate(FlaskForm):
    imie_kandydata = StringField("Imię: ", validators=[DataRequired()])
    nazwisko_kandydata = StringField("Nazwisko: ", validators=[DataRequired()])
    pesel_kandydata = IntegerField("Pesel: ", validators=[DataRequired(),NumberRange(min=11,max=11, message="Pesel zawiera 11 znaków!")])
    email_kandydata = StringField("Email: ", validators=[DataRequired(), Email()])
    narodowosc_kandydata = StringField("Narodowość kandydata: ", validators=[DataRequired()])
    miasto_urodzenia_kandydata = StringField("Miasto urodzenia kandydata: ", validators=[DataRequired()])
    data_urodzenia_kandydata = DateField("Data urodzenia kandydata: ", validators=[DataRequired()])
    miejscowosc_zamieszkania_kandydata = StringField("Miasto zamieszkania kandydata: ", validators=[DataRequired()])
    adres_zamieszkania_kandydata = StringField("Adres zamieszkania kandydata: ", validators=[DataRequired()])
    kod_pocztowy_kandydata = IntegerField("Kod pocztowy kandydata: ", validators=[DataRequired()])
    numer_karty_kierowcy = IntegerField("Numer karty kierowcy: ", validators=[DataRequired(),NumberRange(min=15,max=15, message="Karta kierowcy zawiera 15 znaków!")])
    submit = SubmitField("Submit Post")