from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, IntegerField, DateField, SelectField, FileField
from wtforms.validators import DataRequired, URL, NumberRange, Email, Length, Optional


class NewCandidate(FlaskForm):
    karta_kierowcy = FileField("OPCJONALNE: Dodaj kartę kierowcy (jpg/png)", validators=[Optional()],render_kw={'style': 'margin-top:1rem!important;'})
    skan_dowodu = FileField("OPCJONALNE: Dodaj skan dowodu (jpg/png)", validators=[Optional()],render_kw={'style': 'margin-top:1rem!important;'})
    imie_kandydata = StringField("Imię: ", validators=[DataRequired(message="Brak imienia!")])
    nazwisko_kandydata = StringField("Nazwisko: ", validators=[DataRequired(message="Brak nazwiska!")])
    pesel_kandydata = IntegerField("Pesel: ", validators=[DataRequired(message="Brak numeru pesel!")])
    email_kandydata = StringField("Email: ", validators=[DataRequired(message="Brak adresu email!"), Email()])
    narodowosc_kandydata = StringField("Narodowość kandydata: ", validators=[DataRequired(message="Brak narodowości!")])
    miasto_urodzenia_kandydata = StringField("Miasto urodzenia kandydata: ", validators=[DataRequired(message="Brak miasta urodzenia!")])
    data_urodzenia_kandydata = DateField("Data urodzenia kandydata: ", validators=[DataRequired(message="Brak daty urodzenia!")])
    miejscowosc_zamieszkania_kandydata = StringField("Miasto zamieszkania kandydata: ", validators=[DataRequired(message="Brak miejscowości!")])
    adres_zamieszkania_kandydata = StringField("Adres zamieszkania kandydata: ", validators=[DataRequired(message="Brak adresu!")])
    kod_pocztowy_kandydata = IntegerField("Kod pocztowy kandydata: ", validators=[DataRequired(message="Brak kodu pocztowego!")])
    numer_karty_kierowcy = IntegerField("Numer karty kierowcy: ", validators=[DataRequired(message="Niepoprawny numer karty kierowcy!")])
    data_wygasniecia_karty_kierowcy = DateField("Data wygaśniecia karty kierowcy: ", validators=[DataRequired(message="Brak daty wygaśnięcia karty kierowcy!")])
    form1 = SelectField(u'Formularz 1', choices=[('0', 'Nie wysłano'), ('1', 'Wysłano')])
    form2 = SelectField(u'Formularz 2', choices=[('0', 'Nie wysłano'), ('1', 'Wysłano')])
    form3 = SelectField(u'Formularz 3', choices=[('0', 'Nie wysłano'), ('1', 'Wysłano')])
    form4 = SelectField(u'Formularz 4', choices=[('0', 'Nie wysłano'), ('1', 'Wysłano')])
    submit = SubmitField("Dodaj kandydata",render_kw={'style': 'margin-top:1rem!important;'})

class EditCandidate(FlaskForm):
    karta_kierowcy = FileField("OPCJONALNE: Dodaj kartę kierowcy (pdf)", validators=[Optional(),FileAllowed(['jpg', 'png'])],
                               render_kw={'style': 'margin-top:1rem!important;'})
    skan_dowodu = FileField("OPCJONALNE: Dodaj skan dowodu (pdf)", validators=[Optional(),FileAllowed(['jpg', 'png'])],
                            render_kw={'style': 'margin-top:1rem!important;'})
    imie_kandydata = StringField("Imię: ", validators=[DataRequired(message="Brak imienia!")])
    nazwisko_kandydata = StringField("Nazwisko: ", validators=[DataRequired(message="Brak nazwiska!")])
    pesel_kandydata = IntegerField("Pesel: ", validators=[DataRequired(message="Brak numeru pesel!")])
    email_kandydata = StringField("Email: ", validators=[DataRequired(message="Brak adresu email!"), Email()])
    narodowosc_kandydata = StringField("Narodowość kandydata: ", validators=[DataRequired(message="Brak narodowości!")])
    miasto_urodzenia_kandydata = StringField("Miasto urodzenia kandydata: ", validators=[DataRequired(message="Brak miasta urodzenia!")])
    data_urodzenia_kandydata = DateField("Data urodzenia kandydata: ",  validators=[DataRequired(message="Brak daty urodzenia!")])
    miejscowosc_zamieszkania_kandydata = StringField("Miasto zamieszkania kandydata: ", validators=[DataRequired(message="Brak miejscowości!")])
    adres_zamieszkania_kandydata = StringField("Adres zamieszkania kandydata: ", validators=[DataRequired(message="Brak adresu!")])
    kod_pocztowy_kandydata = IntegerField("Kod pocztowy kandydata: ", validators=[DataRequired(message="Brak kodu pocztowego!")])
    numer_karty_kierowcy = IntegerField("Numer karty kierowcy: ", validators=[DataRequired(message="Niepoprawny numer karty kierowcy!")])
    data_wygasniecia_karty_kierowcy = DateField("Data wygasniecia karty kierowcy: ", validators=[DataRequired(message="Brak daty wygaśniecia karty kierowcy!")])
    form1 = SelectField(u'Formularz 1', choices=[('0', 'Nie wysłano'), ('1', 'Wysłano'), ('3', 'Otrzymano zgodę'),('4', 'Otrzymano odmowę')])
    form2 = SelectField(u'Formularz 2', choices=[('0', 'Nie wysłano'), ('1', 'Wysłano'), ('3', 'Otrzymano zgodę'),('4', 'Otrzymano odmowę')])
    form3 = SelectField(u'Formularz 3', choices=[('0', 'Nie wysłano'), ('1', 'Wysłano'), ('3', 'Otrzymano zgodę'),('4', 'Otrzymano odmowę')])
    form4 = SelectField(u'Formularz 4', choices=[('0', 'Nie wysłano'), ('1', 'Wysłano'), ('3', 'Otrzymano zgodę'),('4', 'Otrzymano odmowę')])
    submit = SubmitField("Edytuj kandydata",render_kw={'style': 'margin-top:1rem!important;'})

