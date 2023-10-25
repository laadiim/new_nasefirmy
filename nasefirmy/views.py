#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# project/users/views.py


#################
#### imports ####
#################

from functools import wraps
from flask import flash, redirect, render_template, request, session, url_for, Blueprint
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, update

from nasefirmy.forms import RegisterUserForm, TeamForm, TeamsListForm, RegisterPlaceForm, LoginTeamForm, \
    CreateGameForm, MktMessageForm, MktMessageVotingForm, SpecialPaymentForm, CardForm, CardsListForm
from nasefirmy import app, db, bcrypt
from nasefirmy.models import CisTymy, CisMista, Hry, CisKarty, CisTypyKaret, CisKartyProTymy, HryKarty, HryTymy,\
    HryZpravy, HryHlasovani, CisHryNastaveni, HryKartyHistorie, HryTymyPrijmy #, InvesticeKolo

import random
import logging
from time import localtime
from itertools import accumulate
from datetime import datetime
from collections import namedtuple, defaultdict, Counter
import pygal
import os

investmentCheck = []
teamsRef = []

################
#### config ####
################

# users_blueprint = Blueprint('users', __name__)
logging.basicConfig(filename='nfapp.log',
                    format='[%(asctime)s]  -  %(message)s',
                    datefmt='%d.%m.%Y %H:%M:%S',
                    level=logging.INFO)

VVJ = 1
VRB = 2
OBD = 3
SRV = 4
MKT = 5
POJ = 6
EXP = 7
PUJ = 8
VYZ = 11
PR = 12
HRZ = 13

# slovnik vyhodnocujicich SQL --
# vyhodnoceni_SQL = read_sheet.read_sql_commands()
# --

# inv_dict = {}
# for ctype in db.session.query(CisTypyKaret):
#     inv_dict[ctype.kod] = ctype.typk_id
inv_dict = {'VVJ': 1, 'VRB': 2, 'OBD': 3, 'SRV': 4, 'MKT': 5, 'POJ': 6, 'EXP': 7, 'PUJ': 8}


class GameState():
    def __init__(self):
        self.hra_id = None
        self.teams = []
        self.n_teams = 0
        self.team_data = []
        self.karty = []
        self.card_PR = None
        self.winners_PR = ''
        self.team_name = None
        self.team_id = None
        self.role = None
        self.round_state = 'stopped'
        self.round_no = 0
        self.round_count = 0
        self.round_evaluated = False
        self.investments = defaultdict(list)
        self.investments_accepted = defaultdict(list)
        self.loans = defaultdict(list)
        self.loans_accepted = defaultdict(list)
        # self.invested = defaultdict(lambda: [False, False])
        self.logged_in = False

    def __repr__(self):
        return 'Game: hra_id={}, teams={}'.format(self.hra_id, [t.tym_id for t in self.teams if t.hra_id == self.hra_id])

    # Unused, may need to fix round_count if used
    def reset(self):
        self.teams = []
        self.team_data = []
        self.karty = []
        self.card_PR = None
        self.round_state = 'stopped'
        self.round_no = 0
        self.round_evaluated = False
        # self.investments = defaultdict(list)
        # self.invested = defaultdictlambda: [False, False])
        # self.invested = defaultdict(list)
        self.reset_investments()
        self.reset_loans()

    def set_game(self, hra_id):
        self.reset()
        self.hra_id = hra_id
        self.karty = get_cards()
        self.card_PR = update_pr(0)
        self.teams = get_teams()
        self.team_data = get_team_data()
        self.n_teams = len(self.team_data)
        self.round_state = 'stopped'
        self.round_no = 0
        self.round_count = get_round_count()
        self.round_evaluated = False
        logprint("set_game")
        logprint(self.round_count)

    def create_game(self, new_game):
        self.reset()
        self.hra_id = new_game.hra_id
        draw_cards(new_game)
        self.karty = get_cards()
        self.card_PR = update_pr(0)
        self.round_no = 0
        self.round_count = get_round_count()
        # self.teams = get_teams()
        # self.team_data = get_team_data()
        # self.n_teams = len(self.team_data)
        logprint("create_game")

    def reset_investments(self):
        self.investments = defaultdict(list)
        self.investments_accepted = defaultdict(list)

    def reset_loans(self):
        self.loans = defaultdict(list)
        self.loans_accepted = defaultdict(list)

    def logout(self):
        self.role = None
        self.logged_in = False


    def login(self, team_name, team_id, role, hra_id):
        self.team_name = team_name
        self.team_id = team_id
        self.role = role
        self.hra_id = hra_id
        self.logged_in = True

game = GameState()


##########################
#### helper functions ####
##########################


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('Pro tuto akci je nutné být přihlášen.')
            return redirect(url_for('login'))
    return wrap


def admin_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        # if 'logged_in' in session and session['role'] == 'admin':
        if game.logged_in and game.role == 'admin':
            return test(*args, **kwargs)
        else:
            flash('Pro tuto akci je nutné být přihlášen jako správce.')
            return redirect(url_for('login'))
    return wrap


def logprint(msg, print_it=True, log_it=True):
    if print_it:
        print(msg)
    if log_it:
        logging.info(msg)


def render_game(error, teams_error="", control=True, first=False):
    # team_data = get_team_data()
    # if 'round_state' not in session:
    #     session['round_state'] = 'stopped'
    # investitions = get_investitions(session['team_id'])
    game.team_data = get_team_data()
    cards_info = get_cards_info()
    mkt_mess_form = None
    mkt_mess_voting_form = None
    # if game.hra_id is not None:
    #     graph_data = get_graph_data()
    # else:
    #     graph_data = None

    if game.team_name == 'admin':
        pujcky = []
        majetek = None
        payment_form = SpecialPaymentForm(request.form)
    else:
        pujcky = get_loans()
        majetek = get_majetek(game.team_id)
        payment_form = None

        get_number_of_investments(game.team_id, MKT)
        # if game.round_state == 'running' and db.session.query(HryKarty).filter_by(
        #         hra_id=game.hra_id, tym_id=game.team_id, ciskarta.typ_karta.typk_id=MKT).first() is not None:
        if game.round_state == 'running' and get_number_of_investments(game.team_id, MKT) > 0:
            mkt_mess_form = MktMessageForm(request.form)

        elif game.round_state == 'stopped' and game.round_no > 0:
            if db.session.query(HryHlasovani).filter_by(hra_id=game.hra_id, tym_id=game.team_id).first() is None:
                mkt_mess_voting_form = MktMessageVotingForm(request.form)
                titles = get_mkt_titles()
                # nahodne zamichani
                random.shuffle(titles)
                # mkt_mess_voting_form.example.choices = titles
                mkt_mess_voting_form.item.choices = titles
                mkt_mess_voting_form.process()
    tce = len(teams_error) > 0
    print("Error: {} ".format(tce))
    return render_template('game.html',team_check_error=tce, error_teams=teams_error, game=game, cards_info=cards_info, pujcky=pujcky, majetek=majetek,
                           mkt_mess_form=mkt_mess_form, mkt_mess_voting_form=mkt_mess_voting_form,
                           payment_form=payment_form, winners_PR=game.winners_PR, control=control, first=first)


def team_id2team_name(team_id):
    name = db.session.query(HryTymy.nazev_firmy).filter_by(hra_id=game.hra_id, tym_id=team_id).first()[0]
    return name


def get_mista():
    return db.session.query(CisMista).order_by(CisMista.nazev.asc())


def get_hry():
    return db.session.query(Hry).order_by(Hry.hra_id.desc())


