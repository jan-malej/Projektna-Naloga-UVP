class Predmet:
    def __init__(self, ime, slovar={}, st=2):
        self.ime = ime
        self.rezultati = slovar
        self.stevilo_kolokvijev = st

    def dodaj_rezultat(self, opis, kolicina):
        if opis in self.rezultati.keys():
            return "Ta opis je že uporabljen."
        else:
            self.rezultati[opis] = kolicina

    def odstrani_rezultat(self, opis):
        if opis in self.rezultati.keys():
            del self.rezultati[opis]
        else:
            return "Tega rezultata ni v redovalnici."

    def seznam_rezultatov(self):
        return [res for res in self.rezultati.values()]

    def trenutna_vsota_rezultatov(self):
        out = 0
        for res in self.seznam_rezultatov():
            out += res
        return out

    def trenutno_povprecje(self):
        vsota = 0
        for st in self.seznam_rezultatov():
            vsota += st  
        return round(vsota / len(self.seznam_rezultatov()), 2)

    def trenutna_ocena(self):
        if self.trenutno_povprecje() < 50:
            return 5
        elif self.trenutno_povprecje() == 100:
            return 10
        else:
            return int(self.trenutno_povprecje() // 10 + 1)

    def koliko_potrebujem(self, ocena):
        """Glede na dosedanje rezultate vrne vrednost (minimalen potreben rezultat)/kolokvij, če študent želi doseči oceno."""   
        if ocena <= 5 or ocena > 10:
            return "Tu ni kaj izračunati, uporabne ocene so od vključno 6 do vključno 10."
        
        elif self.stevilo_kolokvijev <= len(self.seznam_rezultatov()):
            return "Prepozno je za tak izračun, imate preveč vnešenih rezultatov."
        minimum = (ocena - 1) * 10
        potrebna_vsota = minimum * self.stevilo_kolokvijev
        out = (potrebna_vsota - self.trenutna_vsota_rezultatov()) / (self.stevilo_kolokvijev - len(self.seznam_rezultatov()))
        if out > 100:
            return f"Za {ocena} v povprečju potrebujete {out} odstotkov na vsak preostali kolokvij. Težka bo."
        elif out <= 0:
            return f"Oceno {ocena} imate že zagotovljeno."
        return f"Za {ocena} v povprečju potrebujete {out} odstotkov na vsak preostali kolokvij."


class SolskoLeto:
    pass

class Stanje:
    pass