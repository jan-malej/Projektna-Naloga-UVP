class Predmet:
    def __init__(self, ime, slovar={}):
        self.ime = ime
        self.ocene = slovar

    def dodaj(self, opis, kolicina):
        if opis in self.ocene.keys():
            return "Ta ocena je že vnešena."
        else:
            self.ocene[opis] = kolicina