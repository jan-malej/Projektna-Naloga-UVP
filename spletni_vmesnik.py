import bottle
import model
IME_DATOTEKE_S_STANJEM = 'stanje.json'
stanje = model.Stanje.preberi_iz_datoteke(IME_DATOTEKE_S_STANJEM)

def shrani():
    stanje.zapisi_v_datoteko(IME_DATOTEKE_S_STANJEM)

@bottle.get('/')
def osnovna_stran():
    return bottle.template('osnova.html', imena = stanje.solska_leta)

@bottle.post('/dodaj_solsko_leto/')
def dodaj_solsko_leto():
    ime = bottle.request.forms['Ime']
    stanje.dodaj_solsko_leto(ime)
    #stanje.zapisi_v_datoteko(IME_DATOTEKE_S_STANJEM)
    bottle.redirect('/')

@bottle.post('/izbrisi_solsko_leto/')
def izbrisi_solsko_leto():
    ime = bottle.request.forms['Ime']
    stanje.izbrisi_solsko_leto(ime)
    #stanje.zapisi_v_datoteko(IME_DATOTEKE_S_STANJEM)
    bottle.redirect('/')

bottle.run(debug=True, reloader=True)