def draw_cards_by_id(cards_setup, game_id, typk_id, session):
    # - zjistit ID vsech karet daneho typu
    # TODO: uvazuji pouze karty, ktere maji vyhodnoceni
    # cards_ids2 = [id[0] for id in db.session.query(CisKarty.karta_id).filter_by(typk_id=typk_id)]
    # cards_ids = [id[0] for id in session.query(CisKarty.karta_id).filter_by(typk_id=typk_id)
    #              if id[0] in vyhodnoceni_SQL]

    cards_ids = [c.karta_id for c in session.query(CisKarty).filter_by(typk_id=typk_id) if c.vyhodnoceni is not None]

    # - samplovat ID dle poctu typu v cards.setup
    n_cards = [x.pocet for x in cards_setup if x.typk_id == typk_id][0]

    # P&R se zamichaji vsechny, v tabulce maji udany pocet=99
    # musim proto zajistit, aby mi n_cards = len(cards_ids), jinak Error
    # TODO: tahle podminka funguje i pro pripad, ze mame mene karet s vyhodnocenim nez pozadovanych karet
    if n_cards > len(cards_ids):
        n_cards = len(cards_ids)

    # vytahni nahodne id karet
    drawed_ids = random.sample(cards_ids, n_cards)

    # - pridat vylosovane karty do databaze HryKarty
    # card_no = db.session.query(func.count(CisKarty.karta_id)).scalar()
    card_no = session.query(func.count(HryKarty.karta_hry_id)).scalar()
    for karta_id in drawed_ids:
        card = session.query(CisKarty).filter_by(karta_id=karta_id).first()
        card_no += 1
        session.add(HryKarty(game_id, karta_id, card_no, 0, 0, card.castka, None))


def draw_cards(cur_game, only_investments=False, session=None):
    if session is None:
        session = db.session

    # cur_game = Hry.query.filter_by(hra_id=game.hra_id).first()
    cards_setup = CisKartyProTymy.query.filter_by(poc_tymu=cur_game.poc_tymu)

    if not only_investments:
        # vybrani karet, ktere se maji losovat
        to_draw = CisTypyKaret.query.filter_by(losovat=True)
        # losovani karet
        for ctype in to_draw:
            typk_id = ctype.typk_id
            # print('typk_id: {}'.format(typk_id))
            draw_cards_by_id(cards_setup, cur_game.hra_id, typk_id, session)

    # pridavani investic
    # inv_ids = ['VVJ', 'VRB', 'OBD', 'SRV', 'MKT']
    inv_ids = [VVJ, VRB, OBD, SRV, MKT]
    # card_no = db.session.query(func.count(CisKarty.karta_id)).scalar()
    card_no = session.query(func.count(HryKarty.karta_hry_id)).scalar()
    for typk_id in inv_ids:
        cards = CisKartyProTymy.query.filter_by(poc_tymu=cur_game.poc_tymu, typk_id=typk_id)

        for ctype in cards:
            karta_id = CisKarty.query.filter_by(typk_id=ctype.typk_id, uroven=ctype.uroven).first().karta_id
            for c in range(ctype.pocet):
                card_no += 1
                # print('INSERTING: HryKarty(hra_id={}, karta_id={}, poradi={}, cena={}, naklady={}, prijem={}, 0)'.
                #       format(game.hra_id, karta_id, card_no, ctype.cena, ctype.naklady, ctype.prijem))
                session.add(HryKarty(cur_game.hra_id, karta_id, card_no, ctype.cena, ctype.naklady, ctype.prijem, None))

    # for c in db.session.query(HryKarty):
    #     # print(db.session.query(CisKarty).filter_by(karta_id=c.karta_id).first().nazev)
    #     print('typ: {}, nazev: {}'.format(c.cis_karta.typ_karta.kod, c.cis_karta.nazev))
    # print('---')
    session.commit()

def get_round_count():
    # if 'hra_id' in session:
    if game.hra_id is not None:
        return db.session.query(Hry.poc_kol).filter_by(hra_id=game.hra_id).first()[0]
    else:
        return 0


def get_cards():
    if game.hra_id is not None:
        return db.session.query(HryKarty).filter_by(hra_id=game.hra_id).order_by(HryKarty.poradi.asc())
    else:
        return []


def get_teams():
    # if 'hra_id' in session:
    if game.hra_id is not None:
        return list(db.session.query(HryTymy).filter_by(hra_id=game.hra_id).order_by(HryTymy.tym_id.asc()))
    else:
        return []


def get_team_data():
    teams = get_teams()
    # team_data = namedtuple('TeamData', 'nazev vyvoj vyroba obchod servis marketing')
    data = []

    for t in teams:
        nazev = t.nazev_firmy
        team_data = {'nazev': nazev, 'tym_id': t.tym_id, 'ma_vyrobek': 0,
                     'vyvoj': 0, 'vyroba': 0, 'obchod': 0, 'servis': 0, 'marketing': 0}
        team_data['ma_vyrobek'] = db.session.query(HryTymy.ma_vyrobek).filter_by(hra_id=game.hra_id,
                                                                                 tym_id=t.tym_id).first()[0]
        team_data['ma_nazev'] = db.session.query(HryTymy.ma_nazev).filter_by(hra_id=game.hra_id,
                                                                                 tym_id=t.tym_id).first()[0]
        team_data['ma_logo'] = db.session.query(HryTymy.ma_logo).filter_by(hra_id=game.hra_id,
                                                                                 tym_id=t.tym_id).first()[0]

        karty = db.session.query(HryKarty).filter_by(hra_id=game.hra_id, tym_id=t.tym_id)
        for k in karty:
            # filtrovat karty
            typk_id = k.cis_karta.typ_karta.typk_id
            if typk_id == VVJ:
                team_data['vyvoj'] += 1
            elif typk_id == VRB:
                team_data['vyroba'] += 1
            elif typk_id == OBD:
                team_data['obchod'] += 1
            elif typk_id == SRV:
                team_data['servis'] += 1
            elif typk_id == MKT:
                team_data['marketing'] += 1
        data.append(team_data)
    return data


def publish_investments():
    # investments = InvesticeKolo.query.all()
    investments = HryKartyHistorie.query.filter_by(kolo=game.round_no)
    for inv in investments:
        # HryKarty.update().where(HryKarty==inv.karta_hry_id).values(tym_id=inv.tym_id)
        # update(HryKarty).where(HryKarty.karta_hry_id == inv.karta_hry_id).values(tym_id=inv.tym_id)
        db.session.query(HryKarty).filter_by(karta_hry_id=inv.karta_hry_id).update({"tym_id": inv.tym_id})
    db.session.commit()


def start_round():
    if game.round_state == 'stopped':
        game.round_no += 1
        db.session.query(Hry).filter_by(hra_id=game.hra_id).update({"akt_kolo": game.round_no})
        logprint('\n----------------------------------------------------------------------------------------\n')
        logprint('KOLO {} - START'.format(game.round_no))
    else:
        logprint('KOLO {} - POKRACOVANI'.format(game.round_no))
    game.card_PR = update_pr()
    game.round_state = 'running'
    game.round_evaluated = False
    game.winners_PR = ''
    render_game(None)


def stop_round():
    game.round_state = 'stopped'
    logprint('KOLO {} - STOP'.format(game.round_no))
    publish_investments()
    game.reset_investments()
    game.reset_loans()


def update_pr(idx=None):
    if idx is None:
        idx = game.round_no - 1
    sql = "SELECT HK.karta_id FROM nf_hry_karty HK INNER JOIN `nf_cis_karty` K ON HK.karta_id = K.karta_id " \
          "INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK.hra_id={} AND T.kod='P&R' " \
          "ORDER BY HK.poradi".format(game.hra_id)
    res = [r[0] for r in db.engine.execute(sql)]
    card_id = res[idx]
    card = db.session.query(HryKarty).filter_by(karta_id=card_id).first()
    return card


