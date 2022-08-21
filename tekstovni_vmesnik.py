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
    ime = input('Ime predmeta>')
    st_kolokvijev = input('Število kolokvijev')
    st_ocen = input('Število ocen')
    stanje.dodaj_predmet(ime, st_kolokvijev, st_ocen)

def odstrani_predmet():
    pass

def dodaj_rezultat():
    ime_predmeta = input('Kateremu predmetu želite dodati rezultat?')
    opis = input('Opis rezultata>')
    kolicina = input('Vpišite rezultat')
    stanje.dodaj_rezultat(ime_predmeta, opis, kolicina)

def odstrani_rezultat():
    ime_predmeta = input('Kateremu predmetu želite odstraniti rezultat?')
    opis = input('Vpišite opis rezultata, ki ga želite izbrisati.')
    stanje.odstrani_rezultat(ime_predmeta, opis)

def vpisi_oceno():
    ime_predmeta = input('Kateremu predmetu želite vpisati oceno?')
    opis = input('Vpišite opis ocene.')
    kolicina = input('Vpišite oceno.')
    stanje.vpisi_oceno(ime_predmeta, opis, kolicina)

def izbrisi_oceno():
    ime_predmeta = input('Kateremu predmetu želite izbrisati oceno?')
    opis = input('Vpišite opis ocene, ki jo želite izbrisati.')
    stanje.izbrisi_oceno(ime_predmeta, opis)

def nastavi_stevilo_kolokvijev():
    ime_predmeta = input('Kateremu predmetu želite nastaviti število kolokvijev?')
    st = int(input('Vpišite število kolokvijev.'))
    stanje.nastavi_st_kolokvijev(ime_predmeta, st)

def izpis_povprecja_ocen():
    povprecje_ocen = stanje.aktualno_solsko_leto.povprecje()
    print(f"Trenutno povprečje ocen: {povprecje_ocen}")

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
