import bottle
import model
IME_DATOTEKE_S_STANJEM = 'stanje.json'
STEVKE = '0123456789'
stanje = model.Stanje.preberi_iz_datoteke(IME_DATOTEKE_S_STANJEM)

def shrani():
    stanje.zapisi_v_datoteko(IME_DATOTEKE_S_STANJEM)

@bottle.get('/')
def osnovna_stran():
    return bottle.template('osnova.html', leta = stanje.solska_leta)

@bottle.post('/dodaj_solsko_leto/')
def dodaj_solsko_leto():
    ime = bottle.request.forms['Ime']
    stanje.dodaj_solsko_leto(ime)
    shrani()
    bottle.redirect('/')

@bottle.post('/izbrisi_solsko_leto/')
def izbrisi_solsko_leto():
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
    if st == '':
        bottle.redirect(f'/solsko_leto/{index}/')
    for znak in st:
        if znak not in STEVKE:
            bottle.redirect(f'/solsko_leto/{index}/')   
        elif znak[0] == '0':
            bottle.redirect(f'/solsko_leto/{index}/')
    stanje.dodaj_predmet(ime, int(st))
    shrani()
    bottle.redirect(f'/solsko_leto/{index}/')

@bottle.post('/solsko_leto/<index:int>/odstrani_predmet/')
def izbrisi_predmet(index):
    aktualno = stanje.solska_leta[index]
    stanje.nastavi_aktualno(aktualno)
    ime = bottle.request.forms['ime']
    stanje.odstrani_predmet(ime)
    shrani()
    bottle.redirect(f'/solsko_leto/{index}/')    


bottle.run(debug=True, reloader=True)