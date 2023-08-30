# db_create.py


from nasefirmy import db, bcrypt, app
from nasefirmy.models import CisTypyKaret, CisMista, CisKartyProTymy, CisKarty  # User, Company
from flask import url_for
from collections import defaultdict

import os


def fill_db(db):
    # nf_cis_mista
    db.session.add(CisMista("1. ZŠ", "První 1", "Plzeň", "12345", "gps 1"))
    db.session.add(CisMista("2. ZŠ", "Druhá 2", "Písek", "23456", "gps 2"))
    db.session.add(CisMista("3. ZŠ", "Třetí 3", "Třeboň", "34567", "gps 3"))
    # /DUMMY----

    # nf_cis_typy_karet ----
    db.session.add(CisTypyKaret(1, "VVJ", "AH", False, "vývoj", "vývoj, věda, výzkum", "static/image/vyvoj.png"))
    # url_for('static', filename='image/vyvoj.png')))
    db.session.add(CisTypyKaret(2, "VRB", "AH", False, "výroba", "výroba", "static/image/vyroba.png"))
    # url_for('static', filename='image/vyroba.png')))
    db.session.add(CisTypyKaret(3, "OBD", "AH", False, "obchod", "obchod, distribuce", "static/image/obchod.png"))
    # url_for('static', filename='image/obchod.png')))
    db.session.add(CisTypyKaret(4, "SRV", "AH", False, "servis", "servis, služby", "static/image/servis.png"))
    # url_for('static', filename='image/servis.png')))
    db.session.add(CisTypyKaret(5, "MKT", "AH", False, "marketing", "marketing, propagace", "static/image/marketing.png"))
    # url_for('static', filename='image/marketing.png')))
    db.session.add(CisTypyKaret(6, "POJ", "AH", False, "pojištění", "pojištění proti negativnímu efektu", "static/image/iko_pojisteni.png"))
    # url_for('static', filename='image/iko_pojisteni.png')))
    db.session.add(CisTypyKaret(7, "EXP", "AH", False, "expert", "využití služeb experta", "static/image/iko_expert.png"))
    # url_for('static', filename='image/iko_expert.png')))
    db.session.add(CisTypyKaret(8, "PUJ", "AV", False, "půjčka", "půjčka", "static/image/iko_pujcka.png"))
    # url_for('static', filename='image/iko_pujcka.png')))
    db.session.add(CisTypyKaret(11, "VYZ", "EH", True, "výzva", "výzva, úkol na celou hru", "static/image/iko_ost-vyzva.png"))
    # url_for('static', filename='image/iko_ost-vyzva.png')))
    db.session.add(CisTypyKaret(12, "P&R", "EK", True, "P & R", "příležitost / riziko, po dobu jednoho kola", "static/image/iko_ost-par.png"))
    # url_for('static', filename='image/iko_ost-par.png')))
    db.session.add(CisTypyKaret(13, "HRZ", "EH", True, "hrozba", "hrozba postihu po celou hru", "static/image/iko_ost-hrozba.png"))
    # url_for('static', filename='image/iko_ost-hrozba.png')))
    # ----

    # nf_cis_karty: (karta_id, typk_id, uroven, nazev, popis, castka, symbol_obr, cil, vyhodnoceni)
    # slovnik vyhodnocujicich SQL --
    vyhodnoceni_SQL = defaultdict(str)
    # VYZVY
    vyhodnoceni_SQL[
        31] = "SELECT Min(H.tym_id) as tym_id, H.typk_id, M.kod, H.poc_karet FROM (SELECT HK2.hra_id, HK2.tym_id, COUNT(HK2.karta_hry_id) AS poc_karet, K.typk_id, K.nazev FROM nf_hry_karty HK2 INNER JOIN `nf_cis_karty`K ON HK2.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK2.hra_id = #hra_id# AND NOT HK2.tym_id IS NULL GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS H INNER JOIN (SELECT SK.hra_id, SK.typk_id, Max(SK.poc_karet) as max_poc_karet, SK.kod FROM (SELECT HK1.hra_id, K.typk_id, COUNT(HK1.karta_hry_id) AS poc_karet, HK1.tym_id, T.kod FROM nf_hry_karty HK1 INNER JOIN `nf_cis_karty`K ON HK1.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK1.hra_id = #hra_id# AND NOT HK1.tym_id IS NULL GROUP BY HK1.hra_id, K.typk_id, T.kod, HK1.tym_id) SK GROUP BY SK.kod) AS M ON H.hra_id = M.hra_id AND H.typk_id = M.typk_id AND H.poc_karet = M.max_poc_karet GROUP BY H.typk_id, M.kod HAVING Min(H.tym_id) = Max(H.tym_id) AND H.poc_karet >=2 AND M.kod = 'VVJ'"
    vyhodnoceni_SQL[
        32] = "SELECT Min(H.tym_id) as tym_id, H.typk_id, M.kod, H.poc_karet FROM (SELECT HK2.hra_id, HK2.tym_id, COUNT(HK2.karta_hry_id) AS poc_karet, K.typk_id, K.nazev FROM nf_hry_karty HK2 INNER JOIN `nf_cis_karty`K ON HK2.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK2.hra_id = #hra_id# AND NOT HK2.tym_id IS NULL GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS H INNER JOIN (SELECT SK.hra_id, SK.typk_id, Max(SK.poc_karet) as max_poc_karet, SK.kod FROM (SELECT HK1.hra_id, K.typk_id, COUNT(HK1.karta_hry_id) AS poc_karet, HK1.tym_id, T.kod FROM nf_hry_karty HK1 INNER JOIN `nf_cis_karty`K ON HK1.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK1.hra_id = #hra_id# AND NOT HK1.tym_id IS NULL GROUP BY HK1.hra_id, K.typk_id, T.kod, HK1.tym_id) SK GROUP BY SK.kod) AS M ON H.hra_id = M.hra_id AND H.typk_id = M.typk_id AND H.poc_karet = M.max_poc_karet GROUP BY H.typk_id, M.kod HAVING Min(H.tym_id) = Max(H.tym_id) AND H.poc_karet >=2 AND M.kod = 'VRB'"
    vyhodnoceni_SQL[
        33] = "SELECT Min(H.tym_id) as tym_id, H.typk_id, M.kod, H.poc_karet FROM (SELECT HK2.hra_id, HK2.tym_id, COUNT(HK2.karta_hry_id) AS poc_karet, K.typk_id, K.nazev FROM nf_hry_karty HK2 INNER JOIN `nf_cis_karty`K ON HK2.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK2.hra_id = #hra_id# AND NOT HK2.tym_id IS NULL GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS H INNER JOIN (SELECT SK.hra_id, SK.typk_id, Max(SK.poc_karet) as max_poc_karet, SK.kod FROM (SELECT HK1.hra_id, K.typk_id, COUNT(HK1.karta_hry_id) AS poc_karet, HK1.tym_id, T.kod FROM nf_hry_karty HK1 INNER JOIN `nf_cis_karty`K ON HK1.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK1.hra_id = #hra_id# AND NOT HK1.tym_id IS NULL GROUP BY HK1.hra_id, K.typk_id, T.kod, HK1.tym_id) SK GROUP BY SK.kod) AS M ON H.hra_id = M.hra_id AND H.typk_id = M.typk_id AND H.poc_karet = M.max_poc_karet GROUP BY H.typk_id, M.kod HAVING Min(H.tym_id) = Max(H.tym_id) AND H.poc_karet >=2 AND M.kod = 'OBD'"
    vyhodnoceni_SQL[
        35] = "SELECT Min(H.tym_id) as tym_id, H.typk_id, M.kod, H.poc_karet FROM (SELECT HK2.hra_id, HK2.tym_id, COUNT(HK2.karta_hry_id) AS poc_karet, K.typk_id, K.nazev FROM nf_hry_karty HK2 INNER JOIN `nf_cis_karty`K ON HK2.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK2.hra_id = #hra_id# AND NOT HK2.tym_id IS NULL GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS H INNER JOIN (SELECT SK.hra_id, SK.typk_id, Max(SK.poc_karet) as max_poc_karet, SK.kod FROM (SELECT HK1.hra_id, K.typk_id, COUNT(HK1.karta_hry_id) AS poc_karet, HK1.tym_id, T.kod FROM nf_hry_karty HK1 INNER JOIN `nf_cis_karty`K ON HK1.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK1.hra_id = #hra_id# AND NOT HK1.tym_id IS NULL GROUP BY HK1.hra_id, K.typk_id, T.kod, HK1.tym_id) SK GROUP BY SK.kod) AS M ON H.hra_id = M.hra_id AND H.typk_id = M.typk_id AND H.poc_karet = M.max_poc_karet GROUP BY H.typk_id, M.kod HAVING Min(H.tym_id) = Max(H.tym_id) AND H.poc_karet >=2 AND M.kod = 'SRV'"
    vyhodnoceni_SQL[
        36] = "SELECT Min(H.tym_id) as tym_id, H.typk_id, M.kod, H.poc_karet FROM (SELECT HK2.hra_id, HK2.tym_id, COUNT(HK2.karta_hry_id) AS poc_karet, K.typk_id, K.nazev FROM nf_hry_karty HK2 INNER JOIN `nf_cis_karty`K ON HK2.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK2.hra_id = #hra_id# AND NOT HK2.tym_id IS NULL GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS H INNER JOIN (SELECT SK.hra_id, SK.typk_id, Max(SK.poc_karet) as max_poc_karet, SK.kod FROM (SELECT HK1.hra_id, K.typk_id, COUNT(HK1.karta_hry_id) AS poc_karet, HK1.tym_id, T.kod FROM nf_hry_karty HK1 INNER JOIN `nf_cis_karty`K ON HK1.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK1.hra_id = #hra_id# AND NOT HK1.tym_id IS NULL GROUP BY HK1.hra_id, K.typk_id, T.kod, HK1.tym_id) SK GROUP BY SK.kod) AS M ON H.hra_id = M.hra_id AND H.typk_id = M.typk_id AND H.poc_karet = M.max_poc_karet GROUP BY H.typk_id, M.kod HAVING Min(H.tym_id) = Max(H.tym_id) AND H.poc_karet >=2 AND M.kod = 'MKT'"

    # P&R
    vyhodnoceni_SQL[
        50] = "SELECT * FROM (SELECT HK2.hra_id, HK2.tym_id, COUNT(HK2.karta_hry_id) AS poc_karet, K.typk_id, K.nazev FROM nf_hry_karty HK2 INNER JOIN `nf_cis_karty`K ON HK2.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK2.hra_id = #hra_id# AND NOT HK2.tym_id IS NULL GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS H INNER JOIN (SELECT SK.hra_id, SK.typk_id, Max(SK.poc_karet) as max_poc_karet, SK.kod FROM (SELECT HK1.hra_id, K.typk_id, COUNT(HK1.karta_hry_id) AS poc_karet, HK1.tym_id, T.kod FROM nf_hry_karty HK1 INNER JOIN `nf_cis_karty`K ON HK1.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK1.hra_id = #hra_id# AND NOT HK1.tym_id IS NULL GROUP BY HK1.hra_id, K.typk_id, T.kod, HK1.tym_id) SK GROUP BY SK.kod) AS M ON H.hra_id = M.hra_id AND H.typk_id = M.typk_id AND H.poc_karet = M.max_poc_karet AND M.kod = 'VVJ'"
    vyhodnoceni_SQL[
        52] = "SELECT * FROM (SELECT HK2.hra_id, HK2.tym_id, COUNT(HK2.karta_hry_id) AS poc_karet, K.typk_id, K.nazev FROM nf_hry_karty HK2 INNER JOIN `nf_cis_karty`K ON HK2.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK2.hra_id = #hra_id# AND NOT HK2.tym_id IS NULL GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS H INNER JOIN (SELECT SK.hra_id, SK.typk_id, Max(SK.poc_karet) as max_poc_karet, SK.kod FROM (SELECT HK1.hra_id, K.typk_id, COUNT(HK1.karta_hry_id) AS poc_karet, HK1.tym_id, T.kod FROM nf_hry_karty HK1 INNER JOIN `nf_cis_karty`K ON HK1.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK1.hra_id = #hra_id# AND NOT HK1.tym_id IS NULL GROUP BY HK1.hra_id, K.typk_id, T.kod, HK1.tym_id) SK GROUP BY SK.kod) AS M ON H.hra_id = M.hra_id AND H.typk_id = M.typk_id AND H.poc_karet = M.max_poc_karet AND M.kod = 'VRB'"
    vyhodnoceni_SQL[
        53] = "SELECT * FROM (SELECT HK2.hra_id, HK2.tym_id, COUNT(HK2.karta_hry_id) AS poc_karet, K.typk_id, K.nazev FROM nf_hry_karty HK2 INNER JOIN `nf_cis_karty`K ON HK2.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK2.hra_id = #hra_id# AND NOT HK2.tym_id IS NULL GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS H INNER JOIN (SELECT SK.hra_id, SK.typk_id, Max(SK.poc_karet) as max_poc_karet, SK.kod FROM (SELECT HK1.hra_id, K.typk_id, COUNT(HK1.karta_hry_id) AS poc_karet, HK1.tym_id, T.kod FROM nf_hry_karty HK1 INNER JOIN `nf_cis_karty`K ON HK1.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK1.hra_id = #hra_id# AND NOT HK1.tym_id IS NULL GROUP BY HK1.hra_id, K.typk_id, T.kod, HK1.tym_id) SK GROUP BY SK.kod) AS M ON H.hra_id = M.hra_id AND H.typk_id = M.typk_id AND H.poc_karet = M.max_poc_karet AND M.kod = 'OBD'"
    vyhodnoceni_SQL[
        56] = "SELECT * FROM (SELECT HK2.hra_id, HK2.tym_id, COUNT(HK2.karta_hry_id) AS poc_karet, K.typk_id, K.nazev FROM nf_hry_karty HK2 INNER JOIN `nf_cis_karty`K ON HK2.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK2.hra_id = #hra_id# AND NOT HK2.tym_id IS NULL GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS H INNER JOIN (SELECT SK.hra_id, SK.typk_id, Max(SK.poc_karet) as max_poc_karet, SK.kod FROM (SELECT HK1.hra_id, K.typk_id, COUNT(HK1.karta_hry_id) AS poc_karet, HK1.tym_id, T.kod FROM nf_hry_karty HK1 INNER JOIN `nf_cis_karty`K ON HK1.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK1.hra_id = #hra_id# AND NOT HK1.tym_id IS NULL GROUP BY HK1.hra_id, K.typk_id, T.kod, HK1.tym_id) SK GROUP BY SK.kod) AS M ON H.hra_id = M.hra_id AND H.typk_id = M.typk_id AND H.poc_karet = M.max_poc_karet AND M.kod = 'SRV'"
    vyhodnoceni_SQL[
        57] = "SELECT * FROM (SELECT HK2.hra_id, HK2.tym_id, COUNT(HK2.karta_hry_id) AS poc_karet, K.typk_id, K.nazev FROM nf_hry_karty HK2 INNER JOIN `nf_cis_karty`K ON HK2.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK2.hra_id = #hra_id# AND NOT HK2.tym_id IS NULL GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS H INNER JOIN (SELECT SK.hra_id, SK.typk_id, Max(SK.poc_karet) as max_poc_karet, SK.kod FROM (SELECT HK1.hra_id, K.typk_id, COUNT(HK1.karta_hry_id) AS poc_karet, HK1.tym_id, T.kod FROM nf_hry_karty HK1 INNER JOIN `nf_cis_karty`K ON HK1.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK1.hra_id = #hra_id# AND NOT HK1.tym_id IS NULL GROUP BY HK1.hra_id, K.typk_id, T.kod, HK1.tym_id) SK GROUP BY SK.kod) AS M ON H.hra_id = M.hra_id AND H.typk_id = M.typk_id AND H.poc_karet = M.max_poc_karet AND M.kod = 'MKT'"
    vyhodnoceni_SQL[
        58] = "SELECT S1.hra_id, S1.tym_id, S1.typk_id, S1.kod, S1.poc_karet FROM (SELECT HT.hra_id, HT.tym_id, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) AS poc_karet FROM (SELECT hra_id, tym_id, typk_id, kod FROM nf_hry_tymy, nf_cis_typy_karet WHERE hra_id = #hra_id# AND kod IN ('VVJ', 'VRB', 'OBD', 'SRV', 'MKT') GROUP BY hra_id, tym_id, typk_id) AS HT LEFT JOIN (SELECT hra_id, tym_id, typk_id, COUNT(karta_hry_id) as poc_karet FROM nf_hry_karty HK2 INNER JOIN nf_cis_karty K ON HK2.karta_id = K.karta_id GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS HK ON HT.hra_id = HK.hra_id AND HT.tym_id = HK.tym_id AND HT.typk_id = HK.typk_id) AS S1 INNER JOIN (SELECT HT.hra_id, Min(HT.tym_id) AS MinTID, Max(HT.tym_id) AS MaxTID, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) AS poc_karet FROM (SELECT hra_id, tym_id, typk_id, kod FROM nf_hry_tymy, nf_cis_typy_karet WHERE hra_id = #hra_id# AND kod IN ('VVJ', 'VRB', 'OBD', 'SRV', 'MKT') GROUP BY hra_id, tym_id, typk_id) AS HT LEFT JOIN (SELECT hra_id, tym_id, typk_id, COUNT(karta_hry_id) as poc_karet FROM nf_hry_karty HK2 INNER JOIN nf_cis_karty K ON HK2.karta_id = K.karta_id GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS HK ON HT.hra_id = HK.hra_id AND HT.tym_id = HK.tym_id AND HT.typk_id = HK.typk_id GROUP BY HT.hra_id, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) HAVING HT.kod = 'VVJ' LIMIT 1) AS S2 ON S1.hra_id = S2.hra_id AND S1.typk_id = S2.typk_id AND S1.poc_karet = S2.poc_karet"
    vyhodnoceni_SQL[
        59] = "SELECT S1.hra_id, S1.tym_id, S1.typk_id, S1.kod, S1.poc_karet FROM (SELECT HT.hra_id, HT.tym_id, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) AS poc_karet FROM (SELECT hra_id, tym_id, typk_id, kod FROM nf_hry_tymy, nf_cis_typy_karet WHERE hra_id = #hra_id# AND kod IN ('VVJ', 'VRB', 'OBD', 'SRV', 'MKT') GROUP BY hra_id, tym_id, typk_id) AS HT LEFT JOIN (SELECT hra_id, tym_id, typk_id, COUNT(karta_hry_id) as poc_karet FROM nf_hry_karty HK2 INNER JOIN nf_cis_karty K ON HK2.karta_id = K.karta_id GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS HK ON HT.hra_id = HK.hra_id AND HT.tym_id = HK.tym_id AND HT.typk_id = HK.typk_id) AS S1 INNER JOIN (SELECT HT.hra_id, Min(HT.tym_id) AS MinTID, Max(HT.tym_id) AS MaxTID, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) AS poc_karet FROM (SELECT hra_id, tym_id, typk_id, kod FROM nf_hry_tymy, nf_cis_typy_karet WHERE hra_id = #hra_id# AND kod IN ('VVJ', 'VRB', 'OBD', 'SRV', 'MKT') GROUP BY hra_id, tym_id, typk_id) AS HT LEFT JOIN (SELECT hra_id, tym_id, typk_id, COUNT(karta_hry_id) as poc_karet FROM nf_hry_karty HK2 INNER JOIN nf_cis_karty K ON HK2.karta_id = K.karta_id GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS HK ON HT.hra_id = HK.hra_id AND HT.tym_id = HK.tym_id AND HT.typk_id = HK.typk_id GROUP BY HT.hra_id, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) HAVING HT.kod = 'VRB' LIMIT 1) AS S2 ON S1.hra_id = S2.hra_id AND S1.typk_id = S2.typk_id AND S1.poc_karet = S2.poc_karet"
    vyhodnoceni_SQL[
        60] = "SELECT S1.hra_id, S1.tym_id, S1.typk_id, S1.kod, S1.poc_karet FROM (SELECT HT.hra_id, HT.tym_id, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) AS poc_karet FROM (SELECT hra_id, tym_id, typk_id, kod FROM nf_hry_tymy, nf_cis_typy_karet WHERE hra_id = #hra_id# AND kod IN ('VVJ', 'VRB', 'OBD', 'SRV', 'MKT') GROUP BY hra_id, tym_id, typk_id) AS HT LEFT JOIN (SELECT hra_id, tym_id, typk_id, COUNT(karta_hry_id) as poc_karet FROM nf_hry_karty HK2 INNER JOIN nf_cis_karty K ON HK2.karta_id = K.karta_id GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS HK ON HT.hra_id = HK.hra_id AND HT.tym_id = HK.tym_id AND HT.typk_id = HK.typk_id) AS S1 INNER JOIN (SELECT HT.hra_id, Min(HT.tym_id) AS MinTID, Max(HT.tym_id) AS MaxTID, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) AS poc_karet FROM (SELECT hra_id, tym_id, typk_id, kod FROM nf_hry_tymy, nf_cis_typy_karet WHERE hra_id = #hra_id# AND kod IN ('VVJ', 'VRB', 'OBD', 'SRV', 'MKT') GROUP BY hra_id, tym_id, typk_id) AS HT LEFT JOIN (SELECT hra_id, tym_id, typk_id, COUNT(karta_hry_id) as poc_karet FROM nf_hry_karty HK2 INNER JOIN nf_cis_karty K ON HK2.karta_id = K.karta_id GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS HK ON HT.hra_id = HK.hra_id AND HT.tym_id = HK.tym_id AND HT.typk_id = HK.typk_id GROUP BY HT.hra_id, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) HAVING HT.kod = 'OBD' LIMIT 1) AS S2 ON S1.hra_id = S2.hra_id AND S1.typk_id = S2.typk_id AND S1.poc_karet = S2.poc_karet"
    vyhodnoceni_SQL[
        61] = "SELECT S1.hra_id, S1.tym_id, S1.typk_id, S1.kod, S1.poc_karet FROM (SELECT HT.hra_id, HT.tym_id, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) AS poc_karet FROM (SELECT hra_id, tym_id, typk_id, kod FROM nf_hry_tymy, nf_cis_typy_karet WHERE hra_id = #hra_id# AND kod IN ('VVJ', 'VRB', 'OBD', 'SRV', 'MKT') GROUP BY hra_id, tym_id, typk_id) AS HT LEFT JOIN (SELECT hra_id, tym_id, typk_id, COUNT(karta_hry_id) as poc_karet FROM nf_hry_karty HK2 INNER JOIN nf_cis_karty K ON HK2.karta_id = K.karta_id GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS HK ON HT.hra_id = HK.hra_id AND HT.tym_id = HK.tym_id AND HT.typk_id = HK.typk_id) AS S1 INNER JOIN (SELECT HT.hra_id, Min(HT.tym_id) AS MinTID, Max(HT.tym_id) AS MaxTID, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) AS poc_karet FROM (SELECT hra_id, tym_id, typk_id, kod FROM nf_hry_tymy, nf_cis_typy_karet WHERE hra_id = #hra_id# AND kod IN ('VVJ', 'VRB', 'OBD', 'SRV', 'MKT') GROUP BY hra_id, tym_id, typk_id) AS HT LEFT JOIN (SELECT hra_id, tym_id, typk_id, COUNT(karta_hry_id) as poc_karet FROM nf_hry_karty HK2 INNER JOIN nf_cis_karty K ON HK2.karta_id = K.karta_id GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS HK ON HT.hra_id = HK.hra_id AND HT.tym_id = HK.tym_id AND HT.typk_id = HK.typk_id GROUP BY HT.hra_id, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) HAVING HT.kod = 'SRV' LIMIT 1) AS S2 ON S1.hra_id = S2.hra_id AND S1.typk_id = S2.typk_id AND S1.poc_karet = S2.poc_karet"
    vyhodnoceni_SQL[
        62] = "SELECT S1.hra_id, S1.tym_id, S1.typk_id, S1.kod, S1.poc_karet FROM (SELECT HT.hra_id, HT.tym_id, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) AS poc_karet FROM (SELECT hra_id, tym_id, typk_id, kod FROM nf_hry_tymy, nf_cis_typy_karet WHERE hra_id = #hra_id# AND kod IN ('VVJ', 'VRB', 'OBD', 'SRV', 'MKT') GROUP BY hra_id, tym_id, typk_id) AS HT LEFT JOIN (SELECT hra_id, tym_id, typk_id, COUNT(karta_hry_id) as poc_karet FROM nf_hry_karty HK2 INNER JOIN nf_cis_karty K ON HK2.karta_id = K.karta_id GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS HK ON HT.hra_id = HK.hra_id AND HT.tym_id = HK.tym_id AND HT.typk_id = HK.typk_id) AS S1 INNER JOIN (SELECT HT.hra_id, Min(HT.tym_id) AS MinTID, Max(HT.tym_id) AS MaxTID, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) AS poc_karet FROM (SELECT hra_id, tym_id, typk_id, kod FROM nf_hry_tymy, nf_cis_typy_karet WHERE hra_id = #hra_id# AND kod IN ('VVJ', 'VRB', 'OBD', 'SRV', 'MKT') GROUP BY hra_id, tym_id, typk_id) AS HT LEFT JOIN (SELECT hra_id, tym_id, typk_id, COUNT(karta_hry_id) as poc_karet FROM nf_hry_karty HK2 INNER JOIN nf_cis_karty K ON HK2.karta_id = K.karta_id GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS HK ON HT.hra_id = HK.hra_id AND HT.tym_id = HK.tym_id AND HT.typk_id = HK.typk_id GROUP BY HT.hra_id, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) HAVING HT.kod = 'MKT' LIMIT 1) AS S2 ON S1.hra_id = S2.hra_id AND S1.typk_id = S2.typk_id AND S1.poc_karet = S2.poc_karet"

    # HROZBY
    vyhodnoceni_SQL[
        70] = "SELECT SX.hra_id, SX.MinTID, SX.MaxTID, SX.typk_id, SX.kod, SX.poc_karet FROM (SELECT HT.hra_id, Min(HT.tym_id) AS MinTID, Max(HT.tym_id) AS MaxTID, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) AS poc_karet FROM (SELECT hra_id, tym_id, typk_id, kod FROM nf_hry_tymy, nf_cis_typy_karet WHERE hra_id = #hra_id# AND kod IN ('VVJ', 'VRB', 'OBD', 'SRV', 'MKT') GROUP BY hra_id, tym_id, typk_id) AS HT LEFT JOIN (SELECT hra_id, tym_id, typk_id, COUNT(karta_hry_id) as poc_karet FROM nf_hry_karty HK2 INNER JOIN nf_cis_karty K ON HK2.karta_id = K.karta_id GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS HK ON HT.hra_id = HK.hra_id AND HT.tym_id = HK.tym_id AND HT.typk_id = HK.typk_id GROUP BY HT.hra_id, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) HAVING HT.kod = 'SRV' LIMIT 1) AS SX WHERE SX.MinTID = SX.MaxTID"
    vyhodnoceni_SQL[
        71] = "SELECT SX.hra_id, SX.MinTID, SX.MaxTID, SX.typk_id, SX.kod, SX.poc_karet FROM (SELECT HT.hra_id, Min(HT.tym_id) AS MinTID, Max(HT.tym_id) AS MaxTID, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) AS poc_karet FROM (SELECT hra_id, tym_id, typk_id, kod FROM nf_hry_tymy, nf_cis_typy_karet WHERE hra_id = #hra_id# AND kod IN ('VVJ', 'VRB', 'OBD', 'SRV', 'MKT') GROUP BY hra_id, tym_id, typk_id) AS HT LEFT JOIN (SELECT hra_id, tym_id, typk_id, COUNT(karta_hry_id) as poc_karet FROM nf_hry_karty HK2 INNER JOIN nf_cis_karty K ON HK2.karta_id = K.karta_id GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS HK ON HT.hra_id = HK.hra_id AND HT.tym_id = HK.tym_id AND HT.typk_id = HK.typk_id GROUP BY HT.hra_id, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) HAVING HT.kod = 'MKT' LIMIT 1) AS SX WHERE SX.MinTID = SX.MaxTID"
    vyhodnoceni_SQL[
        74] = "SELECT SX.hra_id, SX.MinTID, SX.MaxTID, SX.typk_id, SX.kod, SX.poc_karet FROM (SELECT HT.hra_id, Min(HT.tym_id) AS MinTID, Max(HT.tym_id) AS MaxTID, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) AS poc_karet FROM (SELECT hra_id, tym_id, typk_id, kod FROM nf_hry_tymy, nf_cis_typy_karet WHERE hra_id = #hra_id# AND kod IN ('VVJ', 'VRB', 'OBD', 'SRV', 'MKT') GROUP BY hra_id, tym_id, typk_id) AS HT LEFT JOIN (SELECT hra_id, tym_id, typk_id, COUNT(karta_hry_id) as poc_karet FROM nf_hry_karty HK2 INNER JOIN nf_cis_karty K ON HK2.karta_id = K.karta_id GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS HK ON HT.hra_id = HK.hra_id AND HT.tym_id = HK.tym_id AND HT.typk_id = HK.typk_id GROUP BY HT.hra_id, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) HAVING HT.kod = 'VVJ' LIMIT 1) AS SX WHERE SX.MinTID = SX.MaxTID"
    vyhodnoceni_SQL[
        75] = "SELECT SX.hra_id, SX.MinTID, SX.MaxTID, SX.typk_id, SX.kod, SX.poc_karet FROM (SELECT HT.hra_id, Min(HT.tym_id) AS MinTID, Max(HT.tym_id) AS MaxTID, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) AS poc_karet FROM (SELECT hra_id, tym_id, typk_id, kod FROM nf_hry_tymy, nf_cis_typy_karet WHERE hra_id = #hra_id# AND kod IN ('VVJ', 'VRB', 'OBD', 'SRV', 'MKT') GROUP BY hra_id, tym_id, typk_id) AS HT LEFT JOIN (SELECT hra_id, tym_id, typk_id, COUNT(karta_hry_id) as poc_karet FROM nf_hry_karty HK2 INNER JOIN nf_cis_karty K ON HK2.karta_id = K.karta_id GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS HK ON HT.hra_id = HK.hra_id AND HT.tym_id = HK.tym_id AND HT.typk_id = HK.typk_id GROUP BY HT.hra_id, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) HAVING HT.kod = 'VRB' LIMIT 1) AS SX WHERE SX.MinTID = SX.MaxTID"
    vyhodnoceni_SQL[
        76] = "SELECT SX.hra_id, SX.MinTID, SX.MaxTID, SX.typk_id, SX.kod, SX.poc_karet FROM (SELECT HT.hra_id, Min(HT.tym_id) AS MinTID, Max(HT.tym_id) AS MaxTID, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) AS poc_karet FROM (SELECT hra_id, tym_id, typk_id, kod FROM nf_hry_tymy, nf_cis_typy_karet WHERE hra_id = #hra_id# AND kod IN ('VVJ', 'VRB', 'OBD', 'SRV', 'MKT') GROUP BY hra_id, tym_id, typk_id) AS HT LEFT JOIN (SELECT hra_id, tym_id, typk_id, COUNT(karta_hry_id) as poc_karet FROM nf_hry_karty HK2 INNER JOIN nf_cis_karty K ON HK2.karta_id = K.karta_id GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS HK ON HT.hra_id = HK.hra_id AND HT.tym_id = HK.tym_id AND HT.typk_id = HK.typk_id GROUP BY HT.hra_id, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) HAVING HT.kod = 'OBD' LIMIT 1) AS SX WHERE SX.MinTID = SX.MaxTID"
    # --
    # -- karty akci
    db.session.add(CisKarty(1, 1, 1, 'vývoj', 'vývoj, věda, výzkum', 15, 'sym_01_VVJ-01.png', 0, ''))
    db.session.add(CisKarty(2, 1, 2, 'vývoj', 'vývoj, věda, výzkum', 30, 'sym_02_VVJ-02.png', 0, ''))
    db.session.add(CisKarty(3, 1, 3, 'vývoj', 'vývoj, věda, výzkum', 45, 'sym_03_VVJ-03.png', 0, ''))
    db.session.add(CisKarty(4, 2, 1, 'výroba', 'výroba', 12, 'sym_04_VRB-04.png', 0, ''))
    db.session.add(CisKarty(5, 2, 2, 'výroba', 'výroba', 15, 'sym_05_VRB-05.png', 0, ''))
    db.session.add(CisKarty(6, 2, 3, 'výroba', 'výroba', 20, 'sym_06_VRB-06.png', 0, ''))
    db.session.add(CisKarty(7, 3, 1, 'obchod', 'obchod, distribuce', 12, 'sym_07_OBD-07.png', 0, ''))
    db.session.add(CisKarty(8, 3, 2, 'obchod', 'obchod, distribuce', 15, 'sym_08_OBD-08.png', 0, ''))
    db.session.add(CisKarty(9, 3, 3, 'obchod', 'obchod, distribuce', 20, 'sym_09_OBD-09.png', 0, ''))
    db.session.add(CisKarty(10, 4, 1, 'servis', 'servis, služby', 15, 'sym_10_SRV-10.png', 0, ''))
    db.session.add(CisKarty(11, 4, 2, 'servis', 'servis, služby', 20, 'sym_11_SRV-11.png', 0, ''))
    db.session.add(CisKarty(12, 4, 3, 'servis', 'servis, služby', 30, 'sym_12_SRV-12.png', 0, ''))
    db.session.add(CisKarty(13, 5, 1, 'marketing', 'marketing, propagace', 15, 'sym_13_MKT-13.png', 0, ''))
    db.session.add(CisKarty(14, 5, 2, 'marketing', 'marketing, propagace', 20, 'sym_14_MKT-14.png', 0, ''))
    db.session.add(CisKarty(15, 5, 3, 'marketing', 'marketing, propagace', 30, 'sym_15_MKT-15.png', 0, ''))
    db.session.add(CisKarty(16, 6, 1, 'pojištění', 'pojištění proti negativnímu efektu', 0, 'sym_16_POJ-16.png', 0, ''))
    db.session.add(CisKarty(17, 7, 1, 'expert', 'využití služeb experta', 0, 'sym_17_EXP-17.png', 0, ''))
    # db.session.add(CisKarty(18, 8, 1, 'půjčka', 'půjčka', 0, 'sym_18_PUJ-18.png', 0, ''))
    db.session.add(CisKarty(18, 8, 1, 'půjčka', 'malá půjčka', -20, 'sym_18_PUJ-18.png', 0, ''))
    db.session.add(CisKarty(19, 8, 2, 'půjčka', 'velká půjčka', -40, 'sym_18_PUJ-18.png', 0, ''))

    # -- vyzvy
    db.session.add(
        CisKarty(31, 11, 1, 'Nejlepší vývojový tým', 'Nejvíce investic do vývoje, min. 2', 30, 'sym_31_VYZ-31.png', 1,
                 ''))
    db.session.add(
        CisKarty(32, 11, 1, 'Tahoun výroby', 'Nejvíce investic do výroby, min. 2', 30, 'sym_32_VYZ-32.png', 1, ''))
    db.session.add(
        CisKarty(33, 11, 1, 'Nejlepší obchodník', 'Nejvíce investic do obchodu, min. 2', 30, 'sym_33_VYZ-33.png', 1,
                 ''))
    db.session.add(
        CisKarty(34, 11, 1, 'Nejlepší dodavatel', 'Nejvíce dvojic výroba + obchod, min. 2', 30, 'sym_34_VYZ-34.png', 1,
                 ''))
    db.session.add(
        CisKarty(35, 11, 1, 'Nejkvalitnější servis', 'Nejvíce investic do servisu, min. 2', 30, 'sym_35_VYZ-35.png', 1,
                 ''))
    db.session.add(CisKarty(36, 11, 1, 'Nejlepší kampaň marketingu', 'Nejvíce investic do marketingu, min. 2', 30,
                            'sym_36_VYZ-36.png', 1, ''))
    db.session.add(CisKarty(37, 11, 1, 'Prosperující firma', 'Nejvyšší celkový příjem', 30, 'sym_37_VYZ-37.png', 1, ''))
    db.session.add(
        CisKarty(38, 11, 1, 'Nejlepší investiční krok', 'Nejvyšší kvartálový příjem', 30, 'sym_38_VYZ-38.png', 1, ''))
    db.session.add(
        CisKarty(39, 11, 1, 'Kvalitní zázemí', 'Nejvíce investic do vývoje + servisu + marketingu (min. 4)', 30,
                 'sym_39_VYZ-39.png', 1, ''))
    db.session.add(CisKarty(40, 11, 1, 'Zacíleno na zákazníka', 'Nejvíce investic do vývoje + marketingu (min. 4)', 30,
                            'sym_40_VYZ-40.png', 1, ''))
    db.session.add(CisKarty(41, 11, 1, 'Důraz na inovace', 'Nejvíce investic do vývoje + servisu (min. 4)', 30,
                            'sym_41_VYZ-41.png', 1, ''))
    db.session.add(CisKarty(42, 11, 1, 'Propagace služeb', 'Nejvíce investic do servisu + marketingu (min. 4)', 30,
                            'sym_42_VYZ-42.png', 1, ''))
    # -- P&R
    db.session.add(
        CisKarty(50, 12, 1, 'Inovativní přístup', 'Nejvíce investic do vývoje', 30, 'sym_50_P&R-50.png', 99, ''))
    db.session.add(
        CisKarty(51, 12, 1, 'Popularizace vývoje', 'Nejvíce dvojic vývoj + marketing (při shodě rozhoduje marketing)',
                 30, 'sym_51_P&R-51.png', 99, ''))
    db.session.add(
        CisKarty(52, 12, 1, 'Podpora výrobců', 'Nejvíce investic do výroby', 30, 'sym_52_P&R-52.png', 99, ''))
    db.session.add(
        CisKarty(53, 12, 1, 'Oživení obchodu', 'Nejvíce investic do obchodu', 30, 'sym_53_P&R-53.png', 99, ''))
    db.session.add(
        CisKarty(54, 12, 1, 'Kvalitní obchodní model', 'Nejvíce dvojic výroba + obchod (při shodě rozhoduje výroba)',
                 30, 'sym_54_P&R-54.png', 99, ''))
    db.session.add(CisKarty(55, 12, 1, 'Nové obchodní příležitosti',
                            'Nejvíce dvojic výroba + obchod (při shodě rozhoduje marketing)', 30, 'sym_55_P&R-55.png',
                            99, ''))
    db.session.add(
        CisKarty(56, 12, 1, 'Kvalitní zákaznická podpora', 'Nejvíce investic do servisu', 30, 'sym_56_P&R-56.png', 99,
                 ''))
    db.session.add(
        CisKarty(57, 12, 1, 'Univerzální prodejci', 'Nejvíce investic do marketingu', 30, 'sym_57_P&R-57.png', 99, ''))
    db.session.add(
        CisKarty(58, 12, 1, 'Nedostatek nápadů', 'Nejméně investic do vývoje', -30, 'sym_58_P&R-58.png', 99, ''))
    db.session.add(
        CisKarty(59, 12, 1, 'Nízká kvalita výroby', 'Nejméně investic do výroby', -30, 'sym_59_P&R-59.png', 99, ''))
    db.session.add(
        CisKarty(60, 12, 1, 'Podomní prodejci', 'Nejméně investic do obchodu', -30, 'sym_60_P&R-60.png', 99, ''))
    db.session.add(
        CisKarty(61, 12, 1, 'Nefunkční zákaznická linka', 'Nejméně investic do servisu', -30, 'sym_61_P&R-61.png', 99,
                 ''))
    db.session.add(
        CisKarty(62, 12, 1, 'Zmařená kampaň', 'Nejméně investic do marketingu', -30, 'sym_62_P&R-62.png', 99, ''))
    db.session.add(
        CisKarty(63, 12, 1, 'Nevyužité investice', 'Nejnižší investice v tomto kvartálu', -30, 'sym_63_P&R-63.png', 99,
                 ''))
    db.session.add(
        CisKarty(64, 12, 1, 'Příprava úspor', 'Nejnižší investice v tomto kvartálu', 30, 'sym_64_P&R-64.png', 99, ''))
    # -- Hrozby
    db.session.add(
        CisKarty(70, 13, 1, 'Nízká úroveň služeb zákazníkům', 'Nejméně investic do servisu', -20, 'sym_70_HRZ-70.png',
                 1, ''))
    db.session.add(
        CisKarty(71, 13, 1, 'Nízká úroveň marketingu', 'Nejméně investic do marketingu', -20, 'sym_71_HRZ-71.png', 1,
                 ''))
    db.session.add(CisKarty(72, 13, 1, 'Firma bez zázemí', 'Nejméně investic do vývoje + servisu + marketingu', -20,
                            'sym_72_HRZ-72.png', 1, ''))
    db.session.add(CisKarty(73, 13, 1, 'Nevyváženost investic', 'Největší počet oblastí s nejméně investicemi', -20,
                            'sym_73_HRZ-73.png', 1, ''))
    db.session.add(
        CisKarty(74, 13, 1, 'Nízká efektivita vývoje', 'Nejméně investic do vývoje', -20, 'sym_74_HRZ-74.png', 1, ''))
    db.session.add(
        CisKarty(75, 13, 1, 'Slabá optimalizace výroby', 'Nejméně investic do výroby', -20, 'sym_75_HRZ-75.png', 1, ''))
    db.session.add(
        CisKarty(76, 13, 1, 'Nízká úroveň obchodu', 'Nejméně investic do obchodu', -20, 'sym_76_HRZ-76.png', 1, ''))
    db.session.add(CisKarty(77, 13, 1, 'Nekoordinovaná výroba a obchod', 'Nejmenší počet dvojic výroba + obchod', -20,
                            'sym_77_HRZ-77.png', 1, ''))
    # doplneni vyhodnoceni
    for row in CisKarty.query:
        row.vyhodnoceni = vyhodnoceni_SQL[row.karta_id]

    # nf_cis_karty_pro_tymy: (poc_tymu, typk_id, uroven, pocet, cena, naklady, prijem)
    # pocet = 2
    db.session.add(CisKartyProTymy(2, 1, 1, 2, 15, 6, 30))
    db.session.add(CisKartyProTymy(2, 1, 2, 3, 30, 6, 30))
    db.session.add(CisKartyProTymy(2, 1, 3, 1, 45, 6, 30))
    db.session.add(CisKartyProTymy(2, 2, 1, 7, 12, 3, 15))
    db.session.add(CisKartyProTymy(2, 2, 2, 7, 15, 3, 15))
    db.session.add(CisKartyProTymy(2, 3, 1, 7, 12, 3, 15))
    db.session.add(CisKartyProTymy(2, 3, 2, 7, 15, 3, 15))
    db.session.add(CisKartyProTymy(2, 4, 1, 4, 15, 3, 20))
    db.session.add(CisKartyProTymy(2, 4, 2, 3, 20, 3, 20))
    db.session.add(CisKartyProTymy(2, 4, 3, 1, 30, 3, 20))
    db.session.add(CisKartyProTymy(2, 5, 1, 4, 15, 3, 20))
    db.session.add(CisKartyProTymy(2, 5, 2, 3, 20, 3, 20))
    db.session.add(CisKartyProTymy(2, 5, 3, 1, 30, 3, 20))
    # -
    db.session.add(CisKartyProTymy(2, 6, 1, 18, 0, 0, 0))
    db.session.add(CisKartyProTymy(2, 7, 1, 18, 0, 0, 0))
    db.session.add(CisKartyProTymy(2, 8, 1, 99, 20, 2, 0))
    db.session.add(CisKartyProTymy(2, 8, 2, 99, 40, 3, 0))
    db.session.add(CisKartyProTymy(2, 11, 1, 3, 0, 0, 0))
    db.session.add(CisKartyProTymy(2, 12, 1, 99, 0, 0, 0))
    # db.session.add(CisKartyProTymy(2, 12, 1, 1, 0, 0, 0))
    db.session.add(CisKartyProTymy(2, 13, 1, 2, 0, 0, 0))
    # pocet = 3
    db.session.add(CisKartyProTymy(3, 1, 1, 3, 15, 6, 30))
    db.session.add(CisKartyProTymy(3, 1, 2, 3, 30, 6, 30))
    db.session.add(CisKartyProTymy(3, 1, 3, 2, 45, 6, 30))
    db.session.add(CisKartyProTymy(3, 2, 1, 12, 12, 3, 15))
    db.session.add(CisKartyProTymy(3, 2, 2, 9, 15, 3, 15))
    db.session.add(CisKartyProTymy(3, 3, 1, 12, 12, 3, 15))
    db.session.add(CisKartyProTymy(3, 3, 2, 9, 15, 3, 15))
    db.session.add(CisKartyProTymy(3, 4, 1, 6, 15, 3, 20))
    db.session.add(CisKartyProTymy(3, 4, 2, 3, 20, 3, 20))
    db.session.add(CisKartyProTymy(3, 4, 3, 2, 30, 3, 20))
    db.session.add(CisKartyProTymy(3, 5, 1, 6, 15, 3, 20))
    db.session.add(CisKartyProTymy(3, 5, 2, 3, 20, 3, 20))
    db.session.add(CisKartyProTymy(3, 5, 3, 2, 30, 3, 20))
    # -
    db.session.add(CisKartyProTymy(3, 6, 1, 18, 0, 0, 0))
    db.session.add(CisKartyProTymy(3, 7, 1, 18, 0, 0, 0))
    db.session.add(CisKartyProTymy(3, 8, 1, 99, 20, 2, 0))
    db.session.add(CisKartyProTymy(3, 8, 2, 99, 40, 3, 0))
    db.session.add(CisKartyProTymy(3, 11, 1, 4, 0, 0, 0))
    db.session.add(CisKartyProTymy(3, 12, 1, 99, 0, 0, 0))
    # db.session.add(CisKartyProTymy(3, 12, 1, -1, 0, 0, 0))
    db.session.add(CisKartyProTymy(3, 13, 1, 2, 0, 0, 0))
    # pocet = 4
    db.session.add(CisKartyProTymy(4, 1, 1, 4, 15, 6, 30))
    db.session.add(CisKartyProTymy(4, 1, 2, 4, 30, 6, 30))
    db.session.add(CisKartyProTymy(4, 1, 3, 2, 45, 6, 30))
    db.session.add(CisKartyProTymy(4, 2, 1, 16, 12, 3, 15))
    db.session.add(CisKartyProTymy(4, 2, 2, 12, 15, 3, 15))
    db.session.add(CisKartyProTymy(4, 3, 1, 16, 12, 3, 15))
    db.session.add(CisKartyProTymy(4, 3, 2, 12, 15, 3, 15))
    db.session.add(CisKartyProTymy(4, 4, 1, 8, 15, 3, 20))
    db.session.add(CisKartyProTymy(4, 4, 2, 4, 20, 3, 20))
    db.session.add(CisKartyProTymy(4, 4, 3, 2, 30, 3, 20))
    db.session.add(CisKartyProTymy(4, 5, 1, 8, 15, 3, 20))
    db.session.add(CisKartyProTymy(4, 5, 2, 4, 20, 3, 20))
    db.session.add(CisKartyProTymy(4, 5, 3, 2, 30, 3, 20))
    # -
    db.session.add(CisKartyProTymy(4, 6, 1, 18, 0, 0, 0))
    db.session.add(CisKartyProTymy(4, 7, 1, 18, 0, 0, 0))
    db.session.add(CisKartyProTymy(4, 8, 1, 99, 20, 2, 0))
    db.session.add(CisKartyProTymy(4, 8, 2, 99, 40, 3, 0))
    db.session.add(CisKartyProTymy(4, 11, 1, 5, 0, 0, 0))
    db.session.add(CisKartyProTymy(4, 12, 1, 99, 0, 0, 0))
    # db.session.add(CisKartyProTymy(4, 12, 1, 1, 0, 0, 0))
    db.session.add(CisKartyProTymy(4, 13, 1, 3, 0, 0, 0))
    # pocet = 5
    db.session.add(CisKartyProTymy(5, 1, 1, 5, 15, 6, 30))
    db.session.add(CisKartyProTymy(5, 1, 2, 5, 30, 6, 30))
    db.session.add(CisKartyProTymy(5, 1, 3, 2, 45, 6, 30))
    db.session.add(CisKartyProTymy(5, 2, 1, 20, 12, 3, 15))
    db.session.add(CisKartyProTymy(5, 2, 2, 15, 15, 3, 15))
    db.session.add(CisKartyProTymy(5, 3, 1, 20, 12, 3, 15))
    db.session.add(CisKartyProTymy(5, 3, 2, 15, 15, 3, 15))
    db.session.add(CisKartyProTymy(5, 4, 1, 10, 15, 3, 20))
    db.session.add(CisKartyProTymy(5, 4, 2, 5, 20, 3, 20))
    db.session.add(CisKartyProTymy(5, 4, 3, 2, 30, 3, 20))
    db.session.add(CisKartyProTymy(5, 5, 1, 10, 15, 3, 20))
    db.session.add(CisKartyProTymy(5, 5, 2, 5, 20, 3, 20))
    db.session.add(CisKartyProTymy(5, 5, 3, 2, 30, 3, 20))
    # -
    db.session.add(CisKartyProTymy(5, 6, 1, 18, 0, 0, 0))
    db.session.add(CisKartyProTymy(5, 7, 1, 18, 0, 0, 0))
    db.session.add(CisKartyProTymy(5, 8, 1, 99, 20, 2, 0))
    db.session.add(CisKartyProTymy(5, 8, 2, 99, 40, 3, 0))
    db.session.add(CisKartyProTymy(5, 11, 1, 6, 0, 0, 0))
    db.session.add(CisKartyProTymy(5, 12, 1, 99, 0, 0, 0))
    # db.session.add(CisKartyProTymy(5, 12, 1, 1, 0, 0, 0))
    db.session.add(CisKartyProTymy(5, 13, 1, 3, 0, 0, 0))
    # pocet = 6
    db.session.add(CisKartyProTymy(6, 1, 1, 6, 15, 6, 30))
    db.session.add(CisKartyProTymy(6, 1, 2, 6, 30, 6, 30))
    db.session.add(CisKartyProTymy(6, 1, 3, 2, 45, 6, 30))
    db.session.add(CisKartyProTymy(6, 2, 1, 24, 12, 3, 15))
    db.session.add(CisKartyProTymy(6, 2, 2, 18, 15, 3, 15))
    db.session.add(CisKartyProTymy(6, 3, 1, 24, 12, 3, 15))
    db.session.add(CisKartyProTymy(6, 3, 2, 18, 15, 3, 15))
    db.session.add(CisKartyProTymy(6, 4, 1, 12, 15, 3, 20))
    db.session.add(CisKartyProTymy(6, 4, 1, 12, 15, 3, 20))
    db.session.add(CisKartyProTymy(6, 4, 3, 2, 30, 3, 20))
    db.session.add(CisKartyProTymy(6, 5, 1, 12, 15, 3, 20))
    db.session.add(CisKartyProTymy(6, 5, 2, 6, 20, 3, 20))
    db.session.add(CisKartyProTymy(6, 5, 3, 2, 30, 3, 20))
    # -
    db.session.add(CisKartyProTymy(6, 6, 1, 18, 0, 0, 0))
    db.session.add(CisKartyProTymy(6, 7, 1, 18, 0, 0, 0))
    db.session.add(CisKartyProTymy(6, 8, 1, 99, 20, 2, 0))
    db.session.add(CisKartyProTymy(6, 8, 2, 99, 40, 3, 0))
    db.session.add(CisKartyProTymy(6, 11, 1, 7, 0, 0, 0))
    db.session.add(CisKartyProTymy(6, 12, 1, 99, 0, 0, 0))
    # db.session.add(CisKartyProTymy(6, 12, 1, 1, 0, 0, 0))
    db.session.add(CisKartyProTymy(6, 13, 1, 4, 0, 0, 0))
    db.session.commit()

