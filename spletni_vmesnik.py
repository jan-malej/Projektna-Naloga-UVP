import bottle
import model
IME_DATOTEKE_S_STANJEM = 'stanje.json'
stanje = model.Stanje.preberi_iz_datoteke(IME_DATOTEKE_S_STANJEM)
print(enumerate(stanje.solska_leta))
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
        leto=aktualno)

bottle.run(debug=True, reloader=True)