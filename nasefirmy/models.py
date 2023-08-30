#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# project/models.py


from nasefirmy import db
from datetime import datetime


# ----  firma / tym  ----
# class Company(db.Model):
#
#     __tablename__ = 'companies'
#
#     id = db.Column(db.Integer, primary_key=True, nullable=False)
#     name = db.Column(db.String, unique=True, nullable=False)
#     vyvoj = db.Column(db.Integer)
#     vyroba = db.Column(db.Integer)
#     obchod = db.Column(db.Integer)
#     servis = db.Column(db.Integer)
#     marketing = db.Column(db.Integer)
#
#     def __init__(self, name, vyvoj, vyroba, obchod, servis, marketing):
#         self.name = name
#         self.vyvoj = vyvoj
#         self.vyroba = vyroba
#         self.obchod = obchod
#         self.servis = servis
#         self.marketing = marketing
#
#     def __repr__(self):
#         return '<Company.{}'.format(self.name)


# ----  uzivatel  ----
# class User(db.Model):
#
#     __tablename__ = 'users'
#
#     id = db.Column(db.Integer, primary_key=True, nullable=False)
#     name = db.Column(db.String, unique=True, nullable=False)
#     password = db.Column(db.String, nullable=False)
#     role = db.Column(db.String, default='ROM')
#
#     def __init__(self, name=None, password=None, role=None):
#         self.name = name
#         self.password = password
#         self.role = role
#
#     def __repr__(self):
#         return '<User.{}>'.format(self.name)


# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------


# ----  typy karet ----
class CisTypyKaret(db.Model):
    __tablename__ = 'nf_cis_typy_karet'

    typk_id = db.Column(db.Integer, primary_key=True, nullable=False)
    kod = db.Column(db.String, nullable=False)
    # efekt: AH = akce hlavni, AV = akce vedlejsi, EH = efekt po celou hru, EK = efekt pro kolo
    efekt = db.Column(db.String, nullable=False)
    # losovat: 1 = tento typ karty se bude losovat, pocet vylosovanych ks dle tabulky nf_cis_karty_pro_tymy
    losovat = db.Column(db.Boolean, nullable=False)
    nazev = db.Column(db.String, nullable=False)
    popis = db.Column(db.String, nullable=False)
    ikona = db.Column(db.String, nullable=False)

    karta = db.relationship('CisKarty', backref='typ_karta')

    def __init__(self, typk_id, kod, efekt, losovat, nazev, popis, ikona):
        self.typk_id = typk_id
        self.kod = kod
        self.efekt = efekt
        self.losovat = losovat
        self.nazev = nazev
        self.popis = popis
        self.ikona = ikona

    def __repr__(self):
        return '<CisTypyKaret.{}>'.format(self.nazev)


# --------------------------------------------------------------------------------------------------------------------


# ----  cis_karty  ----
class CisKarty(db.Model):

    __tablename__ = 'nf_cis_karty'

    karta_id = db.Column(db.Integer, primary_key=True, nullable=False)
    typk_id = db.Column(db.Integer, db.ForeignKey('nf_cis_typy_karet.typk_id'))
    typ_karty = db.Column(db.String, nullable=False)
    uroven = db.Column(db.Integer, nullable=False)  # cenova uroven nakupu karty (1 - 3)
    nazev = db.Column(db.String, nullable=False)
    popis = db.Column(db.String, nullable=False)
    castka = db.Column(db.Integer, nullable=False)  # +/- zisk/ztrata
    symbol_obr = db.Column(db.String, nullable=False)
    ikony_oblasti = db.Column(db.String, nullable=True)
    cil = db.Column(db.Integer, nullable=False)  # zda pro 1 nebo se deli (99)
    vyhodnoceni = db.Column(db.String, nullable=True)  # vyhodnocujici SQL

    # hry_karta = db.relationship('HryKarty', back_populates='cis_karta')
    hry_karta = db.relationship('HryKarty', backref='cis_karta')

    def __init__(self, karta_id, typk_id, typ_karty, uroven, nazev, popis, castka, symbol_obr, ikony_oblasti, cil,
                 vyhodnoceni):
        self.karta_id = karta_id
        self.typk_id = typk_id
        self.typ_karty = typ_karty
        self.uroven = uroven
        self.nazev = nazev
        self.popis = popis
        self.castka = castka
        self.symbol_obr = symbol_obr
        self.ikony_oblasti = ikony_oblasti
        self.cil = cil
        self.vyhodnoceni = vyhodnoceni

    def __repr__(self):
        return '<CisKarty.{}>'.format(self.nazev)


