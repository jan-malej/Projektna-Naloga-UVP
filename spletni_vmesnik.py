import bottle
import model
IME_DATOTEKE_S_STANJEM = 'stanje.json'
stanje = model.Stanje.preberi_iz_datoteke(IME_DATOTEKE_S_STANJEM)

@bottle.get('/')
def osnovna_stran():
    return bottle.template('osnova.html')

bottle.run(debug=True, reloader=True)