def eval_round():
    logprint('VYHODNOCENI KOLA')
    # ----------------------------------------------------------------------------------------------------
    # ----  INVESTICE  ----
    # prijem z aktivnich investic (investice ziskane v minulych kolech)
    inv_types = ['VVJ', 'VRB', 'OBD', 'SRV', 'MKT']
    for itype in inv_types:
        # sql = "SELECT HK.karta_hry_id, HK.tym_id FROM nf_hry_karty HK INNER JOIN `nf_cis_karty`K ON HK.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK.hra_id = #hra_id# AND T.kod = '#inv_type#' AND NOT HK.tym_id IS NULL"
        sql = "SELECT HK.karta_hry_id, HK.tym_id, HKH.kolo FROM nf_hry_karty HK INNER JOIN `nf_hry_karty_historie` HKH " \
              "ON HK.karta_hry_id = HKH.karta_hry_id INNER JOIN `nf_cis_karty`K ON HK.karta_id = K.karta_id INNER JOIN " \
              "`nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK.hra_id = #hra_id# AND T.kod = '#code#' AND NOT " \
              "HK.tym_id IS NULL"
        sql = sql.replace('#hra_id#', str(game.hra_id))
        sql = sql.replace('#code#', itype)
        result = db.engine.execute(sql)

        for karta_hry_id, tym_id, kolo in result:
            # investice se zapocita pouze pokud ma dany tym hotovy vyrobek
            if db.session.query(HryTymy.ma_vyrobek).filter_by(tym_id=tym_id).first()[0] and kolo < game.round_no:
            # if kolo < game.round_no:
                prijem, naklady = db.session.query(HryKarty.prijem, HryKarty.naklady).filter_by(karta_hry_id=karta_hry_id).first()

                # MKT se vyhodnocuje jinak nez ostatni
                if itype == 'MKT':
                    # test, zda ma firma nazev
                    if not db.session.query(HryTymy.ma_nazev).filter_by(tym_id=tym_id).first()[0]:
                        prijem -= db.session.query(Hry.mkt_nazev).filter_by(hra_id=game.hra_id).first()[0]
                    # test, zda ma firma logo
                    if not db.session.query(HryTymy.ma_logo).filter_by(tym_id=tym_id).first()[0]:
                        prijem -= db.session.query(Hry.mkt_logo).filter_by(hra_id=game.hra_id).first()[0]
                    # test, zda firma napsala zpravu
                    if db.session.query(HryZpravy.zprava_id).filter_by(tym_id=tym_id, kolo=game.round_no).first() is None:
                        prijem -= db.session.query(Hry.mkt_logo).filter_by(hra_id=game.hra_id).first()[0]

                # uprava majetku
                update_majetek(tym_id, prijem - naklady, 'Investice {}'.format(itype))
                logprint('Vyhodnocuji: karta_hry_id={}, tym_id={}, kolo={}, prijem={}, naklady={}'.\
                      format(karta_hry_id, tym_id, kolo, prijem, naklady))
                # db.session.commit()

    # ----------------------------------------------------------------------------------------------------
    # ----  P&R  ----
    # vyhodnoceni efektu P&R
    # splnuje-li podminku vice tymu, castka se deli
    card = db.session.query(CisKarty).join(HryKarty).filter(CisKarty.karta_id==game.card_PR.karta_id).first()
    result = db.engine.execute(card.vyhodnoceni.replace('#hra_id#', str(game.hra_id)))
    if result.returns_rows:
        team_ids = []
        # zjistim tymy splnujici podminky P&R karty
        for r in result:
            # r = (hra_id, tym_id, typk_id, kod, poc_karet)
            team_id = r[1]
            # team_id = r.tym_id
            team_ids.append(team_id)

        # urceni castky
        if len(team_ids) > 0:
            castka = int(card.castka / len(team_ids))

            # updatuji majetek
            # musim to udelat separatne, jelikoz potrebuji zjistit celkvoy pocet tymu, ktere se podeli o castku
            team_names = []
            for team_id in team_ids:
                team_name = db.session.query(HryTymy.nazev_firmy).filter_by(tym_id=team_id).first()[0]
                team_names.append(team_name)

                prev_majetek = get_majetek(team_id)
                update_majetek(team_id, castka, 'P&R id={}'.format(game.card_PR.karta_id))
                logprint("P&R '{}' (id={}) - získal tým '{}' (id={}), odměna={}, majetek: {} -> {}". \
                         format(card.nazev, card.karta_id, team_name, team_id, castka, prev_majetek, get_majetek(team_id)))
            if len(team_names) > 1:
                game.winners_PR = ', '.join(team_names)
            elif len(team_names) == 1:
                game.winners_PR = team_names[0]
        else:
            logprint("P&R '{}' (id={}) - nesplňuje žádný tým".format(card.nazev, card.karta_id))

    # ----------------------------------------------------------------------------------------------------
    # ----  HROZBY  ----
    # predani a vyhodnoceni hrozeb (kdo ma kartu pote u sebe, ztraci; od 2. nebo 3. kola)
    # splnuje-li podminku vice tymu, neziska nikdo nic
    # TODO: zjistit zda od 2. nebo 3. kola
    sql = "SELECT HK.karta_id, K.vyhodnoceni, K.nazev FROM nf_hry_karty HK " \
          "INNER JOIN `nf_cis_karty`K ON HK.karta_id = K.karta_id " \
          "INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id " \
          "WHERE HK.hra_id = #hra_id# AND T.kod = '#code#'"
    sql = sql.replace('#hra_id#', str(game.hra_id))
    sql = sql.replace('#code#', 'HRZ')
    hry_cards = db.engine.execute(sql)

    for karta_id, vyhodnoceni, nazev in hry_cards:
        # TODO: vyhodnocovat pouze od kola 2 nebo 3
        result = db.engine.execute(vyhodnoceni.replace('#hra_id#', str(game.hra_id)))

        if result.returns_rows:
            win_ids = [r[1] for r in result]
            # win_ids = [r.MinTID for r in result]
            # hrozby se vyhodnocuji pouze pokud ji splnuje pouze jeden tym
            if len(win_ids) == 1:
                # for r in result:
                    # team_id = r.MinTID
                    # team_id = r[1]
                    team_id = win_ids[0]
                    team_name = db.session.query(HryTymy.nazev_firmy).filter_by(tym_id=team_id).first()[0]
                    castka = db.session.query(CisKarty.castka).filter_by(karta_id=karta_id).first()[0]

                    prev_majetek = get_majetek(team_id)
                    update_majetek(team_id, castka, 'HRZ id={}'.format(karta_id))
                    logprint("HRZ '{}' (id={}) - získal tým '{}' (id={}), postih={}, majetek: {} -> {}".\
                             format(nazev, karta_id, team_name, team_id, castka, prev_majetek, get_majetek(team_id)))
                    db.session.query(HryKarty).filter_by(karta_id=karta_id).update({'tym_id': team_id})
            else:
                logprint("HRZ '{}' (id={}) - podmínky nesplněny (žádný nebo více týmů).".format(nazev, karta_id))
                db.session.query(HryKarty).filter_by(karta_id=karta_id).update({'tym_id': None})
        else:
            logprint("HRZ '{}' (id={}) - podmínky nesplněny (žádný nebo více týmů).".format(nazev, karta_id))
            db.session.query(HryKarty).filter_by(karta_id=karta_id).update({'tym_id': None})

    # ----------------------------------------------------------------------------------------------------
    # ----  VYZVY  ----
    # vyhodnoceni splneni vyzev (pouze zmenil-li se majitel karty, pri shode nikdo nic)
    # splnuje-li podminku vice tymu, neziska nikdo nic
    # format SQL vysledku: (tym_id, typk_id, kod, poc_karet )
    sql = "SELECT HK.karta_id, K.vyhodnoceni, K.nazev FROM nf_hry_karty HK " \
          "INNER JOIN `nf_cis_karty`K ON HK.karta_id = K.karta_id " \
          "INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id " \
          "WHERE HK.hra_id = #hra_id# AND T.kod = '#code#'"
    sql = sql.replace('#hra_id#', str(game.hra_id))
    sql = sql.replace('#code#', 'VYZ')
    vyz_cards = db.engine.execute(sql)

    for karta_id, vyhodnoceni, nazev in vyz_cards:
        # not IsNull(HK.tym_id) -> MS Access ?
        result = db.engine.execute(vyhodnoceni.replace('#hra_id#', str(game.hra_id)))

        if result.returns_rows:
            win_ids = [r.tym_id for r in result]
            if len(win_ids) == 1:
                team_id = win_ids[0]
                team_name = db.session.query(HryTymy.nazev_firmy).filter_by(tym_id=team_id).first()[0]
                prev_team_id = db.session.query(HryKarty.tym_id).filter_by(karta_id=karta_id).first()[0]
                if team_id != prev_team_id:
                    castka = db.session.query(CisKarty.castka).filter_by(karta_id=karta_id).first()[0]

                    prev_majetek = get_majetek(team_id)
                    update_majetek(team_id, castka, 'VYZ id={}'.format(karta_id))
                    logprint("VYZ '{}' (id={}) - získal tým '{}' (id={}), odmena={}, majetek: {} -> {}".\
                             format(nazev, karta_id, team_name, team_id, castka, prev_majetek, get_majetek(team_id)))
                    logprint(get_majetek(team_id))
                    db.session.query(HryKarty).filter_by(karta_id=karta_id).update({'tym_id': team_id})
                else:
                    logprint("VYZ '{}' (id={}) - vlastní stejný tým: '{}' (id={})".format(
                             nazev, karta_id, team_name, team_id))
            elif len(win_ids) > 1:
                logprint("VYZ '{}' (id={}) - splňuje více týmů -> nevyhodnocuji.".format(nazev, karta_id))
                db.session.query(HryKarty).filter_by(karta_id=karta_id).update({'tym_id': None})
            else:  # len(win_ids) == 0
                logprint("VYZ '{}'(id={}) - podmínky nesplněny (žádný nebo více týmů).".format(nazev, karta_id))
                db.session.query(HryKarty).filter_by(karta_id=karta_id).update({'tym_id': None})
        else:
            logprint("VYZ '{}'(id={}) - podmínky nesplněny (žádný nebo více týmů).".format(nazev, karta_id))
            db.session.query(HryKarty).filter_by(karta_id=karta_id).update({'tym_id': None})

    # naklady z pujcek
    team_ids = db.session.query(HryTymy.tym_id).filter_by(hra_id=game.hra_id)
    for team_id in team_ids:
        team_id = team_id[0]
        team_name = db.session.query(HryTymy.nazev_firmy).filter_by(tym_id=team_id).first()[0]
        loans = get_loans(team_id)
        naklady = 0
        for l in loans:
            naklady += db.session.query(HryKarty.naklady).filter_by(karta_hry_id=l['id']).first()[0]
        if naklady > 0:
            prev_majetek = get_majetek(team_id)
            update_majetek(team_id, -naklady, 'Naklady z pujcek')
            logprint('PUJ - {} (id={}) ma naklady z pujcek={}, majetek: {} -> {}'.\
                     format(team_name, team_id, naklady, prev_majetek, get_majetek(team_id)))
            logprint(get_majetek(team_id))

    # zpracovani hlasovani o MZ
    process_voting()

    # delete HryHlasovani
    HryHlasovani.query.delete()
    db.session.commit()

    # nastaveni flagu
    game.round_evaluated = True