# --------------------------------------------------------------------------------------------------------------------


# ----  cis_karty_pro_tymy  ----
class CisKartyProTymy(db.Model):

    __tablename__ = 'nf_cis_karty_pro_tymy'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    poc_tymu = db.Column(db.Integer, nullable=False)
    typk_id = db.Column(db.Integer, nullable=False)
    uroven = db.Column(db.Integer, nullable=False)
    pocet = db.Column(db.Integer, nullable=False)
    cena = db.Column(db.Integer, nullable=False)
    naklady = db.Column(db.Integer, nullable=False)
    prijem = db.Column(db.Integer, nullable=False)

    def __init__(self, poc_tymu, typk_id, uroven, pocet, cena, naklady, prijem):
        self.poc_tymu = poc_tymu
        self.typk_id = typk_id
        self.uroven = uroven
        self.pocet = pocet
        self.cena = cena
        self.naklady = naklady
        self.prijem = prijem

    def __repr__(self):
        return 'CisKartyProTymy: poc_tymu={}, typk_id={}, uroven={}, pocet={}'.format(self.poc_tymu, self.typk_id,
                                                                                      self.uroven, self.pocet)


# --------------------------------------------------------------------------------------------------------------------


# ----  misto hry  ----
class CisMista(db.Model):

    __tablename__ = 'nf_cis_mista'

    misto_id = db.Column(db.Integer, primary_key=True, nullable=False)
    nazev = db.Column(db.String, nullable=False)
    ulice = db.Column(db.String)
    obec = db.Column(db.String, nullable=False)
    psc = db.Column(db.Integer)
    souradnice = db.Column(db.String)

    def __init__(self, nazev, ulice, obec, psc, souradnice):
        self.nazev = nazev
        self.ulice = ulice
        self.obec = obec
        self.psc = psc
        self.souradnice = souradnice

    def __repr__(self):
        return '<CisMista.{}>'.format(self.nazev)


# --------------------------------------------------------------------------------------------------------------------


