# MRS
Projekti za predmet Metodologija razvoja softvera

#Tema projekta P1 - Vođenje magacina

# Kratak opis:
Omogućiti vođenje proizvoda unutar magacina po halama. Hale mogu biti za čuvanje proizvoda
na sobnoj temperaturi (19°C do 25°C), rashladne hale (1°C do 18°C), hale za zamrzavanje (
-10°C do 0°C). Svaka hala ima i podatak o raspoloživosti (ukupan broj mesta i broj zauzetih
mesta). Magacin može imati proizvoljan broj hala (hale istog ili različitog tipa). U hale se
smeštaju proizvodi. Svaki proizvod je opisan nazivom, rokom upotrebe, temperaturom na kojoj
se čuva. Prilikom smeštanja proizvoda, mora se odabrati hala koja odgovara temperaturi
čuvanja tog proizvoda i proveriti da li hala ima dovoljno mesta za smeštanje. Korisnik unosi
proizvod koji želi da smesti u halu i količinu tog proizvoda. Sami proizvodi se posebno dodaju (u
bazu ili tekstualnu datoteku). Proizvodi se mogu i uklanjati iz hale tako što se odabere prvo hala,
a zatim i proizvod i njegova količina za uklanjanje. Prilikom izmena hala, čuvati promene u bazi
ili datoteci.
Funkcionalni zahtevi:
● Kreiranje, brisanje i izmena proizvoda (u bazi ili tekstualnoj datoteci).
● Kreiranje i dodavanje novih hala. Realizovati izborom tipa hale.
● Brisanje hala iz magacina. Brisati se može samo hala koja postoji u magacinu.
● Dodavanje proizvoda u odgovarajuće hale. Prilikom dodavanja se bira proizvod iz svih
proizvoda (učitanih iz baze ili datoteke), potom se bira količina proizvoda koja se dodaje
u halu, pri čemu se korisniku zabranjuje da doda proizvod u neodgovarajuću halu. Ako
nema dovoljno mesta za smeštanje specificiranje količine proizvoda, zabraniti
dodavanje, i od korisnika tražiti unos manje ili jednake količine proizvoda.
● Uklanjanje proizvoda iz hale. Neophodno je prvo odabrati halu u magacinu, potom
odabrati proizvod, i njegovu količinu. Iz hale se ne može ukloniti nepostojeći proizvod,
kao i količina koja je veća od one koja se lageruje.
● Prikaz proizvoda u halama. Omogućiti tabelarni prikaz proizvoda u hali. U tabeli prikazati
naziv proizvoda, količinu koja se čuva, i datum isteka roka tog proizvoda. Ukoliko je halu
dodato više istih proizvoda sa različitim rokom isteka, potrebno ih je zasebno prikazati.
● Prikaz stanja hale (raspoloživo mesta i ukupno mesta).
Dodatni funkcionalni zahtevi:
● Omogućiti sortiranja proizvoda u halama po datumu isteka roka, nazivu ili prisutnoj
količini.
● Definisati i rok čuvanja proizvoda u hali. Ovaj rok može biti manji ili jednak isteku roka
samog proizvoda. Rok čuvanja se definiše pri dodavanju proizvoda u halu.
● Omogućiti pretragu i filtriranje proizvoda spram naziva. Ovu funkcionalnost ubaciti i
prilikom dodavanja proizvoda u halu i prilikom prikaza proizvoda u hali.
● Omogućiti sumarni prikaz proizvoda (u svim halama).