def get_cards_info():
    info = {}
    types = ['VVJ', 'VRB', 'OBD', 'SRV', 'MKT']
    if game.hra_id is not None:
        for t in types:
            sql = "SELECT HK.tym_id, HK.cena, K.ikony_oblasti FROM nf_hry_karty HK INNER JOIN `nf_cis_karty`K ON " \
                  "HK.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE " \
                  "HK.hra_id = {} AND T.kod = '{}'".format(game.hra_id, t)
            query = db.engine.execute(sql)
            cards = [c for c in query]
            free_cards = [c for c in cards if c[0] is None]
            if free_cards:
                next_cost = min(free_cards, key=lambda x: x[1])[1]
            else:
                next_cost = None
            n_remaining = len(free_cards)
            # print("'{}', n rem: {}, next cost: {}".format(t, n_remaining, next_cost))
            iko_path = cards[0][2]
            if iko_path[0] != '/':
                iko_path = '/' + iko_path
            info[t] = {'n_remaining': n_remaining, 'next_cost': next_cost, 'ikona': iko_path}
    return info


def get_loans(team_id=None):
    if team_id is None:
        team_id = game.team_id
    sql = "SELECT HK.karta_hry_id, K.castka FROM nf_hry_karty HK INNER JOIN `nf_cis_karty` K ON HK.karta_id = K.karta_id " \
          "INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id " \
          "WHERE HK.hra_id = {} AND HK.tym_id = {} AND T.kod = 'PUJ'".format(game.hra_id, team_id)
    try:
        query = db.engine.execute(sql)
        cards = [{'id': c[0], 'value': c[1]} for c in query]
    except:
        cards = []
    return cards


def get_mkt_titles():
    res = db.session.query(HryZpravy.tym_id, HryZpravy.titulek).filter_by(hra_id=game.hra_id, kolo=game.round_no)
    output = [(r[0], r[1]) for r in res]
    return output


def process_voting():
    voting = db.session.query(HryHlasovani.autor_id).filter_by(hra_id=game.hra_id, typ_hlasovani='MZ')
    hlasy = [c[0] for c in voting]

    # pocitani hlasu
    count = Counter(hlasy)
    freq_list = list(count.values())

    # pokud nikdo nehlasoval, ukonci metodu
    if not freq_list:
        return

    max_cnt = max(freq_list)
    n_items = freq_list.count(max_cnt)
    mc = count.most_common(n_items)

    logprint('Hlasovani: {}, mc = {}'.format(hlasy, mc))

    if not mc:  # empty list = no MKT messages found in the database
        logprint('Nenalezeny zadne MZ.')
    else:
        # odmena vitezum
        for winner, _ in mc:
            majetek = get_majetek(winner)
            mz_winner_reward = db.session.query(Hry.odm_zprava).filter_by(hra_id=game.hra_id).first()[0]
            logprint('vitez: {}, majetek: {}->'.format(winner, majetek), end='')
            db.session.query(HryTymy).filter_by(tym_id=winner).update({"majetek": majetek + mz_winner_reward})
            print(get_majetek(winner))

        # odmena tymum, kteri hlasovali pro viteze
        # najdu vsechny tymy dane hry
        teams = db.session.query(HryHlasovani.tym_id, HryHlasovani.autor_id).filter_by(hra_id=game.hra_id)
        # zjistim, ktere hlasovaly pro viteze
        voters = [t[0] for t in teams if t[1] in mc[0]]
        # odmenim je prictenim MZ_VOTER_REWARD k jejich majektu
        for v in voters:
            majetek = get_majetek(v)
            mz_voter_reward = db.session.query(Hry.odm_zprava_hlas).filter_by(hra_id=game.hra_id).first()[0]
            logprint('hlasujici: {}, majetek: {}->'.format(v, majetek), end='')
            db.session.query(HryTymy).filter_by(tym_id=v).update({"majetek": majetek + mz_voter_reward})
            logprint(get_majetek(v))
    db.session.commit()


def get_majetek(team_id, session=None):
    if session is None:
        session = db.session
    majetek = session.query(HryTymy.majetek).filter_by(tym_id=team_id).first()[0]
    return majetek


def update_majetek(team_id, amount, desc='', kolo=None, session=None):
    if session is None:
        session = db.session
    # pepocitani hodnoty majetku
    majetek = get_majetek(team_id, session)
    majetek += amount

    # aktualizace databaze
    session.query(HryTymy).filter_by(tym_id=team_id).update({"majetek": majetek})

    if kolo is None:
        kolo = game.round_no
    new_rec = HryTymyPrijmy(game.hra_id, kolo, team_id, amount, desc)
    session.add(new_rec)
    # db.session.commit()


def overwrite_cards(type, id_list, game_id, session=None):
    if session is None:
        session = db.session

    # find cards of given type
    res = session.query(HryKarty).join(CisKarty).filter(HryKarty.hra_id==game_id, CisKarty.typk_id==type)
    logprint('pred: {}'.format([r.karta_id for r in res]))

    # update found cards
    for c, new_id in zip(res, id_list):
        # db.session.query(HryKarty).filter_by(karta_hry_id=c.karta_hry_id).delete()
        # found new card
        card = session.query(CisKarty).filter_by(karta_id=new_id).first()

        db.session.query(HryKarty).filter_by(karta_hry_id=c.karta_hry_id).\
            update({"karta_id": card.karta_id, "prijem": card.castka})
    db.session.commit()

    res = session.query(HryKarty).join(CisKarty).filter(HryKarty.hra_id == game_id, CisKarty.typk_id == type)
    logprint('after update: {}'.format([r.karta_id for r in res]))


################
#### routes ####
################

@app.route('/')
def home():
    # return render_template('home.html')
    error = None
    print(game.logged_in)
    # if 'logged_in' in session:
    if game.logged_in:
        # return render_template('game.html', companies=get_companies(), error=error, username=session['username'], role=session['role'])
        if game.role == 'admin':
            return render_game(error, control=False, first=True)
        return render_game(error)
        # elif session['username'] == 'ROM':
        #     return render_template('user_home.html', error=error, username=session['username'])
    else:
        return redirect('/login')