# ---- hra ----
class Hry(db.Model):

    __tablename__ = 'nf_hry'

    hra_id = db.Column(db.Integer, primary_key=True)
    nazev = db.Column(db.String, nullable=False)
    dat_hrani = db.Column(db.DateTime, default=datetime.now())
    misto_id = db.Column(db.Integer, db.ForeignKey('nf_cis_mista.misto_id'))
    popis = db.Column(db.String)  # popis hry
    klic = db.Column(db.String, nullable=False)  # klic hry
    majetek = db.Column(db.Integer, nullable=False, default=100)  # pocatecni majetek firmy
    karty_za_kolo = db.Column(db.Integer, nullable=False, default=2)  # pocet investic za kolo
    poc_tymu = db.Column(db.Integer, nullable=False)
    poc_kol = db.Column(db.Integer, nullable=False, default=10)
    akt_kolo = db.Column(db.Integer, nullable=False)
    stav_hry = db.Column(db.String, nullable=False)

    # pokud nema nazev/logo/zpravu, bude strzena tato castka z prijmu
    mkt_nazev = db.Column(db.Integer, nullable=False, default=0)
    mkt_logo = db.Column(db.Integer, nullable=False, default=0)
    mkt_zprava = db.Column(db.Integer, nullable=False, default=0)

    odm_zprava = db.Column(db.Integer, nullable=False, default=0)
    odm_zprava_hlas = db.Column(db.Integer, nullable=False, default=0)
    odm_robot1 = db.Column(db.Integer, nullable=False, default=0)
    odm_robot1_hlas = db.Column(db.Integer, nullable=False, default=0)
    odm_robot2 = db.Column(db.Integer, nullable=False, default=0)
    odm_robot2_hlas = db.Column(db.Integer, nullable=False, default=0)
    odm_robot3 = db.Column(db.Integer, nullable=False, default=0)
    odm_robot3_hlas = db.Column(db.Integer, nullable=False, default=0)

    cena_cert = db.Column(db.Integer, nullable=False, default=-20)  # cena za certifikaci
    odm_cert = db.Column(db.Integer, nullable=False, default=50)  # odmena pri splneni certifikace

    # rotace v kolech [S - start, vylosovani, cekani na spusteni odpoctu, A - aktivni, hraje se [, P = pauza, preruseni],
    # K = konec kola, vyhodnoceni MKT zprav,] R = hodnoceni robota na zaver, Z = zaver hry a zobrazeni vyhodnoceni

    def __init__(self, nazev, dat_hrani, misto_id, popis, klic, majetek, karty_za_kolo, poc_tymu, poc_kol, akt_kolo,
                 stav_hry, mkt_nazev, mkt_logo, mkt_zprava, odm_zprava, odm_zprava_hlas, odm_robot1, odm_robot1_hlas,
                 odm_robot2, odm_robot2_hlas, odm_robot3, odm_robot3_hlas, cena_cert, odm_cert):
        self.nazev = nazev
        self.dat_hrani = dat_hrani
        self.misto_id = misto_id
        self.popis = popis
        self.klic = klic
        self.majetek = majetek
        self.karty_za_kolo = karty_za_kolo
        self.poc_tymu = poc_tymu
        self.poc_kol = poc_kol
        self.akt_kolo = akt_kolo
        self.stav_hry = stav_hry

        self.mkt_nazev = mkt_nazev
        self.mkt_logo = mkt_logo
        self.mkt_zprava = mkt_zprava

        self.odm_zprava = odm_zprava
        self.odm_zprava_hlas = odm_zprava_hlas
        self.odm_robot1 = odm_robot1
        self.odm_robot1_hlas = odm_robot1_hlas
        self.odm_robot2 = odm_robot2
        self.odm_robot2_hlas = odm_robot2_hlas
        self.odm_robot3 = odm_robot3
        self.odm_robot3_hlas = odm_robot3_hlas

        self.cena_cert = cena_cert
        self.odm_cert = odm_cert


    def __repr__(self):
        return '<Hry.{}>'.format(self.nazev)


# --------------------------------------------------------------------------------------------------------------------


# ---- tymy ----
class CisTymy(db.Model):

    __tablename__ = 'nf_cis_tymy'

    tym_id = db.Column(db.Integer, primary_key=True, nullable=False)
    # tym_klic = db.Column(db.String, nullable=False)  # pro spravovani polozky v tabulce s pristupovym klicem tymu
    nazev = db.Column(db.String, nullable=False)
    dat_registrace = db.Column(db.Date, default=datetime.now())
    popis = db.Column(db.String, nullable=False)
    stav = db.Column(db.String, nullable=False)  # A = aktivni, N = neaktivni, X = zruseno

    hry_karta = db.relationship('HryKarty', backref='cis_tym')

    def __init__(self, nazev, dat_registrace, popis, stav):
        self.nazev = nazev
        self.dat_registrace = dat_registrace
        self.popis = popis
        self.stav = stav

    def __repr__(self):
        return '<CisTymy.{}>'.format(self.nazev)


# --------------------------------------------------------------------------------------------------------------------


