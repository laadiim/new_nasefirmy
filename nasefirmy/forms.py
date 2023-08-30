#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
# nasefirmy/users/forms.py


# from flask_wtf import Form
from flask_wtf import FlaskForm
# from flask.ext.wtf import Form, widgets, SelectMultipleField
from wtforms import StringField, TextAreaField, PasswordField, IntegerField, DateField, DateTimeField, FieldList, FormField, RadioField
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms.widgets import TextArea
from datetime import datetime


class RegisterUserForm(FlaskForm):
    name = StringField('Uživatel', validators=[
                       DataRequired(), Length(min=2, max=25)])
    password = PasswordField('Heslo', validators=[
                             DataRequired(), Length(min=2, max=40)])
    confirm = PasswordField('Potvrď heslo', validators=[
                            DataRequired(), EqualTo('password')])


# -- formulare pro registraci tymu
class TeamForm(FlaskForm):
    team_name = StringField('Název', validators=[DataRequired()])
    team_key = StringField('Klíč týmu', validators=[DataRequired()])
    team_date = DateTimeField('Datum (dd/mm/yyyy h/m)', validators=[DataRequired()], format='%d/%m/%Y %H:%M',
                              default=datetime.now())
    team_desc = StringField('Popis', validators=[
                            DataRequired()], default='popis')
    team_num_players = IntegerField('Počet hráčů', validators=[
                                    DataRequired()], default=5)


class TeamsListForm(FlaskForm):
    teams = FieldList(FormField(TeamForm), validators=[Length(max=160)])
# --


# -- formular pro select karet
class CardForm(FlaskForm):
    card_id = IntegerField('Karta ID')


class CardsListForm(FlaskForm):
    pr_cards = FieldList(FormField(CardForm))
    vyz_cards = FieldList(FormField(CardForm))
    hrz_cards = FieldList(FormField(CardForm))
# --


class LoginUserForm(FlaskForm):
    name = StringField('Uživatel', validators=[DataRequired()])
    password = PasswordField('Heslo', validators=[DataRequired()])


class LoginTeamForm(FlaskForm):
    game_key = StringField('Klíč Hry', validators=[DataRequired()])
    team_key = PasswordField('Klíč týmu')


class MktMessageForm(FlaskForm):
    title = StringField('Titulek')
    # body = TextAreaField('Obsah zprávy', widget=TextArea(row=3, cols=60))
    body = StringField('Obsah zprávy', widget=TextArea())


class RegisterPlaceForm(FlaskForm):
    nazev = StringField('Název', validators=[DataRequired()])
    ulice = StringField('Ulice')
    obec = StringField('Obec')
    psc = IntegerField('PSČ')
    souradnice = StringField('GPS')


class CreateGameForm(FlaskForm):
    nazev = StringField('Název', validators=[
                        DataRequired()], default='hra DEFAULT')
    # dat_hrani = DateField('Datum (dd/mm/yyyy)', validators=[DataRequired()], format='%d/%m/%Y',
    #                       default=datetime.now())
    dat_hrani = DateTimeField('Datum (dd/mm/yyyy h/m)', validators=[DataRequired()], format='%d/%m/%Y %H:%M',
                              default=datetime.now())
    misto_id = IntegerField('Místo ID', validators=[DataRequired()])
    popis = StringField('Popis', validators=[
                        DataRequired()], default='popis DEFAULT')
    klic = StringField('Klíč', validators=[DataRequired()], default='klic')
    poc_tymu = IntegerField('Počet týmů', validators=[
                            DataRequired()], default=3)
    majetek = IntegerField('Počáteční majetek', validators=[
                           DataRequired()], default=100)
    karty_za_kolo = IntegerField('Počet karet za kolo', validators=[
                                 DataRequired()], default=2)
    poc_kol = IntegerField('Počet kol', validators=[
                           DataRequired()], default=10)

    mkt_nazev = IntegerField('Odměna za název firmy', validators=[
                             DataRequired()], default=10)
    mkt_logo = IntegerField('Odměna za logo firmy', validators=[
                            DataRequired()], default=5)
    mkt_zprava = IntegerField('Odměna za napsání MZ', validators=[
                              DataRequired()], default=5)

    odm_zprava = IntegerField('Odměna za nejlepší MZ', validators=[
                              DataRequired()], default=5)
    odm_zprava_hlas = IntegerField('Odměna za hlas pro nejlepší MZ', validators=[
                                   DataRequired()], default=1)

    odm_robot1 = IntegerField('Odměna za nejlepší skelet robota', validators=[
                              DataRequired()], default=20)
    odm_robot1_hlas = IntegerField(
        'Odměna za hlas pro nejlepší skelet robota', validators=[DataRequired()], default=5)

    odm_robot2 = IntegerField('Odměna za nejlepší masku robota', validators=[
                              DataRequired()], default=10)
    odm_robot2_hlas = IntegerField(
        'Odměna za hlas pro nejlepší masku robota', validators=[DataRequired()], default=3)

    odm_robot3 = IntegerField('Odměna za nejlepší disky robota', validators=[
                              DataRequired()], default=10)
    odm_robot3_hlas = IntegerField(
        'Odměna za hlas pro nejlepší disky robota', validators=[DataRequired()], default=3)

    cena_cert = IntegerField('Poplatek za přístup k certifikaci', validators=[
                             DataRequired()], default=20)
    odm_cert = IntegerField('Odměna za certifikaci', validators=[
                            DataRequired()], default=50)


class MktMessageVotingForm(FlaskForm):
    item = RadioField('Label', choices=[])


class SpecialPaymentForm(FlaskForm):
    # teams = FieldList(FormField(TeamForm), validators=[Length(max=160)])
    team_name = StringField('Název týmu', validators=[Length(max=160)])
    amount = IntegerField('Částka', validators=[DataRequired()])
    description = StringField('Popis')


class ActionBackForm(FlaskForm):
    # teams = FieldList(FormField(TeamForm), validators=[Length(max=160)])
    team_name = StringField('Název týmu', validators=[Length(max=160)])
    card = StringField(validators=[DataRequired()])
    amount = StringField('popis')

# class MultiCheckboxField(SelectMultipleField):
#     widget = widgets.ListWidget(prefix_label=False)
#     option_widget = widgets.CheckboxInput()


# class MaVyrobekNazevLogoForm(Form):
#     # string_of_files = ['one\r\ntwo\r\nthree\r\n']
#     # list_of_files = string_of_files[0].split()
#     # create a list of value/description tuples
#     # files = [(x, x) for x in list_of_files]
#     choices = [('ma_vyrobek', 'ma_vyrobek'), ('ma_nazev', 'ma_nazev'), ('ma_logo', 'ma_logo')]
#     example = MultiCheckboxField('Label', choices=choices)
