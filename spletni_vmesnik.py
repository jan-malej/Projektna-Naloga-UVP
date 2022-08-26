import bottle
import model
IME_DATOTEKE_S_STANJEM = 'stanje.json'
GESLO = 'geslo'

with open('skrivnost.txt') as dat:
    SIFRA = dat.read()

def preveri_int(vnos):
    """Preveri, če se vnos pretvori v int, ki je večji od 0"""
    try:
        ok = int(vnos)
        out = isinstance(ok, int)
    except ValueError:
        out = False
        return out
    return ok > 0

def preveri_float(niz):
    """Preveri, če se niz pretvori v float"""
    try:
        ok = float(niz)
        out = isinstance(ok, float)
    except ValueError:
        out = False
    return out

def je_neprazen_seznam(sez):
    """Preveri ali je seznam neprazen."""
    if sez == []:
        return False
    return True
def je_neprazen_niz(niz):
    """Preveri ali je niz neprazen"""
    if niz == '':
        return False
    return True

def ime_uporabnikove_datoteke(username):
    return f"Uporabniki/{username}.json"

def trenutni_uporabnik_stanje():
    username = bottle.request.get_cookie('uporabnisko_ime', secret=SIFRA)
    if username == None:
        bottle.redirect('/login/')
    ime_datoteke = ime_uporabnikove_datoteke(username)
    try:
        stanje = model.Stanje.preberi_iz_datoteke(ime_datoteke)
    except FileNotFoundError:
        stanje = model.Stanje()
        stanje.zapisi_v_datoteko(ime_datoteke)
    return stanje

def shrani(stanje):
    username = bottle.request.get_cookie('uporabnisko_ime', secret=SIFRA)
    ime_datoteke = ime_uporabnikove_datoteke(username)
    stanje.zapisi_v_datoteko(ime_datoteke)

@bottle.get("/Static/<file>")
def staticni_css(file):
    return bottle.static_file(file, root="Static")

@bottle.get('/login/')
def login():
    return bottle.template('log-in.html')

@bottle.get('/napaka_ob_prijavi/')
def napaka():
    return bottle.template('napaka-ob-prijavi.html')

@bottle.post('/login/')
def login_post():
    username = bottle.request.forms.getunicode('username')
    geslo = bottle.request.forms.getunicode('geslo')
    if je_neprazen_niz(username) and geslo == GESLO:
        bottle.response.set_cookie('uporabnisko_ime', username, path='/', secret=SIFRA)
        bottle.redirect('/')
    else:
        bottle.redirect('/napaka_ob_prijavi/')

@bottle.post('/logout/')
def logout_post():
    bottle.response.delete_cookie('uporabnisko_ime', path='/')
    bottle.redirect('/')

@bottle.get('/')
def osnovna_stran():
    uporabnik = bottle.request.get_cookie('uporabnisko_ime', secret=SIFRA)
    stanje = trenutni_uporabnik_stanje()
    return bottle.template('osnova.html', leta = stanje.solska_leta, user=uporabnik)

@bottle.post('/dodaj_solsko_leto/')
def dodaj_solsko_leto():
    stanje = trenutni_uporabnik_stanje()
    ime = bottle.request.forms.getunicode('Ime')
    if je_neprazen_niz(ime):
        stanje.dodaj_solsko_leto(ime)
        shrani(stanje)
        bottle.redirect('/')
    else:
        bottle.redirect('/')

@bottle.post('/izbrisi_solsko_leto/')
def izbrisi_solsko_leto():
    stanje = trenutni_uporabnik_stanje()
    if not je_neprazen_seznam(stanje.solska_leta):
        bottle.redirect('/')
    ime = bottle.request.forms.getunicode('Ime')
    stanje.izbrisi_solsko_leto(ime)
    shrani(stanje)
    bottle.redirect('/')

@bottle.get('/solsko_leto/<index:int>/')
def solsko_leto(index):
    stanje = trenutni_uporabnik_stanje()
    aktualno = stanje.solska_leta[index]
    stanje.nastavi_aktualno(aktualno)
    return bottle.template(
        'solsko_leto.html',
        leto=aktualno,
        predmeti=aktualno.predmeti,
        index=index)

@bottle.post('/solsko_leto/<index:int>/dodaj_predmet/')
def dodaj_predmet(index):
    stanje = trenutni_uporabnik_stanje()
    aktualno = stanje.solska_leta[index]
    stanje.nastavi_aktualno(aktualno)
    ime = bottle.request.forms.getunicode('ime')
    st = bottle.request.forms.getunicode('st')
    if not preveri_int(st):
        bottle.redirect(f'/solsko_leto/{index}/')
    stanje.dodaj_predmet(ime, int(st))
    shrani(stanje)
    bottle.redirect(f'/solsko_leto/{index}/')