#zaznam tymu v aktualni hre
class HryTymy(db.Model):

    __tablename__ = 'nf_hry_tymy'

    id = db.Column(db.Integer, primary_key=True)
    hra_id = db.Column(db.Integer, db.ForeignKey('nf_hry.hra_id'), nullable=False)
    tym_id = db.Column(db.Integer, db.ForeignKey('nf_cis_tymy.tym_id'), nullable=False)
    klic = db.Column(db.String, nullable=False)  # klic pro pripojeni ke hre (vygeneruje se a pote zaci zadaji)
    nazev_firmy = db.Column(db.String, nullable=False)
    logo = db.Column(db.String)
    majetek = db.Column(db.Integer, nullable=False)  # aktualni majetek tymu

    ma_vyrobek = db.Column(db.Boolean, nullable=False, default=False)
    ma_nazev = db.Column(db.Boolean, nullable=False, default=False)
    ma_logo = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, hra_id, tym_id, klic, nazev_firmy, logo, majetek, ma_vyrobek, ma_nazev, ma_logo):
        self.hra_id = hra_id
        self.tym_id = tym_id
        self.klic = klic
        self.nazev_firmy = nazev_firmy
        self.logo = logo
        self.majetek = majetek

        self.ma_vyrobek = ma_vyrobek
        self.ma_nazev = ma_nazev
        self.ma_logo = ma_logo

    def __repr__(self):
        return '<hra_id: {}, tym_id: {}>'.format(self.hra_id, self.tym_id)


# --------------------------------------------------------------------------------------------------------------------


class HryTymyHraci(db.Model):

    __tablename__ = 'nf_hry_tymy_hraci'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    hra_id = db.Column(db.Integer, db.ForeignKey('nf_hry.hra_id'),  nullable=False)
    tym_id = db.Column(db.Integer, db.ForeignKey('nf_cis_tymy.tym_id'), nullable=False)
    # role hrace(bude vypsano, nebo to bude pres tabulku a id
    # RED, OBD, MKT, VVJ, VRB, ROB = reditel + obchodnik v jednom (4 zaci v tymu),
    # ROM = reditel + obchodnik + marketing (3 zaci v tymu)
    # podle teto role se bude umoznovat pristup k jednotlivym funkcim
    role = db.Column(db.String, nullable=False)
    # lze zadat jmeno hrace, ktere se pak muze zobrazovat ve hre; mozna v budoucnu tabulka hracu a zde hrac_id
    jmeno = db.Column(db.String, nullable=False)

    def __init__(self, hra_id, tym_id, role, jmeno):
        self.hra_id = hra_id
        self.tym_id = tym_id
        self.role = role
        self.jmeno = jmeno

    def __repr__(self):
        return '<HryTymyHraci.{}'.format(self.id)


# --------------------------------------------------------------------------------------------------------------------


# ---- karty vylosovane pro hru  ----
# tabulka s prehledem karet vylosovanych pro hru na zaklade poctu tymu dle tabulky nf_cis_karty_pro_tymy
class HryKarty(db.Model):

    __tablename__ = 'nf_hry_karty'

    karta_hry_id = db.Column(db.Integer, primary_key=True, nullable=False)
    hra_id = db.Column(db.Integer, db.ForeignKey('nf_hry.hra_id'))
    karta_id = db.Column(db.Integer, db.ForeignKey('nf_cis_karty.karta_id'))
    # karta_id = db.Column(db.Integer, db.ForeignKey(CisKarty.karta_id))
    poradi = db.Column(db.Integer, nullable=False)  # poradi karty ve hre (dulezite pro nakup beznych karet)
    cena = db.Column(db.Integer, nullable=False)  # nakupni cena karty
    naklady = db.Column(db.Integer, nullable=False)  # poplatek za udrzbu karty
    prijem = db.Column(db.Integer, nullable=False)  # zisk z dane karty
    tym_id = db.Column(db.Integer, db.ForeignKey('nf_cis_tymy.tym_id'))

    def __init__(self, hra_id, karta_id, poradi, cena, naklady, prijem, tym_id):
        self.hra_id = hra_id
        self.karta_id = karta_id
        self.poradi = poradi
        self.cena = cena
        self.naklady = naklady
        self.prijem = prijem
        self.tym_id = tym_id

    def __repr__(self):
        return '<HryKarty.{}>'.format(self.karta_hry_id)


# --------------------------------------------------------------------------------------------------------------------


