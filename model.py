class Predmet:
    def __init__(self, ime, slovar={}, st=2, slovar_ocen={}, numerus=2):
        self.ime = ime
        self.rezultati = slovar
        self.stevilo_kolokvijev = st
        self.ocene = slovar_ocen
        self.stevilo_ocen = numerus

    #obejktu razreda Predmet dodelimo ime, slovar rezultatov kolokvijev, stevilo kolokvijev,
    #slovar ocen, ki se vpišejo pri predmetu, in število ocen pri predmetu (za kasneje)
    #default value za število ocen pri predmetu je 2, vrednost bo potrebna za izračun povprečja v letniku kasneje
    #ideja je, da ločimo beleženje rezultatov na kolokvijih in vpis ocen, saj ni nujno, da bo ocena iz kolokvijev dejansko vpisana

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

    def vpisi_oceno(self, opis, kolicina=None):
        if opis in self.ocene.keys():
            return "Ta opis je že uporabljen."
        else:
            self.ocene[opis] = kolicina

    #razmisli, če je mogoče bolje da je default 0

    def izbrisi_oceno(self, opis):
        if opis in self.ocene.keys():
            del self.ocene[opis]
        else:
            return "Te ocene ni v redovalnici."

    def seznam_rezultatov(self):
        return [res for res in self.rezultati.values()]

    def seznam_ocen(self):
        return[oc for oc in self.ocene.values()]

    def trenutna_vsota_rezultatov(self):
        out = 0
        for res in self.seznam_rezultatov():
            out += res
        return out

    def trenutna_vsota_ocen(self):
        out = 0
        for oc in self.seznam_ocen():
            out += oc
        return out

    def trenutno_povprecje(self): 
        return round(self.trenutna_vsota_rezultatov() / len(self.seznam_rezultatov()), 2)

    def trenutno_povprecje_ocen(self):
        return round(self.trenutna_vsota_ocen() / len(self.seznam_ocen()), 2)

    def trenutna_ocena_iz_rezultatov(self):
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