@app.route('/logout/')
def logout():
    # session.pop('logged_in', None)
    # session.pop('user_id', None)
    # session.pop('role', None)
    # session.pop('username', None)
    game.logout()

    flash('Na viděnou!')
    # return redirect(url_for('home'))
    return redirect('/')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginTeamForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            # user = User.query.filter_by(name=request.form['name']).first()

            if request.form['game_key'] == 'mentor' and request.form['team_key'] == 'm3nt0rx':
                # session['logged_in'] = True
                # session['team_name'] = 'admin'
                # session['team_id'] = 0
                # session['role'] = 'admin'
                game.login('admin', 0, 'admin', game.hra_id)
                return render_game(error)

            # Zadany klic hry musi odpovidat klici v databazi
            # if Hry.query.filter_by(hra_id=request.form['game_key']).first() is not None:
            #     flash('Hra nalezena')
            #     team = CisTymy.query.filter_by(tym_klic=request.form['team_key']).order_by(
            #         CisTymy.dat_registrace.desc()).first()
            #
            #     # pokud se najde tym se zadanym klicem, dojde k prihlaseni
            #     if team is not None:
            #         # tym musel byt nedavno zaregistrovan
            #         # TODO: tohle je zrejme nesmysl - prehodnotit
            #         if datetime.now() - team.dat_registrace < 3:
            #             # session['logged_in'] = True
            #             # session['team_name'] = team.nazev
            #             # session['team_id'] = HryTymy.query.filter_by(hra_id=session['hra_id'], nazev_firmy=team.nazev).\
            #             #     first().tym_id
            #             # session['role'] = 'ROM'
            #             tym_id = HryTymy.query.filter_by(hra_id=session['hra_id'], nazev_firmy=team.nazev).first().tym_id
            #             game.login(team.nazev, tym_id, 'ROM')
            #             flash('Přihlášení proběhlo úspěšně. Vítej!')
            #             return render_game(error)
            #     else:
            #         error = 'Tým s daným klíčem nenalezen.'
            #
            # else:
            #     error = 'Hra nenalezena'

            hra = db.session.query(Hry).filter_by(klic=request.form['game_key']).first()
            if hra is not None:
                flash('Hra nalezena')

                sql = "SELECT T.nazev, T.tym_id, HT.hra_id FROM nf_cis_tymy T INNER JOIN `nf_hry_tymy` HT " \
                      "ON T.tym_id = HT.tym_id WHERE HT.hra_id = {} AND HT.klic = '{}'".\
                    format(hra.hra_id, request.form['team_key'])
                team = db.engine.execute(sql).first()
                # team = db.session.query(HryTymy).filter_by(hra_id=hra.hra_id, klic=request.form['team_key']).first()
                if team is not None:
                    game.login(team.nazev, team.tym_id, 'ROM', team.hra_id)
                    flash('Přihlášení proběhlo úspěšně. Vítej!')
                    return render_game(error)
                else:
                    error = 'Tým s daným klíčem nenalezen.'
            else:
                error = 'Hra nenalezena'

    return render_template('login.html', form=form, error=error, game=game)


# @app.route('/register/', methods=['GET', 'POST'])
# def register():
#     error = None
#     form = RegisterUserForm(request.form)
#     if request.method == 'POST':
#         if form.validate_on_submit():
#             new_user = User(form.name.data, bcrypt.generate_password_hash(form.password.data))
#             try:
#                 db.session.add(new_user)
#                 db.session.commit()
#                 flash('Děkujeme ze registraci. Přihlaš se, prosím.')
#                 return redirect(url_for('login'))
#             except IntegrityError:
#                 error = 'Zadaný uživatel již existuje.'
#                 return render_template('register.html', form=form, error=error)
#     return render_template('register.html', form=form, error=error)


@app.route('/register_teams/', methods=['GET', 'POST'])
def register_teams():
    error = None
    # form = TeamsDummyListForm()
    form = TeamsListForm()
    if request.method == 'GET':
        if len(game.teams) == 0:
            # form = TeamsListForm()
            # if 'hra_id' in session:
            if game.hra_id is not None:
                # hra = Hry.query.filter_by(hra_id=session['hra_id']).first()
                hra = Hry.query.filter_by(hra_id=game.hra_id).first()
                if hra is not None:
                    global teamsRef
                    teamsRef = []
                    num_teams = hra.poc_tymu
                    # teams_list = TeamsListForm()
                    for i in range(num_teams):
                        team_form = TeamForm()
                        team_form.team_name = 'tým {}'.format(i + 1)
                        team_form.team_key = 'klic{}'.format(i + 1)
                        team_form.team_date = datetime.now()
                        team_form.team_desc = 'popis'
                        team_form.team_num_players = 5
                        form.teams.append_entry(team_form)
                        if team_form.team_name not in teamsRef:
                            teamsRef.append(team_form.team_name)

                    render_template('register_teams.html', form=form, game=game)
                else:
                    error = 'Hra nenalezena.'
            else:
                error = 'Nenalezeno ID hry. Byla hra založena?'
        else:
            error = 'Týmy již registrovány.'
    #
    #     return render_template('register_teams.html', error=error, form=form)

    if request.method == 'POST':
        if len(game.teams) == 0:
            if form.validate_on_submit():
                # hra = Hry.query.filter_by(hra_id=session['hra_id']).first()
                hra = Hry.query.filter_by(hra_id=game.hra_id).first()
                for team in form.teams:
                    # zadani tymu do databaze
                    new_team = CisTymy(team.team_name.data, team.team_date.data, team.team_desc.data, 'A')
                    try:
                        db.session.add(new_team)
                        db.session.commit()
                        # print('tym ulozen')
                    except:
                        error = 'Něco se pokazilo při ukládání týmu do databáze.'
                        # print('ERROR pri ukladani tymu')

                    # sparovani hry a tymu v databazi
                    new_hra_tym = HryTymy(hra.hra_id, new_team.tym_id, team.team_key.data, new_team.nazev, "", 0,
                                        False, False, False)
                    try:
                        db.session.add(new_hra_tym)
                        db.session.commit()
                    except:
                        error = 'Něco se pokazilo při párování hry a týmu.'

                if error is None:
                    flash('Registrace proběhla úspěšně.')
                game.teams = get_teams()
                game.team_data = get_team_data()
                game.n_teams = len(game.team_data)

                # record input wealth
                input_wealth = hra.majetek
                for t in game.teams:
                    update_majetek(t.tym_id, input_wealth, 'Pocatecni majetek')
                db.session.commit()

                return render_game(error)
        else:
            error = 'Týmy již registrovány.'

    return render_template('register_teams.html', error=error, form=form, game=game)
    # return render_game(error)


@app.route('/places/', methods=['GET', 'POST'])
@admin_required
def places():
    error = None
    return render_template('places.html', form=RegisterPlaceForm(request.form), mista=get_mista(),
                           error=error, game=game)


@app.route('/register_place/', methods=['GET', 'POST'])
@admin_required
def register_place():
    error = None
    form = RegisterPlaceForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_place = CisMista(form.nazev.data, form.ulice.data, form.obec.data, form.psc.data, form.souradnice.data)
            try:
                db.session.add(new_place)
                db.session.commit()
                flash('Nové místo úspěšně přidáno.')
                # return render_template('admin_home.html', error=error, username=session['username'])
                # return redirect(url_for('users.places'))
                return render_template('places.html', form=form, mista=get_mista(), error=error, game=game)
            except IntegrityError:
                error = 'Zadané místo již existuje.'
                # return render_template('register_place.html', form=form, error=error, username=session['username'])
                # return redirect(url_for('users.places'))
            return render_template('places.html', form=form, mista=get_mista(), error=error, game=game)
    # return render_template('register_place.html', form=form, error=error, username=session['username'])
    return render_template('places.html', form=form, mista=get_mista(), error=error, game=game)