class HryKartyHistorie(db.Model):

    __tablename__ = 'nf_hry_karty_historie'

    zaznam_id = db.Column(db.Integer, primary_key=True, nullable=False)
    karta_hry_id = db.Column(db.Integer, db.ForeignKey('nf_hry_karty.karta_hry_id'), nullable=False)
    kolo = db.Column(db.Integer, nullable=False)
    tym_id = db.Column(db.Integer, db.ForeignKey('nf_cis_tymy.tym_id'), nullable=False)
    dat_ziskani = db.Column(db.DateTime,  default=datetime.now())

    def __init__(self, karta_hry_id, kolo, tym_id, dat_ziskani):
        self.karta_hry_id = karta_hry_id
        self.kolo = kolo
        self.tym_id = tym_id
        self.dat_ziskani = dat_ziskani

    def __repr__(self):
        return '<HryKartyHistorie.>'.format(self.karta_hry_id)


# --------------------------------------------------------------------------------------------------------------------


class HryZpravy(db.Model):

    __tablename__ = 'nf_hry_zpravy'

    zprava_id = db.Column(db.Integer, primary_key=True, nullable=False)
    hra_id = db.Column(db.Integer, db.ForeignKey('nf_hry.hra_id'))
    tym_id = db.Column(db.Integer, db.ForeignKey('nf_cis_tymy.tym_id'))
    kolo = db.Column(db.Integer, nullable=False)
    titulek = db.Column(db.String)
    zprava = db.Column(db.String)
    obrazek = db.Column(db.String)

    def __init__(self, hra_id, tym_id, kolo, titulek, zprava, obrazek):
        self.hra_id = hra_id
        self.tym_id = tym_id
        self.kolo = kolo
        self.titulek = titulek
        self.zprava = zprava
        self.obrazek = obrazek

    def __repr__(self):
        return "<tym_id:{}, zprava:'{}'>".format(self.tym_id, self.zprava)


# --------------------------------------------------------------------------------------------------------------------


class HryTymyPrijmy(db.Model):

    __tablename__ = 'nf_hry_tymy_prijmy'

    zaznam_id = db.Column(db.Integer, primary_key=True, nullable=False)
    hra_id = db.Column(db.Integer, db.ForeignKey('nf_hry.hra_id'))
    kolo = db.Column(db.Integer, nullable=False)
    tym_id = db.Column(db.Integer, db.ForeignKey('nf_cis_tymy.tym_id'))
    castka = db.Column(db.Integer, nullable=False, default=0)
    poznamka = db.Column(db.String)

    def __init__(self, hra_id, kolo, tym_id, castka, poznamka):
        self.hra_id = hra_id
        self.kolo = kolo
        self.tym_id = tym_id
        self.castka = castka
        self.poznamka = poznamka

    def __repr__(self):
        return '<tym_id:{}, kolo:{}, castka:{}, poznamka:{}>'.format(self.tym_id, self.kolo, self.castka, self.poznamka)


# --------------------------------------------------------------------------------------------------------------------


class HryHlasovani(db.Model):

    __tablename__ = 'nf_tmp_hry_hlasovani'

    hlasovani_id = db.Column(db.Integer, primary_key=True)
    hra_id = db.Column(db.Integer, db.ForeignKey('nf_hry.hra_id'))
    tym_id = db.Column(db.Integer, db.ForeignKey('nf_cis_tymy.tym_id'))  # hlasujici tym
    # rozliseni hlasovani: MZ = MKT zprava / R1 = skelet / R2 = maska / R3 =disky robota
    typ_hlasovani = db.Column(db.String, nullable=False)
    autor_id = db.Column(db.Integer, db.ForeignKey('nf_cis_tymy.tym_id'))  # autor hodnocene zpravy / robota
    zprava_id = db.Column(db.Integer, db.ForeignKey('nf_hry_zpravy.zprava_id'))  # id MKT zpravy, u robota NULL
    popis = db.Column(db.String)  # poznamka
    hlas = db.Column(db.Boolean, nullable=False, default=0)  # zda dane polozce pridelil tym hlas

    def __init__(self, hra_id, tym_id, typ_hlasovani, autor_id, zprava_id, popis, hlas):
        self.hra_id = hra_id
        self.tym_id = tym_id
        self.typ_hlasovani = typ_hlasovani
        self.autor_id = autor_id
        self.zprava_id = zprava_id
        self.popis = popis
        self.hlas = hlas

    def __repr__(self):
        return "<tym_id:{}, typ:{}, zprava:'{}'>".format(self.tym_id, self.typ_hlasovani, self.zprava_id)


