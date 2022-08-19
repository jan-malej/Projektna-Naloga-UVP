import json

class Predmet:
    def __init__(self, ime, slovar={}, st=2, slovar_ocen={}, numerus=2):
        self.ime = ime
        self.rezultati = slovar
        self.stevilo_kolokvijev = st
        self.ocene = slovar_ocen
        self.stevilo_ocen = numerus

    def nastavi_st_kolokvijev(self, n):
        self.stevilo_kolokvijev = n

    def nastavi_st_ocen(self, n):
        self.stevilo_ocen = n
    
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
        if self.seznam_rezultatov() == []:
            return "Noben rezultat še ni bil dodan." 
        return round(self.trenutna_vsota_rezultatov() / len(self.seznam_rezultatov()), 2)

    def trenutno_povprecje_ocen(self):
        if self.seznam_ocen() == []:
            return "Nobena ocena še ni bila vpisana."
        return round(self.trenutna_vsota_ocen() / len(self.seznam_ocen()), 2)

    def trenutna_ocena_iz_rezultatov(self):
        if self.seznam_rezultatov() == []:
            return "Noben rezultat še ni bil dodan."
        elif self.trenutno_povprecje() < 50:
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

    def v_slovar(self):
        return {
            'ime': self.ime,
            'rezultati': self.rezultati,
            'stevilo_kolokvijev': self.stevilo_kolokvijev,
            'ocene': self.ocene,
            'stevilo_ocen': self.stevilo_ocen
        }

    @staticmethod
    def iz_slovarja(slovar):
        return Predmet(slovar['ime'],
        slovar['rezultati'],
        slovar['stevilo_kolokvijev'],
        slovar['ocene'],
        slovar['stevilo_ocen'])

class SolskoLeto:
    def __init__(self, ime):
        self.ime = ime
        self.predmeti = {}

    def dodaj_predmet(self, ime):
        if ime in self.predmeti.keys():
            return "Dva predmeta ne moreta imeti enakih imen. To ime je že uporabljeno."
        predmet = Predmet(ime)
        self.predmeti[ime] = predmet

    def odstrani_predmet(self, ime):
        if ime in self.predmeti.keys():
            del self.predmeti[ime]
        return "Tega predmeta ni v redovalnici."

    def povprecje(self):
        if len(self.predmeti) == 0:
            return "Najprej je potrebno vpisati vsaj en predmet."
        vsota = 0
        stevec = 0
        for predmet in self.predmeti.values():
            for oc in predmet.seznam_ocen():
                vsota += oc
                stevec += 1
        if stevec == 0:
            return "Najprej je potrebno vpisati kakšno oceno."
        return round(vsota / stevec, 2)

    def v_slovar(self):
        return {
            'ime': self.ime,
            'predmeti': [predmet.v_slovar() for predmet in self.predmeti.values()]
        }

    @staticmethod
    def iz_slovarja(slovar):
        leto = SolskoLeto(slovar['ime'])
        sez = [Predmet.iz_slovarja(predmet) for predmet in slovar['predmeti']]
        for pr in sez:
            leto.predmeti[pr.ime] = pr
        return leto

class Stanje:
    def __init__(self):
        self.solska_leta = []
        self.aktualno_solsko_leto = None

    def dodaj_solsko_leto(self, ime):
        leto = SolskoLeto(ime)
        self.solska_leta.append(leto)
        if not self.aktualno_solsko_leto:
            self.aktualno_solsko_leto = leto

    def izbrisi_solsko_leto(self, s_leto):
        self.solska_leta.remove(s_leto)

    def nastavi_aktualno(self, s_leto):
        self.aktualno_solsko_leto = s_leto

    def dodaj_predmet(self, predmet):
        self.aktualno_solsko_leto.dodaj_predmet(predmet)

    def odstrani_predmet(self, predmet):
        self.aktualno_solsko_leto.odstrani_predmet(predmet)

    def vpisi_oceno(self, ime_predmeta, opis, kolicina):
        if ime_predmeta in self.aktualno_solsko_leto.predmeti.keys():
            self.aktualno_solsko_leto.predmeti[ime_predmeta].vpisi_oceno(opis, kolicina)
        else:
            return "Tega predmeta ni v tem šolskem letu."

    def izbrisi_oceno(self, ime_predmeta, opis):
        if ime_predmeta in self.aktualno_solsko_leto.predmeti.keys():
            self.aktualno_solsko_leto.predmeti[ime_predmeta].izbrisi_oceno(opis) 
        else:
            return "Tega predmeta ni v tem šolskem letu."

    def dodaj_rezultat(self, ime_predmeta, opis, kolicina):
        if ime_predmeta in self.aktualno_solsko_leto.predmeti.keys():
            self.aktualno_solsko_leto.predmeti[ime_predmeta].dodaj_rezultat(opis, kolicina)
        else:
            return "Tega predmeta ni v tem šolskem letu."

    def odstrani_rezultat(self, ime_predmeta, opis):
        if ime_predmeta in self.aktualno_solsko_leto.predmeti.keys():
            self.aktualno_solsko_leto.predmeti[ime_predmeta].odstrani_rezultat(opis) 
        else:
            return "Tega predmeta ni v tem šolskem letu."

    def nastavi_st_kolokvijev(self, ime_predmeta, n):
        if ime_predmeta in self.aktualno_solsko_leto.predmeti.keys():
            self.aktualno_solsko_leto.predmeti[ime_predmeta].nastavi_st_kolokvijev(n) 
        else:
            return "Tega predmeta ni v tem šolskem letu."

    def nastavi_st_ocen(self, ime_predmeta, n):
        if ime_predmeta in self.aktualno_solsko_leto.predmeti.keys():
            self.aktualno_solsko_leto.predmeti[ime_predmeta].nastavi_st_ocen(n) 
        else:
            return "Tega predmeta ni v tem šolskem letu."

    def v_slovar(self):
        return {
            'solska_leta': [leto.v_slovar() for leto in self.solska_leta]
        }

    @staticmethod
    def iz_slovarja(slovar):
        out = Stanje()
        out.solska_leta = [SolskoLeto.iz_slovarja(sl) for sl in slovar['solska_leta']]
        return out

    def zapisi_v_datoteko(self, datoteka):
        with open(datoteka, 'w') as dat:
            slovar = self.v_slovar()
            json.dump(slovar, dat)

    @staticmethod
    def preberi_iz_datoteke(datoteka):
        with open(datoteka) as dat:
            slovar = json.load(dat)
            return Stanje.iz_slovarja(slovar)