@app.route('/setup_cards/', methods=['GET', 'POST'])
@admin_required
def setup_cards():
    error = None
    # pr_form = CardsListForm()
    # vyzvy_form = CardsListForm()
    # hrozby_form = CardsListForm()
    # cards_form = CardsListForm()
    cards_form = CardsListForm(request.form)

    if request.method == 'GET':
        if game.hra_id is not None:
            hra = Hry.query.filter_by(hra_id=game.hra_id).first()
            if hra is not None:
                # cards_form = CardsListForm(request.form)
                num_teams = hra.poc_tymu
                # num_kol = hra.poc_kol

                # get PR cards
                # pr_cards = [(c.karta_id, c.nazev) for c in session.query(CisKarty).filter_by(typk_id=PR)]
                pr_cards = [c for c in db.session.query(CisKarty).filter_by(typk_id=PR) if c.vyhodnoceni]

                # get VYZ cards
                # vyz_cards = [(c.karta_id, c.nazev) for c in db.session.query(CisKarty).filter_by(typk_id=VYZ)]
                vyz_cards = [c for c in db.session.query(CisKarty).filter_by(typk_id=VYZ) if c.vyhodnoceni]

                # get HRZ cards
                # hrz_cards = [(c.karta_id, c.nazev) for c in db.session.query(CisKarty).filter_by(typk_id=HRZ)]
                hrz_cards = [c for c in db.session.query(CisKarty).filter_by(typk_id=HRZ) if c.vyhodnoceni]

                # get the correct numbers of cards
                cards_setup = CisKartyProTymy.query.filter_by(poc_tymu=num_teams)
                n_pr = [x.pocet for x in cards_setup if x.typk_id == PR][0]
                # n_pr2 = db.session.query(CisKartyProTymy.pocet).filter_by(poc_tymu=num_teams, typk_id=PR).first()[0]
                n_vyz = [x.pocet for x in cards_setup if x.typk_id == VYZ][0]
                n_hrz = [x.pocet for x in cards_setup if x.typk_id == HRZ][0]

                # create cards form
                # for i in range(hra.poc_kol):
                #     card_form = CardForm()
                #     cards_form.pr_cards.append_entry(card_form)
                # for i in range(n_vyz):
                #     card_form = CardForm()
                #     cards_form.vyz_cards.append_entry(card_form)
                # for i in range(n_hrz):
                #     card_form = CardForm()
                #     cards_form.hrz_cards.append_entry(card_form)

                return render_template('setup_cards.html', form=cards_form, error=error, game=game,
                                       pr_cards=pr_cards, vyz_cards=vyz_cards, hrz_cards=hrz_cards,
                                       n_kol=hra.poc_kol, n_vyz=n_vyz, n_hrz=n_hrz)
            else:
                error = 'Hra nenalezena.'
                return render_game(error)
        else:
            error = 'Nejprve je nutné založit hru.'
            return render_game(error)

    elif request.method == 'POST':
        hra = Hry.query.filter_by(hra_id=game.hra_id).first()
        num_teams = hra.poc_tymu
        cards_setup = CisKartyProTymy.query.filter_by(poc_tymu=num_teams)
        # n_pr2 = db.session.query(CisKartyProTymy.pocet).filter_by(poc_tymu=num_teams, typk_id=PR).first()[0]
        n_vyz = [x.pocet for x in cards_setup if x.typk_id == VYZ][0]
        n_hrz = [x.pocet for x in cards_setup if x.typk_id == HRZ][0]
        # cards_form = CardsListForm(request.form)
        if cards_form.validate_on_submit():
            # get card IDs
            pr_ids = [request.form.get('pr_{}'.format(x)) for x in range(hra.poc_kol)]
            vyz_ids = [request.form.get('vyz_{}'.format(x)) for x in range(n_vyz)]
            hrz_ids = [request.form.get('hrz_{}'.format(x)) for x in range(n_hrz)]

            # print
            logprint('Vybrany P&R s ID: {}'.format(pr_ids))
            logprint('Vybrany VYZ s ID: {}'.format(vyz_ids))
            logprint('Vybrany HRZ s ID: {}'.format(hrz_ids))

            # overwrite cards
            # -- PR
            overwrite_cards(PR, pr_ids, hra.hra_id)
            overwrite_cards(VYZ, vyz_ids, hra.hra_id)
            overwrite_cards(HRZ, hrz_ids, hra.hra_id)

        if error is None:
            flash('Výběr karet proběhl úspěšně.')

    return render_game(error)


@app.route('/create_game/', methods=['GET', 'POST'])
@admin_required
def create_game():
    error = None
    # form = CreateGameForm(request.form)
    game_form = CreateGameForm()

    teamsRef = []
    investmentCheck = []

    if request.method == 'POST':
        if game_form.validate_on_submit():
            new_game = Hry(game_form.nazev.data, game_form.dat_hrani.data, game_form.misto_id.data,
                           game_form.popis.data, game_form.klic.data, game_form.majetek.data,
                           game_form.karty_za_kolo.data, game_form.poc_tymu.data, game_form.poc_kol.data, 0, 'S',
                           game_form.mkt_nazev.data, game_form.mkt_logo.data, game_form.mkt_zprava.data,
                           game_form.odm_zprava.data, game_form.odm_zprava_hlas.data, game_form.odm_robot1.data,
                           game_form.odm_robot1_hlas.data, game_form.odm_robot2.data, game_form.odm_robot2_hlas.data,
                           game_form.odm_robot3.data, game_form.odm_robot3_hlas.data, game_form.cena_cert.data,
                           game_form.odm_cert.data)
            try:
                db.session.add(new_game)
                db.session.commit()
                # session['hra_id'] = new_game.hra_id
                # game.reset()
                # game.hra_id = new_game.hra_id
                # draw_cards(new_game)
                # game.karty = get_cards()
                # game.card_PR = update_pr(0)
                # game.n_teams = len(game.team_data)
                game.create_game(new_game)
                flash('Nová hra úspěšně založena.')
                game.winners_PR = ''
                # return render_template('game.html', companies=get_companies(), error=error, username=session['username'])
                return render_game(error)
            except IntegrityError:
                error = 'Hra se zadaným názvem již existuje.'
                # return render_template('set_game.html', form=form, error=error, username=session['team_name'], mista=get_mista())
    # return render_template('set_game.html', form=form, error=error, team_name=session['team_name'], mista=get_mista())
    return render_template('create_game.html', form=game_form, error=error, game=game, mista=get_mista())


@app.route('/set_game/', methods=['GET', 'POST'])
@admin_required
def set_game():
    error = None
    if request.method == 'POST':
        selected_hra_id = request.form.get('select_hra')
        game.set_game(selected_hra_id)
        return render_game(None)
    return render_template('games.html', form=CreateGameForm(request.form), hry=get_hry(), mista=get_mista(),
                           error=error, game=game)


@app.route('/run_game/')
@admin_required
def run_game():
    pass


@app.route('/game/')
@login_required
def overview():
    error = None
    # return render_template(
    #     'game.html',
    #     companies=get_companies(),
    #     username=session['username'],
    #     role=session['role']
    # )
    return render_game(error)


@app.route('/secret_admin_login/')
def secret_admin_login():
    # session['logged_in'] = True
    # session['team_name'] = 'admin'
    # session['role'] = 'admin'
    # print(game)
    game.login('admin', 0, 'admin', game.hra_id)
    return redirect('/')

@app.route('/new_admin_tab/')
def new_admin_tab():
    error = None
    game.login('admin', 0, 'admin', game.hra_id)
    return render_game(error)


@app.route('/user_login/<int:id>')
def user_login(id):
    team_name = 'tým {}'.format(id)
    if game.hra_id is None:  # 'hra_id' not in session:
        # error = 'Nejprve je nutné vytvořit hru.'
        flash('Nejprve je nutné vytvořit hru a registrovat týmy.')
        return render_template('home.html', game=game)
    # elif HryTymy.query.filter_by(hra_id=session['hra_id'], nazev_firmy=team_name).first() is None:
    elif HryTymy.query.filter_by(hra_id=game.hra_id, nazev_firmy=team_name).first() is None:
        flash("Tým '{}' není registrován.".format(team_name))
        return render_template('home.html', game=game)
    else:
        # session['logged_in'] = True
        # session['team_name'] = 'tým {}'.format(id)
        # session['team_id'] = HryTymy.query.filter_by(hra_id=session['hra_id'],
        #                                              nazev_firmy=session['team_name']).first().tym_id
        # session['role'] = 'ROM'
        team = HryTymy.query.filter_by(hra_id=game.hra_id, nazev_firmy=team_name).first()
        game.login(team.nazev_firmy, team.tym_id, 'ROM', team.hra_id)
        return render_game(None)