@bottle.post('/solsko_leto/<index:int>/odstrani_predmet/')
def izbrisi_predmet(index):
    stanje = trenutni_uporabnik_stanje()
    aktualno = stanje.solska_leta[index]
    stanje.nastavi_aktualno(aktualno)
    if not je_neprazen_seznam(aktualno.predmeti):
        bottle.redirect(f'/solsko_leto/{index}/')
    ime = bottle.request.forms.getunicode('ime')
    stanje.odstrani_predmet(ime)
    shrani(stanje)
    bottle.redirect(f'/solsko_leto/{index}/')    

@bottle.post('/solsko_leto/<index:int>/vpisi_oceno/')
def vpisi_oceno(index):
    stanje = trenutni_uporabnik_stanje()
    aktualno = stanje.solska_leta[index]
    stanje.nastavi_aktualno(aktualno)
    if not je_neprazen_seznam(aktualno.predmeti):
        bottle.redirect(f'/solsko_leto/{index}/')
    ime_pr = bottle.request.forms.getunicode('ime_pr')
    opis = bottle.request.forms.getunicode('opis')
    kol = bottle.request.forms.getunicode('kol')
    if je_neprazen_niz(opis) and preveri_int(kol):
        stanje.vpisi_oceno(ime_pr, opis, int(kol))
        shrani(stanje)
        bottle.redirect(f'/solsko_leto/{index}/')
    else:
        bottle.redirect(f'/solsko_leto/{index}/')

@bottle.post('/solsko_leto/<index:int>/dodaj_rezultat/')
def dodaj_rezultat(index):
    stanje = trenutni_uporabnik_stanje()
    aktualno = stanje.solska_leta[index]
    stanje.nastavi_aktualno(aktualno)
    if not je_neprazen_seznam(aktualno.predmeti):
        bottle.redirect(f'/solsko_leto/{index}/')
    ime_pr = bottle.request.forms.getunicode('ime_pr')
    opis = bottle.request.forms.getunicode('opis')
    kol = bottle.request.forms.getunicode('kol')
    if je_neprazen_niz(opis) and preveri_float(kol):
        stanje.dodaj_rezultat(ime_pr, opis, float(kol))
        shrani(stanje)
        bottle.redirect(f'/solsko_leto/{index}/')
    else:
        bottle.redirect(f'/solsko_leto/{index}/')

@bottle.post('/solsko_leto/<index:int>/izbrisi_oceno/')
def izbrisi_oceno(index):
    stanje = trenutni_uporabnik_stanje()
    aktualno = stanje.solska_leta[index]
    stanje.nastavi_aktualno(aktualno)
    if not je_neprazen_seznam(aktualno.predmeti):
        bottle.redirect(f'/solsko_leto/{index}/')
    ime_pr = bottle.request.forms.getunicode('ime_pr')
    opis = bottle.request.forms.getunicode('opis')
    if not je_neprazen_niz(opis):
        bottle.redirect(f'/solsko_leto/{index}/')
    stanje.izbrisi_oceno(ime_pr, opis)
    shrani(stanje)
    bottle.redirect(f'/solsko_leto/{index}/')

@bottle.post('/solsko_leto/<index:int>/odstrani_rezultat/')
def odstrani_rezultat(index):
    stanje = trenutni_uporabnik_stanje()
    aktualno = stanje.solska_leta[index]
    stanje.nastavi_aktualno(aktualno)
    if not je_neprazen_seznam(aktualno.predmeti):
        bottle.redirect(f'/solsko_leto/{index}/')
    ime_pr = bottle.request.forms.getunicode('ime_pr')
    opis = bottle.request.forms.getunicode('opis')
    if not je_neprazen_niz(opis):
        bottle.redirect(f'/solsko_leto/{index}/')
    stanje.odstrani_rezultat(ime_pr, opis)
    shrani(stanje)
    bottle.redirect(f'/solsko_leto/{index}/')

@bottle.post('/solsko_leto/<index:int>/nastavi_kolokvije/')
def nastavi_st_kolokvijev(index):
    stanje = trenutni_uporabnik_stanje()
    aktualno = stanje.solska_leta[index]
    stanje.nastavi_aktualno(aktualno)
    if not je_neprazen_seznam(aktualno.predmeti):
        bottle.redirect(f'/solsko_leto/{index}/')
    ime_pr = bottle.request.forms.getunicode('ime_pr')
    st = bottle.request.forms.getunicode('st')
    if not preveri_int(st):
        bottle.redirect(f'/solsko_leto/{index}/')
    stanje.nastavi_st_kolokvijev(ime_pr, int(st))
    shrani(stanje)
    bottle.redirect(f'/solsko_leto/{index}/')

bottle.run(debug=True, reloader=True)