class Predmet:
    def __init__(self, ime, slovar={}):
        self.ime = ime
        self.ocene = slovar

    def dodaj_oceno(self, opis, kolicina):
        if opis in self.ocene.keys():
            return "Ta ocena je že vnešena."
        else:
            self.ocene[opis] = kolicina

    def odstrani_oceno(self, opis):
        if opis in self.ocene.keys():
            del self.ocene[opis]
        else:
            return "Te ocene ni v redovalnici."

    def seznam_ocen(self):
        return [ocena for ocena in self.ocene.values()]

    def trenutno_povprecje(self):
        vsota = 0
        for st in self.seznam_ocen():
            vsota += st  
        return vsota / len(self.seznam_ocen())

    def trenutna_ocena(self):
        return round(self.trenutno_povprecje())   