@app.route('/investment/<string:type>')
def investment(type):
    # global investitions
    error = None

    # potvrzeni vyberu
    if type == 'OK':
        # majetek = get_majetek()

        # investice
        for i, (inv, acc) in enumerate(zip(game.investments[game.team_name], game.investments_accepted[game.team_name])):
            if not acc:
                # kdyz napisu podminku jako HryKarty.tym_id is None, tak to nefunguje
                card = db.session.query(HryKarty).join(CisKarty).filter(
                    HryKarty.hra_id == game.hra_id, HryKarty.tym_id == None, CisKarty.typk_id == inv_dict[inv]). \
                    order_by(HryKarty.karta_id).first()
                db.session.query(HryKarty).filter_by(karta_hry_id=card.karta_hry_id).update({"tym_id": -game.team_id})

                # aktualizuj majetek
                # majetek -= card.cena
                # db.session.query(HryTymy).filter_by(tym_id=game.team_id).update({"majetek": majetek})
                update_majetek(game.team_id, -card.cena, 'Investice do {}'.format(inv))

                # zapsani do tabulky
                # new_inv = InvesticeKolo(card.karta_hry_id, card.cis_karta.typk_id, game.team_id)
                new_record = HryKartyHistorie(card.karta_hry_id, game.round_no, game.team_id, datetime.now())
                db.session.add(new_record)
                game.investments_accepted[game.team_name][i] = True

                # log
                logprint("Tým '{}' investoval do '{}'".format(game.team_name, inv))

        # pujcky
        for i, (inv, acc) in enumerate(zip(game.loans[game.team_name], game.loans_accepted[game.team_name])):
            if not acc:
                # urcit typk_id jako PUJ
                typk_id = inv_dict['PUJ']
                # uroven je dana poslednim znakem, PUJ1, PUJ2
                uroven = int(inv[-1])
                # najdu pujcku v CisKarty
                karta_id = db.session.query(CisKarty.karta_id).filter_by(typk_id=typk_id, uroven=uroven).first()[0]
                # poradi karty urcim jak pocet karet ve hre + 1
                card_no = db.session.query(func.count(HryKarty.karta_hry_id)).scalar() + 1
                # urcim pocet tymu
                poc_tymu = db.session.query(Hry.poc_tymu).filter_by(hra_id=game.hra_id).first()[0]
                # najdu danou pujcku v tabulce CisKartyProTymy - zjistim cenu a naklady (u pujcky je prijem 0)
                kpt = db.session.query(CisKartyProTymy).filter_by(poc_tymu=poc_tymu, typk_id=typk_id, uroven=uroven).first()
                # vytvorim novou herni kartu a vlozim ji do databaze
                card = HryKarty(game.hra_id, karta_id, card_no, kpt.cena, kpt.naklady, kpt.prijem, game.team_id)
                db.session.add(card)
                db.session.commit()

                # aktualizuj majetek
                # majetek += kpt.cena
                # db.session.query(HryTymy).filter_by(tym_id=game.team_id).update({"majetek": majetek})
                update_majetek(game.team_id, kpt.cena, 'Pujcka')

                # zapsani do tabulky
                # new_record = InvesticeKolo(card.karta_hry_id, card.cis_karta.typk_id, game.team_id)
                new_record = HryKartyHistorie(card.karta_hry_id, game.round_no, game.team_id, datetime.now())
                db.session.add(new_record)
                game.loans_accepted[game.team_name][i] = True

                # log
                logprint("Tým '{}' si vzal půjčku {}M".format(game.team_name, kpt.cena))
        investmentCheck.append(game.team_name)
        for x in investmentCheck:
            print("Team ready: {}".format(x))
        db.session.commit()


    # zruseni investice
    elif type == 'cancel':
        print('Investice "{}" {} zrušena.'.format(game.team_name, game.investments))
        # investitions[session['team_name']] = []

        # ruseni investic
        tmp_inv = []
        tmp_acc = []
        for inv, acc in zip(game.investments[game.team_name], game.investments_accepted[game.team_name]):
            if acc:
                tmp_inv.append(inv)
                tmp_acc.append(acc)
        game.investments[game.team_name] = tmp_inv
        game.investments_accepted[game.team_name] = tmp_acc

        # ruseni pujcek
        tmp_loans = []
        tmp_acc = []
        for loan, acc in zip(game.loans[game.team_name], game.loans_accepted[game.team_name]):
            if acc:
                tmp_loans.append(loan)
                tmp_acc.append(acc)
        game.loans[game.team_name] = tmp_loans
        game.loans_accepted[game.team_name] = tmp_acc

    # oznaceni investice
    else:
        # uloz pujcku
        if 'PUJ' in type:
            game.loans[game.team_name].append(type)
            game.loans_accepted[game.team_name].append(False)
        elif len(game.investments[game.team_name]) < 2:
            game.investments[game.team_name].append(type)
            game.investments_accepted[game.team_name].append(False)
        else:
            error = 'Příliš mnoho investic.'

        # n_invs = len([x for x in game.investments[game.team_name] if 'PUJ' not in x])
        # # if len(game.investitions[game.team_name]) == 2:
        # if 'PUJ' not in type and n_invs == 2:
        #     error = 'Příliš mnoho investic.'
        # else:
        #     print('Investice "{}" do {}'.format(game.team_name, type))
        #     # investitions[session['team_name']].append(type)
        #     game.investments[game.team_name].append(type)
        #     game.invested[game.team_name].append(False)
    return render_game(error)


def get_number_of_investments(team_id, typk_id):
    number = 0
    cards = db.session.query(HryKarty).filter_by(hra_id=game.hra_id, tym_id=team_id)
    for c in cards:
        if c.cis_karta.typ_karta.typk_id == typk_id:
            number += 1
    return number


def get_graph_data():
    num_rounds = db.session.query(Hry.poc_kol).filter_by(hra_id=game.hra_id).first()[0]

    # pro kazdy tym prolistuj historii majetku
    team_ids = [t.tym_id for t in get_teams()]
    team_names = [db.session.query(CisTymy.nazev).filter_by(tym_id=team_id).first()[0] for team_id in team_ids]
    majetky = []
    for team_id in team_ids:
        majetek_tymu = [0 for i in range(num_rounds + 1)]
        prijmy = db.session.query(HryTymyPrijmy.kolo, HryTymyPrijmy.castka).filter_by(
            hra_id=game.hra_id, tym_id=team_id)
        for p in prijmy:
            majetek_tymu[p[0]] += p[1]
        accum = list(accumulate(majetek_tymu))
        # accum_thresh = [{0: 0, 1: x}.get(i < game.round_no + 1) for i, x in enumerate(accum)]
        # majetky.append(accum_thresh)
        majetky.append(accum)

    # create graph
    graph = pygal.Line(stroke_style={'width': 7}, dots_size=7)
    graph.title = 'Majetek firem'
    graph.x_labels = [str(i) for i in range(num_rounds + 1)]
    for name, data in zip(team_names, majetky):
        graph.add(name, data)
    graph_data = graph.render_data_uri()

    return graph_data


@app.route('/round/<string:action>')
def round_processor(action):
    global investmentCheck
    t = ""
    error = None
    teamsLocal = teamsRef.copy()
    # print('action: {}'.format(action))
    if action == 'pause':
        game.round_state = 'paused'
        logprint('KOLO {} - PAUZA'.format(game.round_no))

    elif action == 'play':
        if game.round_no < game.round_count:

            start_round()
            if game.role == 'admin':
                return redirect("/new_admin_tab")
            else:
                return redirect("/")
        else:
            logprint("ERROR Toto je poslední kolo")

    elif action == 'stop':
        for i in investmentCheck:
            if i in teamsLocal:
                teamsLocal.remove(i)
        if len(teamsLocal) == 0:
            investmentCheck = []
            stop_round()
            if game.role == 'admin':
                return redirect("/new_admin_tab")
            else:
                return redirect("/")
        else:
            print("ERROR")
            for i in teamsLocal:
                t += i
                t += ", "

    elif action == 'eval':
        eval_round()
        if game.role == 'admin':
            return redirect("/new_admin_tab")
        else:
            return redirect("/")
    
    return render_game(error, t[:-2])


