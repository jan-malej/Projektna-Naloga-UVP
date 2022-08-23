import bottle
import model
IME_DATOTEKE_S_STANJEM = 'stanje.json'
STEVKE = '0123456789'
stanje = model.Stanje.preberi_iz_datoteke(IME_DATOTEKE_S_STANJEM)

def preveri_vnos(vnos):
    """Preveri, če je vnos prazen niz in če je celo število."""
    if vnos == '':
        return False
    elif vnos[0] == '0':
        return False
    for znak in vnos:
        if znak not in STEVKE:
            return False
           
    return True

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

def shrani():
    stanje.zapisi_v_datoteko(IME_DATOTEKE_S_STANJEM)

@bottle.get('/')
def osnovna_stran():
    return bottle.template('osnova.html', leta = stanje.solska_leta)

@bottle.post('/dodaj_solsko_leto/')
def dodaj_solsko_leto():
    ime = bottle.request.forms['Ime']
    if je_neprazen_niz(ime):
        stanje.dodaj_solsko_leto(ime)
        shrani()
        bottle.redirect('/')
    else:
        bottle.redirect('/')

@bottle.post('/izbrisi_solsko_leto/')
def izbrisi_solsko_leto():
    if not je_neprazen_seznam(stanje.solska_leta):
        bottle.redirect('/')
    ime = bottle.request.forms['Ime']
    stanje.izbrisi_solsko_leto(ime)
    shrani()
    bottle.redirect('/')

@bottle.get('/solsko_leto/<index:int>/')
def solsko_leto(index):
    aktualno = stanje.solska_leta[index]
    stanje.nastavi_aktualno(aktualno)
    return bottle.template(
        'solsko_leto.html',
        leto=aktualno,
        predmeti=aktualno.predmeti,
        index=index)

@bottle.post('/solsko_leto/<index:int>/dodaj_predmet/')
def dodaj_predmet(index):
    aktualno = stanje.solska_leta[index]
    stanje.nastavi_aktualno(aktualno)
    ime = bottle.request.forms['ime']
    st = bottle.request.forms['st']
    if not preveri_vnos(st):
        bottle.redirect(f'/solsko_leto/{index}/')
    stanje.dodaj_predmet(ime, int(st))
    shrani()
    bottle.redirect(f'/solsko_leto/{index}/')

@bottle.post('/solsko_leto/<index:int>/odstrani_predmet/')
def izbrisi_predmet(index):
    aktualno = stanje.solska_leta[index]
    stanje.nastavi_aktualno(aktualno)
    if not je_neprazen_seznam(aktualno.predmeti):
        bottle.redirect(f'/solsko_leto/{index}/')
    ime = bottle.request.forms['ime']
    stanje.odstrani_predmet(ime)
    shrani()
    bottle.redirect(f'/solsko_leto/{index}/')    

@bottle.post('/solsko_leto/<index:int>/vpisi_oceno/')
def vpisi_oceno(index):
    aktualno = stanje.solska_leta[index]
    stanje.nastavi_aktualno(aktualno)
    if not je_neprazen_seznam(aktualno.predmeti):
        bottle.redirect(f'/solsko_leto/{index}/')
    ime_pr = bottle.request.forms['ime_pr']
    opis = bottle.request.forms['opis']
    kol = bottle.request.forms['kol']
    if je_neprazen_niz(opis) and preveri_vnos(kol):
        stanje.vpisi_oceno(ime_pr, opis, int(kol))
        shrani()
        bottle.redirect(f'/solsko_leto/{index}/')
    else:
        bottle.redirect(f'/solsko_leto/{index}/')

bottle.run(debug=True, reloader=True)