# --------------------------------------------------------------------------------------------------------------------


# class InvesticeKolo(db.Model):
#
#     __tablename__ = 'nf_investice_kolo'
#
#     investice_id = db.Column(db.Integer, primary_key=True)
#     karta_hry_id = db.Column(db.Integer, db.ForeignKey('nf_hry_karty.karta_hry_id'))
#     typ_investice = db.Column(db.Integer, db.ForeignKey('nf_cis_karty.typk_id'))
#     tym_id = db.Column(db.Integer, db.ForeignKey('nf_cis_tymy.tym_id'))
#
#     def __init__(self, karta_hry_id, typ_investice, tym_id):
#         self.karta_hry_id = karta_hry_id
#         self.typ_investice = typ_investice
#         self.tym_id = tym_id
#
#     def __repr__(self):
#         return '<InvesticeKolo: karta_hry_id={}, tym_id={}, typ_investice={}'.\
#             format(self.karta_hry_id, self.tym_id, self.typ_investice)


# --------------------------------------------------------------------------------------------------------------------


class CisHryNastaveni(db.Model):

    __tablename__ = 'nf_cis_hry_nastaveni'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    majetek = db.Column(db.Integer, nullable=False, default=100)  # pocatecni majetek firmy
    karty_za_kolo = db.Column(db.Integer, nullable=False, default=2)  # obvykly pocet investic za kolo
    poc_kol = db.Column(db.Integer, nullable=False, default=10)  # obvykly pocet kol hry
    # soucast zisku z marketingu - firma ma nazev (nema-li -> odecist z prijmu z kazde karty MKT)
    mkt_nazev = db.Column(db.Integer, nullable=False, default=10)
    # soucast zisku z marketingu - firma ma logo (nema-li -> odecist z prijmu z kazde karty MKT)
    mkt_logo = db.Column(db.Integer, nullable=False, default=5)
    # soucast zisku z marketingu - firma napsala zpravu (nema-li -> odecist z prijmu z kazde karty MKT)
    mkt_zprava = db.Column(db.Integer, nullable=False, default=5)
    odm_zprava = db.Column(db.Integer, nullable=False, default=5)  # odmena za nejlepsi marketingovou zpravu
    odm_zprava_hlas = db.Column(db.Integer, nullable=False, default=1)  # odmena za hlas pro nejlepsi marketingovou zpravu
    odm_robot1 = db.Column(db.Integer, nullable=False, default=20)  # odmena za nejlepsi design robota - skelet
    odm_robot1_hlas = db.Column(db.Integer, nullable=False, default=5)  # odmena za hlas pro nejlepsi design robota - skelet
    odm_robot2 = db.Column(db.Integer, nullable=False, default=10)  # odmena za nejlepsi design robota - masku
    odm_robot2_hlas = db.Column(db.Integer, nullable=False, default=3)  # odmena za hlas pro nejlepsi design robota - masku
    odm_robot3 = db.Column(db.Integer, nullable=False, default=10)  # odmena za nejlepsi design robota - disky
    odm_robot3_hlas = db.Column(db.Integer, nullable=False, default=3)  # odmena za hlas pro nejlepsi design robota - disky
    # certifikace
    cena_cert = db.Column(db.Integer, nullable=False, default=-20)  # cena za certifikaci
    odm_cert = db.Column(db.Integer, nullable=False, default=50)  # odmena pri splneni certifikace

    def __init__(self):
        pass

    def __repr__(self):
        pass