# delete existing database
if os.path.exists(app.config['DATABASE_PATH']):
    os.remove(app.config['DATABASE_PATH'])

# create the database and the db table
db.create_all()

# fill table
fill_db(db)

# DUMMY ----
# insert users
# db.session.add(User("admin", bcrypt.generate_password_hash("admin"), "admin"))
# db.session.add(User("user1", bcrypt.generate_password_hash("user1"), "ROM"))
# db.session.add(User("user2", bcrypt.generate_password_hash("user2"), "ROM"))

# insert companies
# db.session.add(Company("acka", 1, 2, 3, 4, 5))
# db.session.add(Company("becka", 5, 4, 3, 2, 1))
# db.session.add(Company("jednicky", 1, 1, 1, 1, 1))

# # nf_cis_mista
# db.session.add(CisMista("1. ZŠ", "První 1", "Plzeň", "12345", "gps 1"))
# db.session.add(CisMista("2. ZŠ", "Druhá 2", "Písek", "23456", "gps 2"))
# db.session.add(CisMista("3. ZŠ", "Třetí 3", "Třeboň", "34567", "gps 3"))
# # /DUMMY----
#
# # nf_cis_typy_karet ----
# db.session.add(CisTypyKaret(1, "VVJ", "AH", False, "vývoj", "vývoj, věda, výzkum", "static/image/vyvoj.png"))
#                             # url_for('static', filename='image/vyvoj.png')))
# db.session.add(CisTypyKaret(2, "VRB", "AH", False, "výroba", "výroba", "static/image/vyroba.png"))
#                             # url_for('static', filename='image/vyroba.png')))
# db.session.add(CisTypyKaret(3, "OBD", "AH", False, "obchod", "obchod, distribuce", "static/image/obchod.png"))
#                             # url_for('static', filename='image/obchod.png')))
# db.session.add(CisTypyKaret(4, "SRV", "AH", False, "servis", "servis, služby","static/image/servis.png"))
#                             # url_for('static', filename='image/servis.png')))
# db.session.add(CisTypyKaret(5, "MKT", "AH", False, "marketing", "marketing, propagace","static/image/marketing.png"))
#                             # url_for('static', filename='image/marketing.png')))
# db.session.add(CisTypyKaret(6, "POJ", "AH", False, "pojištění", "pojištění proti negativnímu efektu","static/image/iko_pojisteni.png"))
#                             # url_for('static', filename='image/iko_pojisteni.png')))
# db.session.add(CisTypyKaret(7, "EXP", "AH", False, "expert", "využití služeb experta","static/image/iko_expert.png"))
#                             # url_for('static', filename='image/iko_expert.png')))
# db.session.add(CisTypyKaret(8, "PUJ", "AV", False, "půjčka", "půjčka","static/image/iko_pujcka.png"))
#                             # url_for('static', filename='image/iko_pujcka.png')))
# db.session.add(CisTypyKaret(11, "VYZ", "EH", True, "výzva", "výzva, úkol na celou hru","static/image/iko_ost-vyzva.png"))
#                             # url_for('static', filename='image/iko_ost-vyzva.png')))
# db.session.add(CisTypyKaret(12, "P&R", "EK", True, "P & R", "příležitost / riziko, po dobu jednoho kola","static/image/iko_ost-par.png"))
#                             # url_for('static', filename='image/iko_ost-par.png')))
# db.session.add(CisTypyKaret(13, "HRZ", "EH", True, "hrozba", "hrozba postihu po celou hru","static/image/iko_ost-hrozba.png"))
#                             # url_for('static', filename='image/iko_ost-hrozba.png')))
# # ----
#
# # nf_cis_karty: (karta_id, typk_id, uroven, nazev, popis, castka, symbol_obr, cil, vyhodnoceni)
# # slovnik vyhodnocujicich SQL --
# vyhodnoceni_SQL = defaultdict(str)
# # VYZVY
# vyhodnoceni_SQL[31] = "SELECT Min(H.tym_id) as tym_id, H.typk_id, M.kod, H.poc_karet FROM (SELECT HK2.hra_id, HK2.tym_id, COUNT(HK2.karta_hry_id) AS poc_karet, K.typk_id, K.nazev FROM nf_hry_karty HK2 INNER JOIN `nf_cis_karty`K ON HK2.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK2.hra_id = #hra_id# AND NOT HK2.tym_id IS NULL GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS H INNER JOIN (SELECT SK.hra_id, SK.typk_id, Max(SK.poc_karet) as max_poc_karet, SK.kod FROM (SELECT HK1.hra_id, K.typk_id, COUNT(HK1.karta_hry_id) AS poc_karet, HK1.tym_id, T.kod FROM nf_hry_karty HK1 INNER JOIN `nf_cis_karty`K ON HK1.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK1.hra_id = #hra_id# AND NOT HK1.tym_id IS NULL GROUP BY HK1.hra_id, K.typk_id, T.kod, HK1.tym_id) SK GROUP BY SK.kod) AS M ON H.hra_id = M.hra_id AND H.typk_id = M.typk_id AND H.poc_karet = M.max_poc_karet GROUP BY H.typk_id, M.kod HAVING Min(H.tym_id) = Max(H.tym_id) AND H.poc_karet >=2 AND M.kod = 'VVJ'"
# vyhodnoceni_SQL[32] = "SELECT Min(H.tym_id) as tym_id, H.typk_id, M.kod, H.poc_karet FROM (SELECT HK2.hra_id, HK2.tym_id, COUNT(HK2.karta_hry_id) AS poc_karet, K.typk_id, K.nazev FROM nf_hry_karty HK2 INNER JOIN `nf_cis_karty`K ON HK2.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK2.hra_id = #hra_id# AND NOT HK2.tym_id IS NULL GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS H INNER JOIN (SELECT SK.hra_id, SK.typk_id, Max(SK.poc_karet) as max_poc_karet, SK.kod FROM (SELECT HK1.hra_id, K.typk_id, COUNT(HK1.karta_hry_id) AS poc_karet, HK1.tym_id, T.kod FROM nf_hry_karty HK1 INNER JOIN `nf_cis_karty`K ON HK1.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK1.hra_id = #hra_id# AND NOT HK1.tym_id IS NULL GROUP BY HK1.hra_id, K.typk_id, T.kod, HK1.tym_id) SK GROUP BY SK.kod) AS M ON H.hra_id = M.hra_id AND H.typk_id = M.typk_id AND H.poc_karet = M.max_poc_karet GROUP BY H.typk_id, M.kod HAVING Min(H.tym_id) = Max(H.tym_id) AND H.poc_karet >=2 AND M.kod = 'VRB'"
# vyhodnoceni_SQL[33] = "SELECT Min(H.tym_id) as tym_id, H.typk_id, M.kod, H.poc_karet FROM (SELECT HK2.hra_id, HK2.tym_id, COUNT(HK2.karta_hry_id) AS poc_karet, K.typk_id, K.nazev FROM nf_hry_karty HK2 INNER JOIN `nf_cis_karty`K ON HK2.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK2.hra_id = #hra_id# AND NOT HK2.tym_id IS NULL GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS H INNER JOIN (SELECT SK.hra_id, SK.typk_id, Max(SK.poc_karet) as max_poc_karet, SK.kod FROM (SELECT HK1.hra_id, K.typk_id, COUNT(HK1.karta_hry_id) AS poc_karet, HK1.tym_id, T.kod FROM nf_hry_karty HK1 INNER JOIN `nf_cis_karty`K ON HK1.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK1.hra_id = #hra_id# AND NOT HK1.tym_id IS NULL GROUP BY HK1.hra_id, K.typk_id, T.kod, HK1.tym_id) SK GROUP BY SK.kod) AS M ON H.hra_id = M.hra_id AND H.typk_id = M.typk_id AND H.poc_karet = M.max_poc_karet GROUP BY H.typk_id, M.kod HAVING Min(H.tym_id) = Max(H.tym_id) AND H.poc_karet >=2 AND M.kod = 'OBD'"
# vyhodnoceni_SQL[35] = "SELECT Min(H.tym_id) as tym_id, H.typk_id, M.kod, H.poc_karet FROM (SELECT HK2.hra_id, HK2.tym_id, COUNT(HK2.karta_hry_id) AS poc_karet, K.typk_id, K.nazev FROM nf_hry_karty HK2 INNER JOIN `nf_cis_karty`K ON HK2.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK2.hra_id = #hra_id# AND NOT HK2.tym_id IS NULL GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS H INNER JOIN (SELECT SK.hra_id, SK.typk_id, Max(SK.poc_karet) as max_poc_karet, SK.kod FROM (SELECT HK1.hra_id, K.typk_id, COUNT(HK1.karta_hry_id) AS poc_karet, HK1.tym_id, T.kod FROM nf_hry_karty HK1 INNER JOIN `nf_cis_karty`K ON HK1.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK1.hra_id = #hra_id# AND NOT HK1.tym_id IS NULL GROUP BY HK1.hra_id, K.typk_id, T.kod, HK1.tym_id) SK GROUP BY SK.kod) AS M ON H.hra_id = M.hra_id AND H.typk_id = M.typk_id AND H.poc_karet = M.max_poc_karet GROUP BY H.typk_id, M.kod HAVING Min(H.tym_id) = Max(H.tym_id) AND H.poc_karet >=2 AND M.kod = 'SRV'"
# vyhodnoceni_SQL[36] = "SELECT Min(H.tym_id) as tym_id, H.typk_id, M.kod, H.poc_karet FROM (SELECT HK2.hra_id, HK2.tym_id, COUNT(HK2.karta_hry_id) AS poc_karet, K.typk_id, K.nazev FROM nf_hry_karty HK2 INNER JOIN `nf_cis_karty`K ON HK2.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK2.hra_id = #hra_id# AND NOT HK2.tym_id IS NULL GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS H INNER JOIN (SELECT SK.hra_id, SK.typk_id, Max(SK.poc_karet) as max_poc_karet, SK.kod FROM (SELECT HK1.hra_id, K.typk_id, COUNT(HK1.karta_hry_id) AS poc_karet, HK1.tym_id, T.kod FROM nf_hry_karty HK1 INNER JOIN `nf_cis_karty`K ON HK1.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK1.hra_id = #hra_id# AND NOT HK1.tym_id IS NULL GROUP BY HK1.hra_id, K.typk_id, T.kod, HK1.tym_id) SK GROUP BY SK.kod) AS M ON H.hra_id = M.hra_id AND H.typk_id = M.typk_id AND H.poc_karet = M.max_poc_karet GROUP BY H.typk_id, M.kod HAVING Min(H.tym_id) = Max(H.tym_id) AND H.poc_karet >=2 AND M.kod = 'MKT'"
#
# # P&R
# vyhodnoceni_SQL[50] = "SELECT * FROM (SELECT HK2.hra_id, HK2.tym_id, COUNT(HK2.karta_hry_id) AS poc_karet, K.typk_id, K.nazev FROM nf_hry_karty HK2 INNER JOIN `nf_cis_karty`K ON HK2.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK2.hra_id = #hra_id# AND NOT HK2.tym_id IS NULL GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS H INNER JOIN (SELECT SK.hra_id, SK.typk_id, Max(SK.poc_karet) as max_poc_karet, SK.kod FROM (SELECT HK1.hra_id, K.typk_id, COUNT(HK1.karta_hry_id) AS poc_karet, HK1.tym_id, T.kod FROM nf_hry_karty HK1 INNER JOIN `nf_cis_karty`K ON HK1.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK1.hra_id = #hra_id# AND NOT HK1.tym_id IS NULL GROUP BY HK1.hra_id, K.typk_id, T.kod, HK1.tym_id) SK GROUP BY SK.kod) AS M ON H.hra_id = M.hra_id AND H.typk_id = M.typk_id AND H.poc_karet = M.max_poc_karet AND M.kod = 'VVJ'"
# vyhodnoceni_SQL[52] = "SELECT * FROM (SELECT HK2.hra_id, HK2.tym_id, COUNT(HK2.karta_hry_id) AS poc_karet, K.typk_id, K.nazev FROM nf_hry_karty HK2 INNER JOIN `nf_cis_karty`K ON HK2.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK2.hra_id = #hra_id# AND NOT HK2.tym_id IS NULL GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS H INNER JOIN (SELECT SK.hra_id, SK.typk_id, Max(SK.poc_karet) as max_poc_karet, SK.kod FROM (SELECT HK1.hra_id, K.typk_id, COUNT(HK1.karta_hry_id) AS poc_karet, HK1.tym_id, T.kod FROM nf_hry_karty HK1 INNER JOIN `nf_cis_karty`K ON HK1.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK1.hra_id = #hra_id# AND NOT HK1.tym_id IS NULL GROUP BY HK1.hra_id, K.typk_id, T.kod, HK1.tym_id) SK GROUP BY SK.kod) AS M ON H.hra_id = M.hra_id AND H.typk_id = M.typk_id AND H.poc_karet = M.max_poc_karet AND M.kod = 'VRB'"
# vyhodnoceni_SQL[53] = "SELECT * FROM (SELECT HK2.hra_id, HK2.tym_id, COUNT(HK2.karta_hry_id) AS poc_karet, K.typk_id, K.nazev FROM nf_hry_karty HK2 INNER JOIN `nf_cis_karty`K ON HK2.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK2.hra_id = #hra_id# AND NOT HK2.tym_id IS NULL GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS H INNER JOIN (SELECT SK.hra_id, SK.typk_id, Max(SK.poc_karet) as max_poc_karet, SK.kod FROM (SELECT HK1.hra_id, K.typk_id, COUNT(HK1.karta_hry_id) AS poc_karet, HK1.tym_id, T.kod FROM nf_hry_karty HK1 INNER JOIN `nf_cis_karty`K ON HK1.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK1.hra_id = #hra_id# AND NOT HK1.tym_id IS NULL GROUP BY HK1.hra_id, K.typk_id, T.kod, HK1.tym_id) SK GROUP BY SK.kod) AS M ON H.hra_id = M.hra_id AND H.typk_id = M.typk_id AND H.poc_karet = M.max_poc_karet AND M.kod = 'OBD'"
# vyhodnoceni_SQL[56] = "SELECT * FROM (SELECT HK2.hra_id, HK2.tym_id, COUNT(HK2.karta_hry_id) AS poc_karet, K.typk_id, K.nazev FROM nf_hry_karty HK2 INNER JOIN `nf_cis_karty`K ON HK2.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK2.hra_id = #hra_id# AND NOT HK2.tym_id IS NULL GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS H INNER JOIN (SELECT SK.hra_id, SK.typk_id, Max(SK.poc_karet) as max_poc_karet, SK.kod FROM (SELECT HK1.hra_id, K.typk_id, COUNT(HK1.karta_hry_id) AS poc_karet, HK1.tym_id, T.kod FROM nf_hry_karty HK1 INNER JOIN `nf_cis_karty`K ON HK1.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK1.hra_id = #hra_id# AND NOT HK1.tym_id IS NULL GROUP BY HK1.hra_id, K.typk_id, T.kod, HK1.tym_id) SK GROUP BY SK.kod) AS M ON H.hra_id = M.hra_id AND H.typk_id = M.typk_id AND H.poc_karet = M.max_poc_karet AND M.kod = 'SRV'"
# vyhodnoceni_SQL[57] = "SELECT * FROM (SELECT HK2.hra_id, HK2.tym_id, COUNT(HK2.karta_hry_id) AS poc_karet, K.typk_id, K.nazev FROM nf_hry_karty HK2 INNER JOIN `nf_cis_karty`K ON HK2.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK2.hra_id = #hra_id# AND NOT HK2.tym_id IS NULL GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS H INNER JOIN (SELECT SK.hra_id, SK.typk_id, Max(SK.poc_karet) as max_poc_karet, SK.kod FROM (SELECT HK1.hra_id, K.typk_id, COUNT(HK1.karta_hry_id) AS poc_karet, HK1.tym_id, T.kod FROM nf_hry_karty HK1 INNER JOIN `nf_cis_karty`K ON HK1.karta_id = K.karta_id INNER JOIN `nf_cis_typy_karet` T ON K.typk_id = T.typk_id WHERE HK1.hra_id = #hra_id# AND NOT HK1.tym_id IS NULL GROUP BY HK1.hra_id, K.typk_id, T.kod, HK1.tym_id) SK GROUP BY SK.kod) AS M ON H.hra_id = M.hra_id AND H.typk_id = M.typk_id AND H.poc_karet = M.max_poc_karet AND M.kod = 'MKT'"
# vyhodnoceni_SQL[58] = "SELECT S1.hra_id, S1.tym_id, S1.typk_id, S1.kod, S1.poc_karet FROM (SELECT HT.hra_id, HT.tym_id, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) AS poc_karet FROM (SELECT hra_id, tym_id, typk_id, kod FROM nf_hry_tymy, nf_cis_typy_karet WHERE hra_id = #hra_id# AND kod IN ('VVJ', 'VRB', 'OBD', 'SRV', 'MKT') GROUP BY hra_id, tym_id, typk_id) AS HT LEFT JOIN (SELECT hra_id, tym_id, typk_id, COUNT(karta_hry_id) as poc_karet FROM nf_hry_karty HK2 INNER JOIN nf_cis_karty K ON HK2.karta_id = K.karta_id GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS HK ON HT.hra_id = HK.hra_id AND HT.tym_id = HK.tym_id AND HT.typk_id = HK.typk_id) AS S1 INNER JOIN (SELECT HT.hra_id, Min(HT.tym_id) AS MinTID, Max(HT.tym_id) AS MaxTID, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) AS poc_karet FROM (SELECT hra_id, tym_id, typk_id, kod FROM nf_hry_tymy, nf_cis_typy_karet WHERE hra_id = #hra_id# AND kod IN ('VVJ', 'VRB', 'OBD', 'SRV', 'MKT') GROUP BY hra_id, tym_id, typk_id) AS HT LEFT JOIN (SELECT hra_id, tym_id, typk_id, COUNT(karta_hry_id) as poc_karet FROM nf_hry_karty HK2 INNER JOIN nf_cis_karty K ON HK2.karta_id = K.karta_id GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS HK ON HT.hra_id = HK.hra_id AND HT.tym_id = HK.tym_id AND HT.typk_id = HK.typk_id GROUP BY HT.hra_id, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) HAVING HT.kod = 'VVJ' LIMIT 1) AS S2 ON S1.hra_id = S2.hra_id AND S1.typk_id = S2.typk_id AND S1.poc_karet = S2.poc_karet"
# vyhodnoceni_SQL[59] = "SELECT S1.hra_id, S1.tym_id, S1.typk_id, S1.kod, S1.poc_karet FROM (SELECT HT.hra_id, HT.tym_id, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) AS poc_karet FROM (SELECT hra_id, tym_id, typk_id, kod FROM nf_hry_tymy, nf_cis_typy_karet WHERE hra_id = #hra_id# AND kod IN ('VVJ', 'VRB', 'OBD', 'SRV', 'MKT') GROUP BY hra_id, tym_id, typk_id) AS HT LEFT JOIN (SELECT hra_id, tym_id, typk_id, COUNT(karta_hry_id) as poc_karet FROM nf_hry_karty HK2 INNER JOIN nf_cis_karty K ON HK2.karta_id = K.karta_id GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS HK ON HT.hra_id = HK.hra_id AND HT.tym_id = HK.tym_id AND HT.typk_id = HK.typk_id) AS S1 INNER JOIN (SELECT HT.hra_id, Min(HT.tym_id) AS MinTID, Max(HT.tym_id) AS MaxTID, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) AS poc_karet FROM (SELECT hra_id, tym_id, typk_id, kod FROM nf_hry_tymy, nf_cis_typy_karet WHERE hra_id = #hra_id# AND kod IN ('VVJ', 'VRB', 'OBD', 'SRV', 'MKT') GROUP BY hra_id, tym_id, typk_id) AS HT LEFT JOIN (SELECT hra_id, tym_id, typk_id, COUNT(karta_hry_id) as poc_karet FROM nf_hry_karty HK2 INNER JOIN nf_cis_karty K ON HK2.karta_id = K.karta_id GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS HK ON HT.hra_id = HK.hra_id AND HT.tym_id = HK.tym_id AND HT.typk_id = HK.typk_id GROUP BY HT.hra_id, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) HAVING HT.kod = 'VRB' LIMIT 1) AS S2 ON S1.hra_id = S2.hra_id AND S1.typk_id = S2.typk_id AND S1.poc_karet = S2.poc_karet"
# vyhodnoceni_SQL[60] = "SELECT S1.hra_id, S1.tym_id, S1.typk_id, S1.kod, S1.poc_karet FROM (SELECT HT.hra_id, HT.tym_id, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) AS poc_karet FROM (SELECT hra_id, tym_id, typk_id, kod FROM nf_hry_tymy, nf_cis_typy_karet WHERE hra_id = #hra_id# AND kod IN ('VVJ', 'VRB', 'OBD', 'SRV', 'MKT') GROUP BY hra_id, tym_id, typk_id) AS HT LEFT JOIN (SELECT hra_id, tym_id, typk_id, COUNT(karta_hry_id) as poc_karet FROM nf_hry_karty HK2 INNER JOIN nf_cis_karty K ON HK2.karta_id = K.karta_id GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS HK ON HT.hra_id = HK.hra_id AND HT.tym_id = HK.tym_id AND HT.typk_id = HK.typk_id) AS S1 INNER JOIN (SELECT HT.hra_id, Min(HT.tym_id) AS MinTID, Max(HT.tym_id) AS MaxTID, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) AS poc_karet FROM (SELECT hra_id, tym_id, typk_id, kod FROM nf_hry_tymy, nf_cis_typy_karet WHERE hra_id = #hra_id# AND kod IN ('VVJ', 'VRB', 'OBD', 'SRV', 'MKT') GROUP BY hra_id, tym_id, typk_id) AS HT LEFT JOIN (SELECT hra_id, tym_id, typk_id, COUNT(karta_hry_id) as poc_karet FROM nf_hry_karty HK2 INNER JOIN nf_cis_karty K ON HK2.karta_id = K.karta_id GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS HK ON HT.hra_id = HK.hra_id AND HT.tym_id = HK.tym_id AND HT.typk_id = HK.typk_id GROUP BY HT.hra_id, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) HAVING HT.kod = 'OBD' LIMIT 1) AS S2 ON S1.hra_id = S2.hra_id AND S1.typk_id = S2.typk_id AND S1.poc_karet = S2.poc_karet"
# vyhodnoceni_SQL[61] = "SELECT S1.hra_id, S1.tym_id, S1.typk_id, S1.kod, S1.poc_karet FROM (SELECT HT.hra_id, HT.tym_id, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) AS poc_karet FROM (SELECT hra_id, tym_id, typk_id, kod FROM nf_hry_tymy, nf_cis_typy_karet WHERE hra_id = #hra_id# AND kod IN ('VVJ', 'VRB', 'OBD', 'SRV', 'MKT') GROUP BY hra_id, tym_id, typk_id) AS HT LEFT JOIN (SELECT hra_id, tym_id, typk_id, COUNT(karta_hry_id) as poc_karet FROM nf_hry_karty HK2 INNER JOIN nf_cis_karty K ON HK2.karta_id = K.karta_id GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS HK ON HT.hra_id = HK.hra_id AND HT.tym_id = HK.tym_id AND HT.typk_id = HK.typk_id) AS S1 INNER JOIN (SELECT HT.hra_id, Min(HT.tym_id) AS MinTID, Max(HT.tym_id) AS MaxTID, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) AS poc_karet FROM (SELECT hra_id, tym_id, typk_id, kod FROM nf_hry_tymy, nf_cis_typy_karet WHERE hra_id = #hra_id# AND kod IN ('VVJ', 'VRB', 'OBD', 'SRV', 'MKT') GROUP BY hra_id, tym_id, typk_id) AS HT LEFT JOIN (SELECT hra_id, tym_id, typk_id, COUNT(karta_hry_id) as poc_karet FROM nf_hry_karty HK2 INNER JOIN nf_cis_karty K ON HK2.karta_id = K.karta_id GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS HK ON HT.hra_id = HK.hra_id AND HT.tym_id = HK.tym_id AND HT.typk_id = HK.typk_id GROUP BY HT.hra_id, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) HAVING HT.kod = 'SRV' LIMIT 1) AS S2 ON S1.hra_id = S2.hra_id AND S1.typk_id = S2.typk_id AND S1.poc_karet = S2.poc_karet"
# vyhodnoceni_SQL[62] = "SELECT S1.hra_id, S1.tym_id, S1.typk_id, S1.kod, S1.poc_karet FROM (SELECT HT.hra_id, HT.tym_id, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) AS poc_karet FROM (SELECT hra_id, tym_id, typk_id, kod FROM nf_hry_tymy, nf_cis_typy_karet WHERE hra_id = #hra_id# AND kod IN ('VVJ', 'VRB', 'OBD', 'SRV', 'MKT') GROUP BY hra_id, tym_id, typk_id) AS HT LEFT JOIN (SELECT hra_id, tym_id, typk_id, COUNT(karta_hry_id) as poc_karet FROM nf_hry_karty HK2 INNER JOIN nf_cis_karty K ON HK2.karta_id = K.karta_id GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS HK ON HT.hra_id = HK.hra_id AND HT.tym_id = HK.tym_id AND HT.typk_id = HK.typk_id) AS S1 INNER JOIN (SELECT HT.hra_id, Min(HT.tym_id) AS MinTID, Max(HT.tym_id) AS MaxTID, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) AS poc_karet FROM (SELECT hra_id, tym_id, typk_id, kod FROM nf_hry_tymy, nf_cis_typy_karet WHERE hra_id = #hra_id# AND kod IN ('VVJ', 'VRB', 'OBD', 'SRV', 'MKT') GROUP BY hra_id, tym_id, typk_id) AS HT LEFT JOIN (SELECT hra_id, tym_id, typk_id, COUNT(karta_hry_id) as poc_karet FROM nf_hry_karty HK2 INNER JOIN nf_cis_karty K ON HK2.karta_id = K.karta_id GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS HK ON HT.hra_id = HK.hra_id AND HT.tym_id = HK.tym_id AND HT.typk_id = HK.typk_id GROUP BY HT.hra_id, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) HAVING HT.kod = 'MKT' LIMIT 1) AS S2 ON S1.hra_id = S2.hra_id AND S1.typk_id = S2.typk_id AND S1.poc_karet = S2.poc_karet"
#
# # HROZBY
# vyhodnoceni_SQL[70] = "SELECT SX.hra_id, SX.MinTID, SX.MaxTID, SX.typk_id, SX.kod, SX.poc_karet FROM (SELECT HT.hra_id, Min(HT.tym_id) AS MinTID, Max(HT.tym_id) AS MaxTID, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) AS poc_karet FROM (SELECT hra_id, tym_id, typk_id, kod FROM nf_hry_tymy, nf_cis_typy_karet WHERE hra_id = #hra_id# AND kod IN ('VVJ', 'VRB', 'OBD', 'SRV', 'MKT') GROUP BY hra_id, tym_id, typk_id) AS HT LEFT JOIN (SELECT hra_id, tym_id, typk_id, COUNT(karta_hry_id) as poc_karet FROM nf_hry_karty HK2 INNER JOIN nf_cis_karty K ON HK2.karta_id = K.karta_id GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS HK ON HT.hra_id = HK.hra_id AND HT.tym_id = HK.tym_id AND HT.typk_id = HK.typk_id GROUP BY HT.hra_id, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) HAVING HT.kod = 'SRV' LIMIT 1) AS SX WHERE SX.MinTID = SX.MaxTID"
# vyhodnoceni_SQL[71] = "SELECT SX.hra_id, SX.MinTID, SX.MaxTID, SX.typk_id, SX.kod, SX.poc_karet FROM (SELECT HT.hra_id, Min(HT.tym_id) AS MinTID, Max(HT.tym_id) AS MaxTID, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) AS poc_karet FROM (SELECT hra_id, tym_id, typk_id, kod FROM nf_hry_tymy, nf_cis_typy_karet WHERE hra_id = #hra_id# AND kod IN ('VVJ', 'VRB', 'OBD', 'SRV', 'MKT') GROUP BY hra_id, tym_id, typk_id) AS HT LEFT JOIN (SELECT hra_id, tym_id, typk_id, COUNT(karta_hry_id) as poc_karet FROM nf_hry_karty HK2 INNER JOIN nf_cis_karty K ON HK2.karta_id = K.karta_id GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS HK ON HT.hra_id = HK.hra_id AND HT.tym_id = HK.tym_id AND HT.typk_id = HK.typk_id GROUP BY HT.hra_id, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) HAVING HT.kod = 'MKT' LIMIT 1) AS SX WHERE SX.MinTID = SX.MaxTID"
# vyhodnoceni_SQL[74] = "SELECT SX.hra_id, SX.MinTID, SX.MaxTID, SX.typk_id, SX.kod, SX.poc_karet FROM (SELECT HT.hra_id, Min(HT.tym_id) AS MinTID, Max(HT.tym_id) AS MaxTID, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) AS poc_karet FROM (SELECT hra_id, tym_id, typk_id, kod FROM nf_hry_tymy, nf_cis_typy_karet WHERE hra_id = #hra_id# AND kod IN ('VVJ', 'VRB', 'OBD', 'SRV', 'MKT') GROUP BY hra_id, tym_id, typk_id) AS HT LEFT JOIN (SELECT hra_id, tym_id, typk_id, COUNT(karta_hry_id) as poc_karet FROM nf_hry_karty HK2 INNER JOIN nf_cis_karty K ON HK2.karta_id = K.karta_id GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS HK ON HT.hra_id = HK.hra_id AND HT.tym_id = HK.tym_id AND HT.typk_id = HK.typk_id GROUP BY HT.hra_id, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) HAVING HT.kod = 'VVJ' LIMIT 1) AS SX WHERE SX.MinTID = SX.MaxTID"
# vyhodnoceni_SQL[75] = "SELECT SX.hra_id, SX.MinTID, SX.MaxTID, SX.typk_id, SX.kod, SX.poc_karet FROM (SELECT HT.hra_id, Min(HT.tym_id) AS MinTID, Max(HT.tym_id) AS MaxTID, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) AS poc_karet FROM (SELECT hra_id, tym_id, typk_id, kod FROM nf_hry_tymy, nf_cis_typy_karet WHERE hra_id = #hra_id# AND kod IN ('VVJ', 'VRB', 'OBD', 'SRV', 'MKT') GROUP BY hra_id, tym_id, typk_id) AS HT LEFT JOIN (SELECT hra_id, tym_id, typk_id, COUNT(karta_hry_id) as poc_karet FROM nf_hry_karty HK2 INNER JOIN nf_cis_karty K ON HK2.karta_id = K.karta_id GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS HK ON HT.hra_id = HK.hra_id AND HT.tym_id = HK.tym_id AND HT.typk_id = HK.typk_id GROUP BY HT.hra_id, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) HAVING HT.kod = 'VRB' LIMIT 1) AS SX WHERE SX.MinTID = SX.MaxTID"
# vyhodnoceni_SQL[76] = "SELECT SX.hra_id, SX.MinTID, SX.MaxTID, SX.typk_id, SX.kod, SX.poc_karet FROM (SELECT HT.hra_id, Min(HT.tym_id) AS MinTID, Max(HT.tym_id) AS MaxTID, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) AS poc_karet FROM (SELECT hra_id, tym_id, typk_id, kod FROM nf_hry_tymy, nf_cis_typy_karet WHERE hra_id = #hra_id# AND kod IN ('VVJ', 'VRB', 'OBD', 'SRV', 'MKT') GROUP BY hra_id, tym_id, typk_id) AS HT LEFT JOIN (SELECT hra_id, tym_id, typk_id, COUNT(karta_hry_id) as poc_karet FROM nf_hry_karty HK2 INNER JOIN nf_cis_karty K ON HK2.karta_id = K.karta_id GROUP BY HK2.hra_id, HK2.tym_id, K.typk_id) AS HK ON HT.hra_id = HK.hra_id AND HT.tym_id = HK.tym_id AND HT.typk_id = HK.typk_id GROUP BY HT.hra_id, HT.typk_id, HT.kod, IFNULL(HK.poc_karet, 0) HAVING HT.kod = 'OBD' LIMIT 1) AS SX WHERE SX.MinTID = SX.MaxTID"
# # --
# # -- karty akci
# db.session.add(CisKarty(1, 1, 1, 'vývoj', 'vývoj, věda, výzkum', 15, 'sym_01_VVJ-01.png', 0, ''))
# db.session.add(CisKarty(2, 1, 2, 'vývoj', 'vývoj, věda, výzkum', 30, 'sym_02_VVJ-02.png', 0, ''))
# db.session.add(CisKarty(3, 1, 3, 'vývoj', 'vývoj, věda, výzkum', 45, 'sym_03_VVJ-03.png', 0, ''))
# db.session.add(CisKarty(4, 2, 1, 'výroba', 'výroba', 12, 'sym_04_VRB-04.png', 0, ''))
# db.session.add(CisKarty(5, 2, 2, 'výroba', 'výroba', 15, 'sym_05_VRB-05.png', 0, ''))
# db.session.add(CisKarty(6, 2, 3, 'výroba', 'výroba', 20, 'sym_06_VRB-06.png', 0, ''))
# db.session.add(CisKarty(7, 3, 1, 'obchod', 'obchod, distribuce', 12, 'sym_07_OBD-07.png', 0, ''))
# db.session.add(CisKarty(8, 3, 2, 'obchod', 'obchod, distribuce', 15, 'sym_08_OBD-08.png', 0, ''))
# db.session.add(CisKarty(9, 3, 3, 'obchod', 'obchod, distribuce', 20, 'sym_09_OBD-09.png', 0, ''))
# db.session.add(CisKarty(10, 4, 1, 'servis', 'servis, služby', 15, 'sym_10_SRV-10.png', 0, ''))
# db.session.add(CisKarty(11, 4, 2, 'servis', 'servis, služby', 20, 'sym_11_SRV-11.png', 0, ''))
# db.session.add(CisKarty(12, 4, 3, 'servis', 'servis, služby', 30, 'sym_12_SRV-12.png', 0, ''))
# db.session.add(CisKarty(13, 5, 1, 'marketing', 'marketing, propagace', 15, 'sym_13_MKT-13.png', 0, ''))
# db.session.add(CisKarty(14, 5, 2, 'marketing', 'marketing, propagace', 20, 'sym_14_MKT-14.png', 0, ''))
# db.session.add(CisKarty(15, 5, 3, 'marketing', 'marketing, propagace', 30, 'sym_15_MKT-15.png', 0, ''))
# db.session.add(CisKarty(16, 6, 1, 'pojištění', 'pojištění proti negativnímu efektu', 0, 'sym_16_POJ-16.png', 0, ''))
# db.session.add(CisKarty(17, 7, 1, 'expert', 'využití služeb experta', 0, 'sym_17_EXP-17.png', 0, ''))
# # db.session.add(CisKarty(18, 8, 1, 'půjčka', 'půjčka', 0, 'sym_18_PUJ-18.png', 0, ''))
# db.session.add(CisKarty(18, 8, 1, 'půjčka', 'malá půjčka', -20, 'sym_18_PUJ-18.png', 0, ''))
# db.session.add(CisKarty(19, 8, 2, 'půjčka', 'velká půjčka', -40, 'sym_18_PUJ-18.png', 0, ''))
#
# # -- vyzvy
# db.session.add(CisKarty(31, 11, 1, 'Nejlepší vývojový tým', 'Nejvíce investic do vývoje, min. 2', 30, 'sym_31_VYZ-31.png', 1, ''))
# db.session.add(CisKarty(32, 11, 1, 'Tahoun výroby', 'Nejvíce investic do výroby, min. 2', 30, 'sym_32_VYZ-32.png', 1, ''))
# db.session.add(CisKarty(33, 11, 1, 'Nejlepší obchodník', 'Nejvíce investic do obchodu, min. 2', 30, 'sym_33_VYZ-33.png', 1, ''))
# db.session.add(CisKarty(34, 11, 1, 'Nejlepší dodavatel', 'Nejvíce dvojic výroba + obchod, min. 2', 30, 'sym_34_VYZ-34.png', 1, ''))
# db.session.add(CisKarty(35, 11, 1, 'Nejkvalitnější servis', 'Nejvíce investic do servisu, min. 2', 30, 'sym_35_VYZ-35.png', 1, ''))
# db.session.add(CisKarty(36, 11, 1, 'Nejlepší kampaň marketingu', 'Nejvíce investic do marketingu, min. 2', 30, 'sym_36_VYZ-36.png', 1, ''))
# db.session.add(CisKarty(37, 11, 1, 'Prosperující firma', 'Nejvyšší celkový příjem', 30, 'sym_37_VYZ-37.png', 1, ''))
# db.session.add(CisKarty(38, 11, 1, 'Nejlepší investiční krok', 'Nejvyšší kvartálový příjem', 30, 'sym_38_VYZ-38.png', 1, ''))
# db.session.add(CisKarty(39, 11, 1, 'Kvalitní zázemí', 'Nejvíce investic do vývoje + servisu + marketingu (min. 4)', 30, 'sym_39_VYZ-39.png', 1, ''))
# db.session.add(CisKarty(40, 11, 1, 'Zacíleno na zákazníka', 'Nejvíce investic do vývoje + marketingu (min. 4)', 30, 'sym_40_VYZ-40.png', 1, ''))
# db.session.add(CisKarty(41, 11, 1, 'Důraz na inovace', 'Nejvíce investic do vývoje + servisu (min. 4)', 30, 'sym_41_VYZ-41.png', 1, ''))
# db.session.add(CisKarty(42, 11, 1, 'Propagace služeb', 'Nejvíce investic do servisu + marketingu (min. 4)', 30, 'sym_42_VYZ-42.png', 1, ''))
# # -- P&R
# db.session.add(CisKarty(50, 12, 1, 'Inovativní přístup', 'Nejvíce investic do vývoje', 30, 'sym_50_P&R-50.png', 99, ''))
# db.session.add(CisKarty(51, 12, 1, 'Popularizace vývoje', 'Nejvíce dvojic vývoj + marketing (při shodě rozhoduje marketing)', 30, 'sym_51_P&R-51.png', 99, ''))
# db.session.add(CisKarty(52, 12, 1, 'Podpora výrobců', 'Nejvíce investic do výroby', 30, 'sym_52_P&R-52.png', 99, ''))
# db.session.add(CisKarty(53, 12, 1, 'Oživení obchodu', 'Nejvíce investic do obchodu', 30, 'sym_53_P&R-53.png', 99, ''))
# db.session.add(CisKarty(54, 12, 1, 'Kvalitní obchodní model', 'Nejvíce dvojic výroba + obchod (při shodě rozhoduje výroba)', 30, 'sym_54_P&R-54.png', 99, ''))
# db.session.add(CisKarty(55, 12, 1, 'Nové obchodní příležitosti', 'Nejvíce dvojic výroba + obchod (při shodě rozhoduje marketing)', 30, 'sym_55_P&R-55.png', 99, ''))
# db.session.add(CisKarty(56, 12, 1, 'Kvalitní zákaznická podpora', 'Nejvíce investic do servisu', 30, 'sym_56_P&R-56.png', 99, ''))
# db.session.add(CisKarty(57, 12, 1, 'Univerzální prodejci', 'Nejvíce investic do marketingu', 30, 'sym_57_P&R-57.png', 99, ''))
# db.session.add(CisKarty(58, 12, 1, 'Nedostatek nápadů', 'Nejméně investic do vývoje', -30, 'sym_58_P&R-58.png', 99, ''))
# db.session.add(CisKarty(59, 12, 1, 'Nízká kvalita výroby', 'Nejméně investic do výroby', -30, 'sym_59_P&R-59.png', 99, ''))
# db.session.add(CisKarty(60, 12, 1, 'Podomní prodejci', 'Nejméně investic do obchodu', -30, 'sym_60_P&R-60.png', 99, ''))
# db.session.add(CisKarty(61, 12, 1, 'Nefunkční zákaznická linka', 'Nejméně investic do servisu', -30, 'sym_61_P&R-61.png', 99, ''))
# db.session.add(CisKarty(62, 12, 1, 'Zmařená kampaň', 'Nejméně investic do marketingu', -30, 'sym_62_P&R-62.png', 99, ''))
# db.session.add(CisKarty(63, 12, 1, 'Nevyužité investice', 'Nejnižší investice v tomto kvartálu', -30, 'sym_63_P&R-63.png', 99, ''))
# db.session.add(CisKarty(64, 12, 1, 'Příprava úspor', 'Nejnižší investice v tomto kvartálu', 30, 'sym_64_P&R-64.png', 99, ''))
# # -- Hrozby
# db.session.add(CisKarty(70, 13, 1, 'Nízká úroveň služeb zákazníkům', 'Nejméně investic do servisu', -20, 'sym_70_HRZ-70.png', 1, ''))
# db.session.add(CisKarty(71, 13, 1, 'Nízká úroveň marketingu', 'Nejméně investic do marketingu', -20, 'sym_71_HRZ-71.png', 1, ''))
# db.session.add(CisKarty(72, 13, 1, 'Firma bez zázemí', 'Nejméně investic do vývoje + servisu + marketingu', -20, 'sym_72_HRZ-72.png', 1, ''))
# db.session.add(CisKarty(73, 13, 1, 'Nevyváženost investic', 'Největší počet oblastí s nejméně investicemi', -20, 'sym_73_HRZ-73.png', 1, ''))
# db.session.add(CisKarty(74, 13, 1, 'Nízká efektivita vývoje', 'Nejméně investic do vývoje', -20, 'sym_74_HRZ-74.png', 1, ''))
# db.session.add(CisKarty(75, 13, 1, 'Slabá optimalizace výroby', 'Nejméně investic do výroby', -20, 'sym_75_HRZ-75.png', 1, ''))
# db.session.add(CisKarty(76, 13, 1, 'Nízká úroveň obchodu', 'Nejméně investic do obchodu', -20, 'sym_76_HRZ-76.png', 1, ''))
# db.session.add(CisKarty(77, 13, 1, 'Nekoordinovaná výroba a obchod', 'Nejmenší počet dvojic výroba + obchod', -20, 'sym_77_HRZ-77.png', 1, ''))
# # doplneni vyhodnoceni
# for row in CisKarty.query:
#     row.vyhodnoceni = vyhodnoceni_SQL[row.karta_id]
#
# # nf_cis_karty_pro_tymy: (poc_tymu, typk_id, uroven, pocet, cena, naklady, prijem)
# # pocet = 2
# db.session.add(CisKartyProTymy(2, 1, 1, 2, 15, 6, 30))
# db.session.add(CisKartyProTymy(2, 1, 2, 3, 30, 6, 30))
# db.session.add(CisKartyProTymy(2, 1, 3, 1, 45, 6, 30))
# db.session.add(CisKartyProTymy(2, 2, 1, 7, 12, 3, 15))
# db.session.add(CisKartyProTymy(2, 2, 2, 7, 15, 3, 15))
# db.session.add(CisKartyProTymy(2, 3, 1, 7, 12, 3, 15))
# db.session.add(CisKartyProTymy(2, 3, 2, 7, 15, 3, 15))
# db.session.add(CisKartyProTymy(2, 4, 1, 4, 15, 3, 20))
# db.session.add(CisKartyProTymy(2, 4, 2, 3, 20, 3, 20))
# db.session.add(CisKartyProTymy(2, 4, 3, 1, 30, 3, 20))
# db.session.add(CisKartyProTymy(2, 5, 1, 4, 15, 3, 20))
# db.session.add(CisKartyProTymy(2, 5, 2, 3, 20, 3, 20))
# db.session.add(CisKartyProTymy(2, 5, 3, 1, 30, 3, 20))
# # -
# db.session.add(CisKartyProTymy(2, 6, 1, 18, 0, 0, 0))
# db.session.add(CisKartyProTymy(2, 7, 1, 18, 0, 0, 0))
# db.session.add(CisKartyProTymy(2, 8, 1, 99, 20, 2, 0))
# db.session.add(CisKartyProTymy(2, 8, 2, 99, 40, 3, 0))
# db.session.add(CisKartyProTymy(2, 11, 1, 3, 0, 0, 0))
# db.session.add(CisKartyProTymy(2, 12, 1, 99, 0, 0, 0))
# # db.session.add(CisKartyProTymy(2, 12, 1, 1, 0, 0, 0))
# db.session.add(CisKartyProTymy(2, 13, 1, 2, 0, 0, 0))
# # pocet = 3
# db.session.add(CisKartyProTymy(3, 1, 1, 3, 15, 6, 30))
# db.session.add(CisKartyProTymy(3, 1, 2, 3, 30, 6, 30))
# db.session.add(CisKartyProTymy(3, 1, 3, 2, 45, 6, 30))
# db.session.add(CisKartyProTymy(3, 2, 1, 12, 12, 3, 15))
# db.session.add(CisKartyProTymy(3, 2, 2, 9, 15, 3, 15))
# db.session.add(CisKartyProTymy(3, 3, 1, 12, 12, 3, 15))
# db.session.add(CisKartyProTymy(3, 3, 2, 9, 15, 3, 15))
# db.session.add(CisKartyProTymy(3, 4, 1, 6, 15, 3, 20))
# db.session.add(CisKartyProTymy(3, 4, 2, 3, 20, 3, 20))
# db.session.add(CisKartyProTymy(3, 4, 3, 2, 30, 3, 20))
# db.session.add(CisKartyProTymy(3, 5, 1, 6, 15, 3, 20))
# db.session.add(CisKartyProTymy(3, 5, 2, 3, 20, 3, 20))
# db.session.add(CisKartyProTymy(3, 5, 3, 2, 30, 3, 20))
# # -
# db.session.add(CisKartyProTymy(3, 6, 1, 18, 0, 0, 0))
# db.session.add(CisKartyProTymy(3, 7, 1, 18, 0, 0, 0))
# db.session.add(CisKartyProTymy(3, 8, 1, 99, 20, 2, 0))
# db.session.add(CisKartyProTymy(3, 8, 2, 99, 40, 3, 0))
# db.session.add(CisKartyProTymy(3, 11, 1, 4, 0, 0, 0))
# db.session.add(CisKartyProTymy(3, 12, 1, 99, 0, 0, 0))
# # db.session.add(CisKartyProTymy(3, 12, 1, -1, 0, 0, 0))
# db.session.add(CisKartyProTymy(3, 13, 1, 2, 0, 0, 0))
# # pocet = 4
# db.session.add(CisKartyProTymy(4, 1, 1, 4, 15, 6, 30))
# db.session.add(CisKartyProTymy(4, 1, 2, 4, 30, 6, 30))
# db.session.add(CisKartyProTymy(4, 1, 3, 2, 45, 6, 30))
# db.session.add(CisKartyProTymy(4, 2, 1, 16, 12, 3, 15))
# db.session.add(CisKartyProTymy(4, 2, 2, 12, 15, 3, 15))
# db.session.add(CisKartyProTymy(4, 3, 1, 16, 12, 3, 15))
# db.session.add(CisKartyProTymy(4, 3, 2, 12, 15, 3, 15))
# db.session.add(CisKartyProTymy(4, 4, 1, 8, 15, 3, 20))
# db.session.add(CisKartyProTymy(4, 4, 2, 4, 20, 3, 20))
# db.session.add(CisKartyProTymy(4, 4, 3, 2, 30, 3, 20))
# db.session.add(CisKartyProTymy(4, 5, 1, 8, 15, 3, 20))
# db.session.add(CisKartyProTymy(4, 5, 2, 4, 20, 3, 20))
# db.session.add(CisKartyProTymy(4, 5, 3, 2, 30, 3, 20))
# # -
# db.session.add(CisKartyProTymy(4, 6, 1, 18, 0, 0, 0))
# db.session.add(CisKartyProTymy(4, 7, 1, 18, 0, 0, 0))
# db.session.add(CisKartyProTymy(4, 8, 1, 99, 20, 2, 0))
# db.session.add(CisKartyProTymy(4, 8, 2, 99, 40, 3, 0))
# db.session.add(CisKartyProTymy(4, 11, 1, 5, 0, 0, 0))
# db.session.add(CisKartyProTymy(4, 12, 1, 99, 0, 0, 0))
# # db.session.add(CisKartyProTymy(4, 12, 1, 1, 0, 0, 0))
# db.session.add(CisKartyProTymy(4, 13, 1, 3, 0, 0, 0))
# # pocet = 5
# db.session.add(CisKartyProTymy(5, 1, 1, 5, 15, 6, 30))
# db.session.add(CisKartyProTymy(5, 1, 2, 5, 30, 6, 30))
# db.session.add(CisKartyProTymy(5, 1, 3, 2, 45, 6, 30))
# db.session.add(CisKartyProTymy(5, 2, 1, 20, 12, 3, 15))
# db.session.add(CisKartyProTymy(5, 2, 2, 15, 15, 3, 15))
# db.session.add(CisKartyProTymy(5, 3, 1, 20, 12, 3, 15))
# db.session.add(CisKartyProTymy(5, 3, 2, 15, 15, 3, 15))
# db.session.add(CisKartyProTymy(5, 4, 1, 10, 15, 3, 20))
# db.session.add(CisKartyProTymy(5, 4, 2, 5, 20, 3, 20))
# db.session.add(CisKartyProTymy(5, 4, 3, 2, 30, 3, 20))
# db.session.add(CisKartyProTymy(5, 5, 1, 10, 15, 3, 20))
# db.session.add(CisKartyProTymy(5, 5, 2, 5, 20, 3, 20))
# db.session.add(CisKartyProTymy(5, 5, 3, 2, 30, 3, 20))
# # -
# db.session.add(CisKartyProTymy(5, 6, 1, 18, 0, 0, 0))
# db.session.add(CisKartyProTymy(5, 7, 1, 18, 0, 0, 0))
# db.session.add(CisKartyProTymy(5, 8, 1, 99, 20, 2, 0))
# db.session.add(CisKartyProTymy(5, 8, 2, 99, 40, 3, 0))
# db.session.add(CisKartyProTymy(5, 11, 1, 6, 0, 0, 0))
# db.session.add(CisKartyProTymy(5, 12, 1, 99, 0, 0, 0))
# # db.session.add(CisKartyProTymy(5, 12, 1, 1, 0, 0, 0))
# db.session.add(CisKartyProTymy(5, 13, 1, 3, 0, 0, 0))
# # pocet = 6
# db.session.add(CisKartyProTymy(6, 1, 1, 6, 15, 6, 30))
# db.session.add(CisKartyProTymy(6, 1, 2, 6, 30, 6, 30))
# db.session.add(CisKartyProTymy(6, 1, 3, 2, 45, 6, 30))
# db.session.add(CisKartyProTymy(6, 2, 1, 24, 12, 3, 15))
# db.session.add(CisKartyProTymy(6, 2, 2, 18, 15, 3, 15))
# db.session.add(CisKartyProTymy(6, 3, 1, 24, 12, 3, 15))
# db.session.add(CisKartyProTymy(6, 3, 2, 18, 15, 3, 15))
# db.session.add(CisKartyProTymy(6, 4, 1, 12, 15, 3, 20))
# db.session.add(CisKartyProTymy(6, 4, 1, 12, 15, 3, 20))
# db.session.add(CisKartyProTymy(6, 4, 3, 2, 30, 3, 20))
# db.session.add(CisKartyProTymy(6, 5, 1, 12, 15, 3, 20))
# db.session.add(CisKartyProTymy(6, 5, 2, 6, 20, 3, 20))
# db.session.add(CisKartyProTymy(6, 5, 3, 2, 30, 3, 20))
# # -
# db.session.add(CisKartyProTymy(6, 6, 1, 18, 0, 0, 0))
# db.session.add(CisKartyProTymy(6, 7, 1, 18, 0, 0, 0))
# db.session.add(CisKartyProTymy(6, 8, 1, 99, 20, 2, 0))
# db.session.add(CisKartyProTymy(6, 8, 2, 99, 40, 3, 0))
# db.session.add(CisKartyProTymy(6, 11, 1, 7, 0, 0, 0))
# db.session.add(CisKartyProTymy(6, 12, 1, 99, 0, 0, 0))
# # db.session.add(CisKartyProTymy(6, 12, 1, 1, 0, 0, 0))
# db.session.add(CisKartyProTymy(6, 13, 1, 4, 0, 0, 0))
# ----

# commit the changes
db.session.commit()
