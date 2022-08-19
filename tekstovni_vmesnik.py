import model

DATOTEKA_S_STANJEM = "stanje.json"
stanje = model.Stanje.preberi_iz_datoteke(DATOTEKA_S_STANJEM)

def izberi_aktualno_solsko_leto():
    pass

def dodaj_solsko_leto():
    ime = input('Ime šolskega leta>')
    stanje.dodaj_solsko_leto(ime)

def izbrisi_solsko_leto():
    ime = input('Katero šolsko leto želite izbrisati?')
    stanje.izbrisi_solsko_leto(ime)

def dodaj_predmet():
    pass

def odstrani_predmet():
    pass

def dodaj_rezultat():
    ime_predmeta = input('Kateremu predmetu želite dodati rezultat?')
    opis = input('Opis rezultata>')
    kolicina = input('Vnesite rezultat')
    stanje.dodaj_rezultat(ime_predmeta, opis, kolicina)

def odstrani_rezultat():
    pass

def vpisi_oceno():
    pass

def izbrisi_oceno():
    pass

def nastavi_stevilo_kolokvijev():
    pass

def izpis_povprecja_ocen():
    pass

def izpis_povprecja_rezultatov():
    pass

def koliko_potrebujem():
    pass
def izbira_moznosti():
    pass

def pozdrav():
    print("Pozdravljeni v redovalnici! Izberite, kaj bi radi storili!")

def izbira():
    pass

def tekstovni_vmesnik():
    pozdrav()
    while True:
        izbira()

tekstovni_vmesnik()