@app.route('/loan_repayment/<int:id>')
def loan_repayment(id):
    # najit pujcky v tabulce hry_karty, ktere patri tymu game.team_id
    # splatit pujcku
    #   odecist finance
    #   odebrat kartu
    value = db.session.query(CisKarty.castka).join(HryKarty).filter(HryKarty.karta_hry_id == id).first()[0]
    # value = db.session.query(HryKarty.castka).filter_by(karta_hry_id=id).first()[0]
    update_majetek(game.team_id, value, 'Splaceni pujcky')
    logprint('Splátka půjčky s id: {}, částka = {}'.format(id, value))
    db.session.query(HryKarty).filter_by(karta_hry_id=id).delete()
    db.session.commit()

    return render_game(None)


@app.route('/mkt_message/', methods=['GET', 'POST'])
def mkt_message():
    error = None
    # form = MktMessageForm(request.form)

    title = request.form['title']
    body = request.form['body']

    # pokud jde o prvni zpravu v tomto kole, vytvor ji
    # v pripade, ze jiz v tomto kole byla nejaka zprava zadana, proved update
    # n_msgs = session.query(func.count(HryZpravy.zprava_id)).scalar()

    res = db.session.query(HryZpravy.zprava_id).filter_by(hra_id=game.hra_id, tym_id=game.team_id, kolo=game.round_no).first()
    if res is None:
        msg = HryZpravy(game.hra_id, game.team_id, game.round_no, title, body, None)
        db.session.add(msg)
    else:
        db.session.query(HryZpravy).filter_by(zprava_id=res[0]).update({"titulek": title, "zprava": body})
    db.session.commit()

    return render_game(error)


@app.route('/mkt_message_voting/', methods=['GET', 'POST'])
def mkt_message_voting():
    error = None
    autor_id = int(request.form['item'])
    zprava_id = db.session.query(HryZpravy.zprava_id).filter_by(hra_id=game.hra_id, tym_id=autor_id,
                                                                kolo=game.round_no).first()[0]
    voting = HryHlasovani(game.hra_id, game.team_id, 'MZ', autor_id, zprava_id, '', 1)
    db.session.add(voting)
    db.session.commit()

    logprint('Hlas dán týmu s ID={}'.format(autor_id))
    return render_game(error)


@app.route('/certification_charge/<int:team_id>')
def certification_charge(team_id):
    error = None
    # certification_charge = -20
    certification_charge = - db.session.query(Hry.cena_cert).filter_by(hra_id=game.hra_id).first()[0]
    update_majetek(team_id, certification_charge, 'Poplatek za pokus o certifikaci')
    prijem = HryTymyPrijmy(game.hra_id, game.round_no, team_id, certification_charge, 'Prihlaska k certifikaci.')
    db.session.add(prijem)
    db.session.commit()
    logprint("'{}' - strženo {} za přihlášku k certifikaci programu.".format(team_id2team_name(team_id),
                                                                             certification_charge))
    return render_game(error)


@app.route('/certification_reward/<int:team_id>')
def certification_reward(team_id):
    error = None
    # certification_reward = 50
    certification_reward = db.session.query(Hry.odm_cert).filter_by(hra_id=game.hra_id).first()[0]
    update_majetek(team_id, certification_reward, 'Zisk certifikace')
    prijem = HryTymyPrijmy(game.hra_id, game.round_no, team_id, certification_reward, 'Ziskani certifikace.')
    db.session.add(prijem)
    db.session.commit()
    logprint("'{}' - připsáno {} za získání certifikace.".format(team_id2team_name(team_id), certification_reward))
    return render_game(error)


@app.route('/vyrobek_state_changed/<int:team_id>')
def vyrobek_state_changed(team_id):
    error = None
    ma_vyrobek = db.session.query(HryTymy.ma_vyrobek).filter_by(hra_id=game.hra_id, tym_id=team_id).first()[0]
    ma_vyrobek = not ma_vyrobek
    db.session.query(HryTymy).filter_by(hra_id=game.hra_id, tym_id=team_id).update({"ma_vyrobek": ma_vyrobek})
    db.session.commit()
    logprint("'{}' - změněn stav 'ma_vyrobek' na {}".format(team_id, ma_vyrobek))

    return render_game(error)


@app.route('/nazev_state_changed/<int:team_id>')
def nazev_state_changed(team_id):
    error = None
    ma_nazev = db.session.query(HryTymy.ma_nazev).filter_by(hra_id=game.hra_id, tym_id=team_id).first()[0]
    ma_nazev = not ma_nazev
    db.session.query(HryTymy).filter_by(hra_id=game.hra_id, tym_id=team_id).update({"ma_nazev": ma_nazev})
    db.session.commit()
    logprint("'{}' - změněn stav 'ma_nazev' na {}".format(team_id, ma_nazev))

    return render_game(error)


@app.route('/logo_state_changed/<int:team_id>')
def logo_state_changed(team_id):
    error = None
    ma_logo = db.session.query(HryTymy.ma_logo).filter_by(hra_id=game.hra_id, tym_id=team_id).first()[0]
    ma_logo = not ma_logo
    db.session.query(HryTymy).filter_by(hra_id=game.hra_id, tym_id=team_id).update({"ma_logo": ma_logo})
    db.session.commit()
    logprint("'{}' - změněn stav 'ma_logo' na {}".format(team_id, ma_logo))

    return render_game(error)


@app.route('/special_payment/', methods=['POST'])
def special_payment():
    error = None
    form = SpecialPaymentForm(request.form)
    if form.validate_on_submit():
        team_id = request.form.get('select_team')
        amount = request.form['amount']
        desc = request.form['description']
        prijem = HryTymyPrijmy(game.hra_id, game.round_no, team_id, amount, desc)
        db.session.add(prijem)
        db.session.commit()
        logprint("Speciální platba pro '{}', částka = {}, popis = '{}'".format(team_id2team_name(team_id), amount, desc))

        return redirect(url_for('new_admin_tab'))
        # return redirect(url_for('render_game'))
    else:
        return render_game(error)

@app.route("/action/db/back", methods=["POST"])
def action_back():
    # SELECT * FROM nf_hry_karty JOIN nf_cis_karty on nf_hry_karty.karta_id=nf_cis_karty.karta_id;

    team = request.form['select_team']
    card_id = request.form['card']
    if 'add' in request.form:
        if team and card_id:
            card = db.session.query(HryKarty).join(CisKarty).filter(
                HryKarty.hra_id == game.hra_id, HryKarty.tym_id == None, CisKarty.typk_id == card_id). \
                order_by(HryKarty.karta_id).first()

            db.session.query(HryKarty).filter_by(karta_hry_id=card.karta_hry_id).update({"tym_id": team})

            new_record = HryKartyHistorie(card.karta_hry_id, game.round_no, team, datetime.now())
            db.session.add(new_record)

            db.session.commit()

    if 'delete' in request.form:
        if team and card_id:
            card = db.session.query(HryKarty).join(CisKarty).filter(
                HryKarty.hra_id == game.hra_id, HryKarty.tym_id == team, CisKarty.typk_id == card_id). \
                order_by(HryKarty.karta_id).first()

            db.session.query(HryKarty).filter_by(karta_hry_id=card.karta_hry_id).update({"tym_id": None})

            HryKartyHistorie.query.filter(HryKartyHistorie.tym_id == team,
                                          HryKartyHistorie.karta_hry_id == card.karta_hry_id).delete()

            db.session.commit()

    return redirect('/new_admin_tab/')




@app.route('/graph/', methods=['GET'])
def graph():
    if game.hra_id is not None:
        graph_data = get_graph_data()
    else:
        graph_data = None

    return render_template('graph.html', game=game, graph_data=graph_data)

@app.route("/dashboard/", methods=['GET', 'POST'])
def dashboard():
    error=None
    return render_game(error, control=False)

@app.route("/logo_select/", methods=['GET', 'POST'])
def logo_select():
    images = []
    for filename in os.listdir('../static/images/loga/'):
        if filename.endswith(".jpg"):
            images.append(os.path.join('../static/images/loga/', filename))
        else:
            continue
    return render_template('logos.html', images=images)