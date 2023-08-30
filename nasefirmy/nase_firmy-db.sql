-- Verze MySQL: 5.1.66

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Databáze: `nase_firmy`
--

-- --------------------------------------------------------

--
-- Struktura tabulky `nf_cis_typy_karet`
--

DROP TABLE IF EXISTS `nf_cis_typy_karet`;
CREATE TABLE IF NOT EXISTS `nf_cis_typy_karet` (
  `typk_id` smallint(6) NOT NULL,
  `kod` varchar(3) NOT NULL,
  `efekt` varchar(2) NOT NULL, -- efekt: AH = akce hlavni, AV = akce vedlejsi, EH = efekt po celou hru, EK = efekt pro kolo
  `losovat` bit NOT NULL DEFAULT 0, -- 1 = tento typ karty se bude losovat, pocet vylosovanych ks dle tabulky nf_cis_karty_pro_tymy
  `nazev` varchar(20) NOT NULL,
  `popis` varchar(50) NOT NULL,
  `ikona` varchar(20) NOT NULL,
  PRIMARY KEY (`typk_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Data pro tabulku `nf_cis_typy_karet`
--

INSERT INTO `nf_cis_typy_karet` (`typk_id`, `kod`, `efekt`, `losovat`, `nazev`, `popis`, `ikona`) VALUES
(1, 'VVJ', 'AH', 0, 'vývoj', 'vývoj, věda, výzkum', 'iko_vyvoj.png'),
(2, 'VRB', 'AH', 0, 'výroba', 'výroba', 'iko_vyroba.png'),
(3, 'OBD', 'AH', 0, 'obchod', 'obchod, distribuce', 'iko_obchod.png'),
(4, 'SRV', 'AH', 0, 'servis', 'servis, služby', 'iko_servis.png'),
(5, 'MKT', 'AH', 0, 'marketing', 'marketing, propagace', 'iko_marketing.png'),
(6, 'POJ', 'AH', 0, 'pojištění', 'pojištění proti negativnímu efektu', 'iko_pojisteni.png'),
(7, 'EXP', 'AH', 0, 'expert', 'využití služeb experta', 'iko_expert.png'),
(8, 'PUJ', 'AV', 0, 'půjčka', 'půjčka', 'iko_pujcka.png'),
(11, 'VYZ', 'EH', 1, 'výzva', 'výzva, úkol na celou hru', 'iko_ost-vyzva.png'),
(12, 'P&R', 'EK', 1, 'P & R', 'příležitost / riziko, po dobu jednoho kola', 'iko_ost-par.png'),
(13, 'HRZ', 'EH', 1, 'hrozba', 'hrozba postihu po celou hru', 'iko_ost-hrozba.png');

-- --------------------------------------------------------

--
-- Struktura tabulky `nf_cis_karty`
--

DROP TABLE IF EXISTS `nf_cis_karty`;
CREATE TABLE IF NOT EXISTS `nf_cis_karty` (
  `karta_id` smallint(6) NOT NULL,
  `typk_id` smallint(6) NOT NULL,
  `uroven` tinyint NOT NULL,   -- cenova uroven nakupu karty (1 - 3) 
  `nazev` varchar(2) NOT NULL,
  `popis` varchar(20) NOT NULL,
  `castka` smallint(6) NOT NULL, -- +/- zisk/ztrata
  `symbol_obr` varchar(255) NOT NULL, -- popisny obrazek - bud nazev souboru nebo pripadne zmenit na obrazek
  `cil` smallint(6) NOT NULL, -- zda pro 1 nebo se deli (99)
  `vyhodnoceni` text NOT NULL, -- vyhodnocujici SQL
  PRIMARY KEY (`karta_id`), 
  KEY `nf_cis_karty_typy_fk` (`typk_id`) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE nf_cis_karty 
    ADD CONSTRAINT nf_cis_karty_typy_fk FOREIGN KEY 
    ( 
     typk_id
    ) 
    REFERENCES nf_cis_typy_karet 
    ( 
     typk_id
    ) 
;

--
-- Data pro tabulku `nf_cis_karty`
--

-- DELETE FROM nf_cis_karty
INSERT INTO `nf_cis_karty` (`karta_id`, `typk_id`, `uroven`, `nazev`, `popis`, `castka`, `symbol_obr`, `cil`, `vyhodnoceni`) VALUES
-- Karty akci
(1, 1, 1, 'vývoj', 'vývoj, věda, výzkum', 15, 'sym_01_VVJ-01.png', 0, ''), 
(2, 1, 2, 'vývoj', 'vývoj, věda, výzkum', 30, 'sym_02_VVJ-02.png', 0, ''), 
(3, 1, 3, 'vývoj', 'vývoj, věda, výzkum', 45, 'sym_03_VVJ-03.png', 0, ''), 
(4, 2, 1, 'výroba', 'výroba', 12, 'sym_04_VRB-04.png', 0, ''), 
(5, 2, 2, 'výroba', 'výroba', 15, 'sym_05_VRB-05.png', 0, ''), 
(6, 2, 3, 'výroba', 'výroba', 20, 'sym_06_VRB-06.png', 0, ''), 
(7, 3, 1, 'obchod', 'obchod, distribuce', 12, 'sym_07_OBD-07.png', 0, ''), 
(8, 3, 2, 'obchod', 'obchod, distribuce', 15, 'sym_08_OBD-08.png', 0, ''), 
(9, 3, 3, 'obchod', 'obchod, distribuce', 20, 'sym_09_OBD-09.png', 0, ''), 
(10, 4, 1, 'servis', 'servis, služby', 15, 'sym_10_SRV-10.png', 0, ''), 
(11, 4, 2, 'servis', 'servis, služby', 20, 'sym_11_SRV-11.png', 0, ''), 
(12, 4, 3, 'servis', 'servis, služby', 30, 'sym_12_SRV-12.png', 0, ''), 
(13, 5, 1, 'marketing', 'marketing, propagace', 15, 'sym_13_MKT-13.png', 0, ''), 
(14, 5, 2, 'marketing', 'marketing, propagace', 20, 'sym_14_MKT-14.png', 0, ''), 
(15, 5, 3, 'marketing', 'marketing, propagace', 30, 'sym_15_MKT-15.png', 0, ''), 
(16, 6, 1, 'pojištění', 'pojištění proti negativnímu efektu', 0, 'sym_16_POJ-16.png', 0, ''), 
(17, 7, 1, 'expert', 'využití služeb experta', 0, 'sym_17_EXP-17.png', 0, ''), 
(18, 8, 1, 'půjčka', 'půjčka', 0, 'sym_18_PUJ-18.png', 0, ''), 

-- Vyzvy
(31, 11, 1, 'Nejlepší vývojový tým', 'Nejvíce investic do vývoje, min. 2', 30, 'sym_31_VYZ-31.png', 1, ''), 
(32, 11, 1, 'Tahoun výroby', 'Nejvíce investic do výroby, min. 2', 30, 'sym_32_VYZ-32.png', 1, ''), 
(33, 11, 1, 'Nejlepší obchodník', 'Nejvíce investic do obchodu, min. 2', 30, 'sym_33_VYZ-33.png', 1, ''), 
(34, 11, 1, 'Nejlepší dodavatel', 'Nejvíce dvojic výroba + obchod, min. 2', 30, 'sym_34_VYZ-34.png', 1, ''), 
(35, 11, 1, 'Nejkvalitnější servis', 'Nejvíce investic do servisu, min. 2', 30, 'sym_35_VYZ-35.png', 1, ''), 
(36, 11, 1, 'Nejlepší kampaň marketingu', 'Nejvíce investic do marketingu, min. 2', 30, 'sym_36_VYZ-36.png', 1, ''), 
(37, 11, 1, 'Prosperující firma', 'Nejvyšší celkový příjem', 30, 'sym_37_VYZ-37.png', 1, ''), 
(38, 11, 1, 'Nejlepší investiční krok', 'Nejvyšší kvartálový příjem', 30, 'sym_38_VYZ-38.png', 1, ''), 
(39, 11, 1, 'Kvalitní zázemí', 'Nejvíce investic do vývoje + servisu + marketingu (min. 4)', 30, 'sym_39_VYZ-39.png', 1, ''), 
(40, 11, 1, 'Zacíleno na zákazníka', 'Nejvíce investic do vývoje + marketingu (min. 4)', 30, 'sym_40_VYZ-40.png', 1, ''), 
(41, 11, 1, 'Důraz na inovace', 'Nejvíce investic do vývoje + servisu (min. 4)', 30, 'sym_41_VYZ-41.png', 1, ''), 
(42, 11, 1, 'Propagace služeb', 'Nejvíce investic do servisu + marketingu (min. 4)', 30, 'sym_42_VYZ-42.png', 1, ''), 

-- P & R
(50, 12, 1, 'Inovativní přístup', 'Nejvíce investic do vývoje', 30, 'sym_50_P&R-50.png', 99, ''), 
(51, 12, 1, 'Popularizace vývoje', 'Nejvíce dvojic vývoj + marketing (při shodě rozhoduje marketing)', 30, 'sym_51_P&R-51.png', 99, ''), 
(52, 12, 1, 'Podpora výrobců', 'Nejvíce investic do výroby', 30, 'sym_52_P&R-52.png', 99, ''), 
(53, 12, 1, 'Oživení obchodu', 'Nejvíce investic do obchodu', 30, 'sym_53_P&R-53.png', 99, ''), 
(54, 12, 1, 'Kvalitní obchodní model', 'Nejvíce dvojic výroba + obchod (při shodě rozhoduje výroba)', 30, 'sym_54_P&R-54.png', 99, ''), 
(55, 12, 1, 'Nové obchodní příležitosti', 'Nejvíce dvojic výroba + obchod (při shodě rozhoduje marketing)', 30, 'sym_55_P&R-55.png', 99, ''), 
(56, 12, 1, 'Kvalitní zákaznická podpora', 'Nejvíce investic do servisu', 30, 'sym_56_P&R-56.png', 99, ''), 
(57, 12, 1, 'Univerzální prodejci', 'Nejvíce investic do marketingu', 30, 'sym_57_P&R-57.png', 99, ''), 
(58, 12, 1, 'Nedostatek nápadů', 'Nejméně investic do vývoje', -30, 'sym_58_P&R-58.png', 99, ''), 
(59, 12, 1, 'Nízká kvalita výroby', 'Nejméně investic do výroby', -30, 'sym_59_P&R-59.png', 99, ''), 
(60, 12, 1, 'Podomní prodejci', 'Nejméně investic do obchodu', -30, 'sym_60_P&R-60.png', 99, ''), 
(61, 12, 1, 'Nefunkční zákaznická linka', 'Nejméně investic do servisu', -30, 'sym_61_P&R-61.png', 99, ''), 
(62, 12, 1, 'Zmařená kampaň', 'Nejméně investic do marketingu', -30, 'sym_62_P&R-62.png', 99, ''), 
(63, 12, 1, 'Nevyužité investice', 'Nejnižší investice v tomto kvartálu', -30, 'sym_63_P&R-63.png', 99, ''), 
(64, 12, 1, 'Příprava úspor', 'Nejnižší investice v tomto kvartálu', 30, 'sym_64_P&R-64.png', 99, ''), 

-- Hrozby
(70, 13, 1, 'Nízká úroveň služeb zákazníkům', 'Nejméně investic do servisu', -20, 'sym_70_HRZ-70.png', 1, ''), 
(71, 13, 1, 'Nízká úroveň marketingu', 'Nejméně investic do marketingu', -20, 'sym_71_HRZ-71.png', 1, ''), 
(72, 13, 1, 'Firma bez zázemí', 'Nejméně investic do vývoje + servisu + marketingu', -20, 'sym_72_HRZ-72.png', 1, ''), 
(73, 13, 1, 'Nevyváženost investic', 'Největší počet oblastí s nejméně investicemi', -20, 'sym_73_HRZ-73.png', 1, ''), 
(74, 13, 1, 'Nízká efektivita vývoje', 'Nejméně investic do vývoje', -20, 'sym_74_HRZ-74.png', 1, ''), 
(75, 13, 1, 'Slabá optimalizace výroby', 'Nejméně investic do výroby', -20, 'sym_75_HRZ-75.png', 1, ''), 
(76, 13, 1, 'Nízká úroveň obchodu', 'Nejméně investic do obchodu', -20, 'sym_76_HRZ-76.png', 1, ''), 
(77, 13, 1, 'Nekoordinovaná výroba a obchod', 'Nejmenší počet dvojic výroba + obchod', -20, 'sym_77_HRZ-77.png', 1, '') 

/*
1, 12, Nejlepší vývojový tým, Nejvíce investic do vývoje, min. 2, 30, 99, 
	SELECT ZKK.tym_id, ZKS.poc_k FROM ziskane_karty ZKK left join (SELECT tym_id, typk_id, count(CAS) where id hry = [XX] AND typk_id = 1 GROUP BY tym_id) ZKS
	ON ZKK.hra_id = ZKS.hra_id AND ZKK.tym_id = ZKS.tym_id AND ZKK.typk_id = ZKS.typk_id
	WHERE ZKK.typk_id = 1 AND ZKS.poc_k > 1
 -> při aplikaci selectu dané karty se provede zjištění; pakliže počet týmů > 0 a <= poč. cílů, pak se provede efekt 
	-> pokud se jedná o typ 11, pak se zjistí, zda poslední tým, který ji má (opět z tab. braní karet) je stejný
		-> není-li, zapíše se to týmu + se připočte zisk; je-li, jen se uloží, že ji i toto kolo má, ale bez započtení zisku
	-> uloží záznam + zisky / postihy do tabulka braní karet

-> u výzev udělat vyhodnocující dotaz tak, že když výsledkem je tým, který kartu má, pak je zisk 0, jinak 30
*/

-- --------------------------------------------------------

--
-- Struktura tabulky `nf_cis_karty_pro_tymy`
--

DROP TABLE IF EXISTS `nf_cis_karty_pro_tymy`;
CREATE TABLE IF NOT EXISTS `nf_cis_karty_pro_tymy` (
  `poc_tymu` smallint(6) NOT NULL, -- pro jaky pocet tymu to plati
  `typk_id` smallint(6) NOT NULL,  -- typ karty, jaky se distribuuje
  `uroven` tinyint NOT NULL,   -- cenova uroven nakupu karty (1 - 3) 
--nepouzito  `karta_id` smallint(6) NOT NULL,  -- karta_id z tabulky nf_cis_karty, kde uroven lze resit dle ceny (vyuzije se pri plneni daneho poctu karet pro hru)
  `pocet` smallint(6) NOT NULL,    -- pocet pripravovanych karet one urovne, 99 = vsechny karty
  `cena` smallint(6) NOT NULL,     -- nakupni cena karty
  `naklady` smallint(6) NOT NULL,  -- poplatek za udrzbu karty
  `prijem` smallint(6) NOT NULL,     -- zisk z dane karty 
  PRIMARY KEY (`poc_tymu`, `typk_id`, `uroven`), 
  KEY `nf_cis_karty_tymy_typy_fk` (`typk_id`) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE nf_cis_karty_pro_tymy 
    ADD CONSTRAINT nf_cis_karty_tymy_typy_fk FOREIGN KEY 
    ( 
     typk_id
    ) 
    REFERENCES nf_cis_typy_karet 
    ( 
     typk_id
    ) 
;

--
-- Data pro tabulku `nf_cis_karty_pro_tymy`
--

INSERT INTO `nf_cis_karty_pro_tymy` (`poc_tymu`, `typk_id`, `uroven`, `pocet`, `cena`, `naklady`, `prijem`) VALUES
(2, 1, 1, 2, 15, 6, 30),
(2, 1, 2, 3, 30, 6, 30),
(2, 1, 3, 1, 45, 6, 30),
(2, 2, 1, 7, 12, 3, 15),
(2, 2, 2, 7, 15, 3, 15),
(2, 3, 1, 7, 12, 3, 15),
(2, 3, 2, 7, 15, 3, 15),
(2, 4, 1, 4, 15, 3, 20),
(2, 4, 2, 3, 20, 3, 20),
(2, 4, 3, 1, 30, 3, 20),
(2, 5, 1, 4, 15, 3, 20),
(2, 5, 2, 3, 20, 3, 20),
(2, 5, 3, 1, 30, 3, 20),

(3, 1, 1, 3, 15, 6, 30),
(3, 1, 2, 3, 30, 6, 30),
(3, 1, 3, 2, 45, 6, 30),
(3, 2, 1, 12, 12, 3, 15),
(3, 2, 2, 9, 15, 3, 15),
(3, 3, 1, 12, 12, 3, 15),
(3, 3, 2, 9, 15, 3, 15),
(3, 4, 1, 6, 15, 3, 20),
(3, 4, 2, 3, 20, 3, 20),
(3, 4, 3, 2, 30, 3, 20),
(3, 5, 1, 6, 15, 3, 20),
(3, 5, 2, 3, 20, 3, 20),
(3, 5, 3, 2, 30, 3, 20),

(4, 1, 1, 4, 15, 6, 30),
(4, 1, 2, 4, 30, 6, 30),
(4, 1, 3, 2, 45, 6, 30),
(4, 2, 1, 16, 12, 3, 15),
(4, 2, 2, 12, 15, 3, 15),
(4, 3, 1, 16, 12, 3, 15),
(4, 3, 2, 12, 15, 3, 15),
(4, 4, 1, 8, 15, 3, 20),
(4, 4, 2, 4, 20, 3, 20),
(4, 4, 3, 2, 30, 3, 20),
(4, 5, 1, 8, 15, 3, 20),
(4, 5, 2, 4, 20, 3, 20),
(4, 5, 3, 2, 30, 3, 20),

(5, 1, 1, 5, 15, 6, 30),
(5, 1, 2, 5, 30, 6, 30),
(5, 1, 3, 2, 45, 6, 30),
(5, 2, 1, 20, 12, 3, 15),
(5, 2, 2, 15, 15, 3, 15),
(5, 3, 1, 20, 12, 3, 15),
(5, 3, 2, 15, 15, 3, 15),
(5, 4, 1, 10, 15, 3, 20),
(5, 4, 2, 5, 20, 3, 20),
(5, 4, 3, 2, 30, 3, 20),
(5, 5, 1, 10, 15, 3, 20),
(5, 5, 2, 5, 20, 3, 20),
(5, 5, 3, 2, 30, 3, 20),

(6, 1, 1, 6, 15, 6, 30),
(6, 1, 2, 6, 30, 6, 30),
(6, 1, 3, 2, 45, 6, 30),
(6, 2, 1, 24, 12, 3, 15),
(6, 2, 2, 18, 15, 3, 15),
(6, 3, 1, 24, 12, 3, 15),
(6, 3, 2, 18, 15, 3, 15),
(6, 4, 1, 12, 15, 3, 20),
(6, 4, 2, 6, 20, 3, 20),
(6, 4, 3, 2, 30, 3, 20),
(6, 5, 1, 12, 15, 3, 20),
(6, 5, 2, 6, 20, 3, 20),
(6, 5, 3, 2, 30, 3, 20), 

(2, 6, 1, 18, 0, 0, 0),
(2, 7, 1, 18, 0, 0, 0),
(2, 11, 1, 3, 0, 0, 0),
(2, 12, 1, 99, 0, 0, 0), 
(2, 13, 1, 2, 0, 0, 0),

(3, 6, 1, 18, 0, 0, 0),
(3, 7, 1, 18, 0, 0, 0),
(3, 11, 1, 4, 0, 0, 0),
(3, 12, 1, 99, 0, 0, 0), 
(3, 13, 1, 2, 0, 0, 0),

(4, 6, 1, 18, 0, 0, 0),
(4, 7, 1, 18, 0, 0, 0),
(4, 11, 1, 5, 0, 0, 0),
(4, 12, 1, 99, 0, 0, 0), 
(4, 13, 1, 3, 0, 0, 0),

(5, 6, 1, 18, 0, 0, 0),
(5, 7, 1, 18, 0, 0, 0),
(5, 11, 1, 6, 0, 0, 0),
(5, 12, 1, 99, 0, 0, 0), 
(5, 13, 1, 3, 0, 0, 0),

(6, 6, 1, 18, 0, 0, 0),
(6, 7, 1, 18, 0, 0, 0),
(6, 11, 1, 7, 0, 0, 0),
(6, 12, 1, 99, 0, 0, 0), 
(6, 13, 1, 4, 0, 0, 0);

/*
Počet hráčů \ karet (poč. dle cenové úrovně)	Výzkum a vývoj	Výroba	Obchod	Servis	Marketing
2	6 (2+3+1)	14 (7+7)	14 (7+7)	8 (4+3+1)	8 (4+3+1)
3	8 (3+3+2)	21 (12+9)	21 (12+9)	11 (6+3+2)	11 (6+3+2)
4	10 (4+4+2)	28 (16+12)	28 (16+12)	14 (8+4+2)	14 (8+4+2)
5	12 (5+5+2)	35 (20+15)	35 (20+15)	17 (10+5+2)	17 (10+5+2)
6	14 (6+6+2)	42 (24+18)	42 (24+18)	20 (12+6+2)	20 (12+6+2)

Karta / Ceny
1 VVJ 15, 30, 45  
2 VRB 12, 15 
3 OBD 12, 15 
4 SRV 15, 20, 30 
5 MKT 15, 20, 30
*/

-- --------------------------------------------------------

--
-- Struktura tabulky `nf_cis_mista`
--
-- (jelikoz je pravdepodobne, ze se budou mista opakovat, je vhodne je evidovat a pro hru mit pouze misto_id)
--

DROP TABLE IF EXISTS `nf_cis_mista`;
CREATE TABLE IF NOT EXISTS `nf_cis_mista` (
  -- mozna automaticky?: `misto_id` int(6) NOT NULL AUTO_INCREMENT,
  `misto_id` int(6) NOT NULL,
  `nazev` varchar(20) NOT NULL,
  `ulice` varchar(30) NOT NULL,
  `obec` varchar(20) NOT NULL,
  `psc` varchar(5) NOT NULL,
  `souradnice` varchar(100) NOT NULL,
  PRIMARY KEY (`misto_id`) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8; -- AUTO_INCREMENT=0;

-- --------------------------------------------------------

--
-- Struktura tabulky `nf_hry`
--
-- (nastaveni konkretni hry na urcitem miste)
--

DROP TABLE IF EXISTS `nf_hry`;
CREATE TABLE IF NOT EXISTS `nf_hry` (
  -- mozna automaticky?: `hra_id` int(6) NOT NULL AUTO_INCREMENT,
  `hra_id` int(6) NOT NULL,
  `nazev` varchar(100) NOT NULL,
  `dat_hrani` datetime NOT NULL,
  `misto_id` int(6) NOT NULL,
  `popis` text,
  `klic` varchar(20) NOT NULL, -- klic pro pripojeni ke hre (vygeneruje se a pote zaci zadaji ci naskenuji)
  `majetek` float(10, 2) NOT NULL DEFAULT 100, -- defaultni majetek tymu po zalozeni             
  `karty_za_kolo` tinyint DEFAULT 2,
  `poc_tymu` tinyint NOT NULL,
  `poc_kol` tinyint NOT NULL,
  `akt_kolo` tinyint NOT NULL,
  `stav_hry` varchar(1) NOT NULL, -- rotace v kolech [S - start, vylosovani, cekani na spusteni odpoctu, A - aktivni, hraje se [, P = pauza, preruseni], K = konec kola, vyhodnoceni MKT zprav,] R = hodnoceni robota na zaver, Z = zaver hry a zobrazeni vyhodnoceni
  PRIMARY KEY (`hra_id`), 
  KEY `nf_hry_mista_fk` (`misto_id`) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8; -- AUTO_INCREMENT=0;

ALTER TABLE nf_hry 
    ADD CONSTRAINT nf_hry_mista_fk FOREIGN KEY 
    ( 
     misto_id
    ) 
    REFERENCES nf_cis_mista 
    ( 
     misto_id
    ) 
;

--
-- Vypisuji data pro tabulku `nf_hry`
--


-- --------------------------------------------------------

--
-- Struktura tabulky `nf_cis_tymy`
--
-- (jelikoz tymy mohou hrat opakovane, je mozna vhodne je evidovat)
--

DROP TABLE IF EXISTS `nf_cis_tymy`;
CREATE TABLE IF NOT EXISTS `nf_cis_tymy` (
  -- mozna automaticky?: `tym_id` int(6) NOT NULL AUTO_INCREMENT,
  `tym_id` int(6) NOT NULL,
  `nazev` varchar(100) NOT NULL,
  `dat_registrace` datetime NOT NULL,
  `popis` text,
  `stav` varchar(1) NOT NULL DEFAULT 'A', -- A = aktivni, N = neaktivni, X = zruseno 
  PRIMARY KEY (`tym_id`) 
)  ENGINE=InnoDB DEFAULT CHARSET=utf8; -- AUTO_INCREMENT=0;


-- --------------------------------------------------------

--
-- Struktura tabulky `nf_hry_tymy`
--
-- (zaznam tymu v aktualni hre)
--

DROP TABLE IF EXISTS `nf_hry_tymy`;
CREATE TABLE IF NOT EXISTS `nf_hry_tymy` (
  `hra_id` int(6) NOT NULL, -- aktualni hra
  `tym_id` int(6) NOT NULL, -- zucastneny tym
  `klic` varchar(20) NOT NULL, -- klic pro pripojeni ke hre (vygeneruje se a pote zaci zadaji ci naskenuji)
  `nazev_firmy` varchar(20) NOT NULL, -- v kazde hre muze mit tym jiny nazev firmy, bude-li chtit
  `logo` varchar(100), -- nazev souboru s logem na serveru, pripadne primo ulozeny obrazek 
  `majetek` float(10, 2) NOT NULL DEFAULT 100, -- aktualni majetek tymu             
  PRIMARY KEY (`hra_id`, `tym_id`), 
  KEY `nf_hry_tymy_a_hry_fk` (`hra_id`), 
  KEY `nf_hry_tymy_a_tymy_fk` (`tym_id`) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE nf_hry_tymy 
    ADD CONSTRAINT nf_hry_tymy_a_hry_fk FOREIGN KEY 
    ( 
     hra_id
    ) 
    REFERENCES nf_hry
    ( 
     hra_id
    ) 
;
ALTER TABLE nf_hry_tymy 
    ADD CONSTRAINT nf_hry_tymy_a_tymy_fk FOREIGN KEY 
    ( 
     tym_id
    ) 
    REFERENCES nf_cis_tymy
    ( 
     tym_id
    ) 
;


-- --------------------------------------------------------

--
-- Struktura tabulky `nf_hry_tymy_hraci`
--
-- (zaznamy clena tymu ve hre)
--

DROP TABLE IF EXISTS `nf_hry_tymy_hraci`;
CREATE TABLE IF NOT EXISTS `nf_hry_tymy_hraci` (
  `hra_id` int(6) NOT NULL, -- aktualni hra
  `tym_id` int(6) NOT NULL, -- tym, pod ktery patri
  `role` varchar(3) NOT NULL, -- role hrace (bud vypsáno, nebo to bude pres tabulku a id: 
  -- RED, OBD, MKT, VVJ, VRB, ROB = reditel + obchodnik v jednom (4 zaci v tymu), ROM = reditel + obchodnik + marketing (3 zaci v tymu)
  -- podle teto role se bude umoznovat pristup k jednotlivym funkcim 
  `jmeno` varchar(20), -- lze zadat jmeno hrace, ktere se pak muze zobrazovat ve hre; mozna v budoucnu tabulka hracu a zde hrac_id 
  PRIMARY KEY (`hra_id`, `tym_id`), 
  KEY `nf_hry_tymy_hraci_a_hry_fk` (`hra_id`), 
  KEY `nf_hry_tymy_hraci_a_tymy_fk` (`tym_id`) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE nf_hry_tymy_hraci 
    ADD CONSTRAINT nf_hry_tymy_hraci_a_hry_fk FOREIGN KEY 
    ( 
     hra_id
    ) 
    REFERENCES nf_hry
    ( 
     hra_id
    ) 
;
ALTER TABLE nf_hry_tymy_hraci 
    ADD CONSTRAINT nf_hry_tymy_hraci_a_tymy_fk FOREIGN KEY 
    ( 
     tym_id
    ) 
    REFERENCES nf_cis_tymy
    ( 
     tym_id
    ) 
;

-- --------------------------------------------------------
--
-- Struktura tabulky `nf_hry_karty`
--
-- (tabulka s prehledem karet vylosovanych pro hru na zaklade poctu tymu dle tabulky nf_cis_karty_pro_tymy)
--

DROP TABLE IF EXISTS `nf_hry_karty`;
CREATE TABLE IF NOT EXISTS `nf_hry_karty` (
  `karta_hry_id` int(6) NOT NULL AUTO_INCREMENT,
  `hra_id` int(6) NOT NULL,       -- aktualni hra
  `karta_id` smallint(6) NOT NULL,-- vylosovana karta
  `poradi` smallint(6) NOT NULL,  -- poradi karty ve hre (dulezite pro nakup beznych karet )
  `cena` smallint(6) NOT NULL,    -- nakupni cena karty
  `naklady` smallint(6) NOT NULL, -- poplatek za udrzbu karty
  `prijem` smallint(6) NOT NULL,  -- zisk z dane karty 
  `tym_id` int(6) NOT NULL DEFAULT 0, -- tym, kteremu karta patri
  PRIMARY KEY (`karta_hry_id`), 
  KEY `nf_hry_karty_a_hry_fk` (`hra_id`), 
  KEY `nf_hry_karty_a_karty_fk` (`karta_id`), 
  KEY `nf_hry_karty_a_tymy_fk` (`tym_id`) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=0;
/* puvodne klic: (`hra_id`, `karta_id`, `poradi`), */ 

ALTER TABLE nf_hry_karty 
    ADD CONSTRAINT nf_hry_karty_a_hry_fk FOREIGN KEY 
    ( 
     hra_id
    ) 
    REFERENCES nf_hry
    ( 
     hra_id
    ) 
;
ALTER TABLE nf_hry_karty 
    ADD CONSTRAINT nf_hry_karty_a_karty_fk FOREIGN KEY 
    ( 
     karta_id
    ) 
    REFERENCES nf_cis_karty
    ( 
     karta_id
    ) 
;
ALTER TABLE nf_hry_karty 
    ADD CONSTRAINT nf_hry_karty_a_tymy_fk FOREIGN KEY 
    ( 
     tym_id
    ) 
    REFERENCES nf_cis_tymy
    ( 
     tym_id
    ) 
;


--
-- Struktura tabulky `nf_hry_karty_historie`
--
-- (historie ziskavani karet - bud nakupem, nebo pridelenim v ramci vyhod ci postihu)
-- (otazka, zda napr. hrozba se bude ukladat kazde kolo ci nikoli)

DROP TABLE IF EXISTS `nf_hry_karty_historie`;
CREATE TABLE IF NOT EXISTS `nf_hry_karty_historie` (
  `karta_hry_id` int(6) NOT NULL, -- lze propojit na id hry, kartu, uroven atd
  `kolo` tinyint NOT NULL,
  `tym_id` int(6) NOT NULL,
  `dat_ziskani` datetime NOT NULL,
  PRIMARY KEY (`karta_hry_id`, `kolo`), 
  KEY `nf_hry_karty_historie_hry_karty_fk` (`karta_hry_id`), 
  KEY `nf_hry_karty_historie_tymy_fk` (`tym_id`) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*asi bude v historii financi  `castka` float(10, 2) NOT NULL DEFAULT 0, -- castka dle karty (cena za nakup u akci, odmena/postih u vyzvy, P&R, hrozby) */             
                       
ALTER TABLE nf_hry_karty_historie 
    ADD CONSTRAINT nf_hry_karty_historie_hry_karty_fk FOREIGN KEY 
    ( 
     karta_hry_id
    ) 
    REFERENCES nf_hry_karty
    ( 
     karta_hry_id
    ) 
;
ALTER TABLE nf_hry_karty_historie 
    ADD CONSTRAINT nf_hry_karty_historie_tymy_fk FOREIGN KEY 
    ( 
     tym_id
    ) 
    REFERENCES nf_cis_tymy
    ( 
     tym_id
    ) 
;


-- --------------------------------------------------------

--
-- Struktura tabulky `nf_hry_zpravy`
--
-- (ulozene zpravy marketingu)
--

DROP TABLE IF EXISTS `nf_hry_zpravy`;
CREATE TABLE IF NOT EXISTS `nf_hry_zpravy` (
  `zprava_id` int(6)  NOT NULL AUTO_INCREMENT,
  `hra_id` int(6) NOT NULL,       -- aktualni hra
  `tym_id` int(6) NOT NULL, -- tym, ktery zpravu napsal
  `kolo` tinyint NOT NULL, -- kolo, kdy byla zprava zverejnena
  `zprava` BLOB, -- text zpravy
  `obrazek` varchar(255), -- nazev souboru s fotografii / obrazkem ke zprave; pripadne zmenit na obrazek
  PRIMARY KEY (`zprava_id`), 
  KEY `nf_hry_zpravy_a_hry_fk` (`hra_id`), 
  KEY `nf_hry_zpravy_a_tymy_fk` (`tym_id`) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=0;

ALTER TABLE nf_hry_zpravy 
    ADD CONSTRAINT nf_hry_zpravy_a_hry_fk FOREIGN KEY 
    ( 
     hra_id
    ) 
    REFERENCES nf_hry
    ( 
     hra_id
    ) 
;
ALTER TABLE nf_hry_zpravy 
    ADD CONSTRAINT nf_hry_zpravy_a_tymy_fk FOREIGN KEY 
    ( 
     tym_id
    ) 
    REFERENCES nf_cis_tymy
    ( 
     tym_id
    ) 
;

-- --------------------------------------------------------

--
-- Struktura tabulky `nf_hry_tymy_prijmy`
--
-- (evidence prijmu tymu za jednotliva kola)
--

DROP TABLE IF EXISTS `nf_hry_tymy_prijmy`;
CREATE TABLE IF NOT EXISTS `nf_hry_tymy_prijmy` (
  `zaznam_id` int(6) NOT NULL AUTO_INCREMENT,
  `hra_id` int(6) NOT NULL,       -- aktualni hra
  `kolo` tinyint NOT NULL, -- kolo evidence prijmu
  `tym_id` int(6) NOT NULL, -- tym pro evidenci prijmu
  `castka` float(10, 2) NOT NULL DEFAULT 0, -- prijem tymu v danem kole             
  `poznamka` varchar(255), /* pripadna textova poznamka proc takovy prijem/vydaj*/
  PRIMARY KEY (`zaznam_id`), 
  KEY `nf_hry_tymy_prijmy_a_hry_fk` (`hra_id`),
  KEY `nf_hry_tymy_prijmy_a_tymy_fk` (`tym_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0 ;

ALTER TABLE nf_hry_tymy_prijmy 
    ADD CONSTRAINT nf_hry_tymy_prijmy_a_hry_fk FOREIGN KEY 
    ( 
     hra_id
    ) 
    REFERENCES nf_hry
    ( 
     hra_id
    ) 
;
ALTER TABLE nf_hry_tymy_prijmy 
    ADD CONSTRAINT nf_hry_tymy_prijmy_a_tymy_fk FOREIGN KEY 
    ( 
     tym_id
    ) 
    REFERENCES nf_cis_tymy
    ( 
     tym_id
    ) 
;



-- --------------------------------------------------------

--
-- Struktura tabulky `nf_hry_hlasovani`
--
-- (tabulka pro docasne ulozeni hlasovani o MKT zprave / jednotlivych casti robota)
--

DROP TABLE IF EXISTS `nf_tmp_hry_hlasovani`;
CREATE TABLE IF NOT EXISTS `nf_tmp_hry_hlasovani` (
  `hra_id` int(6) NOT NULL,   -- aktualni hra
  `tym_id` int(6) NOT NULL,   -- tym hlasujici
  `typ_hlasovani` varchar(2), -- rozliseni hlasovani MZ = MKT zprava, R1 = skelet / R2 = maska / R3 = dosky robota 
  `autor_id` int(6) NOT NULL, -- tym jako autor zpravy / robota
  `zprava_id` int(6),         -- propojeni na zpravu k hodnocení (u robota = NULL)
  `popis` varchar(255),       -- textova poznamka k zaznamu hlasovani - jaka cast se hodnoti 
  `hlas` bit NOT NULL DEFAULT 0, /* 1 = dane polozce pridelil tym hlas */
  PRIMARY KEY (`hra_id`, `tym_id`, `typ_hlasovani`, `autor_id`), 
  KEY `nf_tmp_hry_hlasovani_a_hry_fk` (`hra_id`),
  KEY `nf_tmp_hry_hlasovani_a_zpravy_fk` (`zprava_id`),
  KEY `nf_tmp_hry_hlasovani_a_tymy_fk` (`tym_id`),
  KEY `nf_tmp_hry_hlasovani_a_tymy_2_fk` (`autor_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0 ;

ALTER TABLE nf_tmp_hry_hlasovani 
    ADD CONSTRAINT nf_tmp_hry_hlasovani_a_hry_fk FOREIGN KEY 
    ( 
     hra_id
    ) 
    REFERENCES nf_hry
    ( 
     hra_id
    ) 
;
ALTER TABLE nf_tmp_hry_hlasovani 
    ADD CONSTRAINT nf_tmp_hry_hlasovani_a_zpravy_fk FOREIGN KEY 
    ( 
     zprava_id
    ) 
    REFERENCES nf_hry_zpravy
    ( 
     zprava_id
    ) 
;
ALTER TABLE nf_tmp_hry_hlasovani 
    ADD CONSTRAINT nf_tmp_hry_hlasovani_a_tymy_fk FOREIGN KEY 
    ( 
     tym_id
    ) 
    REFERENCES nf_cis_tymy
    ( 
     tym_id
    ) 
;
ALTER TABLE nf_tmp_hry_hlasovani 
    ADD CONSTRAINT nf_tmp_hry_hlasovani_a_tymy_2_fk FOREIGN KEY 
    ( 
     autor_id
    ) 
    REFERENCES nf_cis_tymy
    ( 
     tym_id
    ) 
;
