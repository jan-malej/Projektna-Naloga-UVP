import json

class Predmet:
    def __init__(self, ime, st=2, numerus=2):
        self.ime = ime
        self.rezultati = []
        self.stevilo_kolokvijev = st
        self.ocene = []
        self.stevilo_ocen = numerus

    def __repr__(self):
        return f"Predmet({self.ime}, {self.stevilo_kolokvijev}, {self.stevilo_ocen})"

    def nastavi_st_kolokvijev(self, n):
        self.stevilo_kolokvijev = n

    def nastavi_st_ocen(self, n):
        self.stevilo_ocen = n
    
    def opisi_rezultatov(self):
        out = []
        for rez in self.rezultati:
            out.append(rez[0])
        return out

    def opisi_ocen(self):
        out = []
        for oc in self.ocene:
            out.append(oc[0])
        return out
    
    def dodaj_rezultat(self, opis, kolicina):
        if opis in self.opisi_rezultatov():
            return "Ta opis je že uporabljen."
        else:
            self.rezultati.append((opis, kolicina))
            
    def odstrani_rezultat(self, opis):
        if opis in self.opisi_rezultatov():
            for tup in self.rezultati:
                if tup[0] == opis:
                    self.rezultati.remove(tup)
        else:
            return "Tega rezultata ni v redovalnici."

    def vpisi_oceno(self, opis, kolicina=None):
        if opis in self.opisi_ocen():
            return "Ta opis je že uporabljen."
        else:
            self.ocene.append((opis, kolicina))

    def izbrisi_oceno(self, opis):
        if opis in self.opisi_ocen():
            for tup in self.ocene:
                if tup[0] == opis:
                    self.ocene.remove(tup)
        else:
            return "Te ocene ni v redovalnici."

    def seznam_rezultatov(self):
        return [res[1] for res in self.rezultati]

    def seznam_ocen(self):
        return[oc[1] for oc in self.ocene]

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
        zaokrozeno = round(out, 2)
        if out > 100:
            return f"Za {ocena} v povprečju potrebujete {zaokrozeno} odstotkov na vsak preostali kolokvij. Težka bo."
        elif out <= 0:
            return f"Oceno {ocena} imate že zagotovljeno."
        return f"Za {ocena} v povprečju potrebujete {zaokrozeno} odstotkov na vsak preostali kolokvij."

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
        out = Predmet(slovar['ime'],
        slovar['stevilo_kolokvijev'],
        slovar['stevilo_ocen'])
        out.rezultati = slovar['rezultati']
        out.ocene = slovar['ocene']
        return out

class SolskoLeto:
    def __init__(self, ime):
        self.ime = ime
        self.predmeti = []

    def __repr__(self):
        return f"SolskoLeto({self.ime}, {self.predmeti})"

    def imena_predmetov(self):
        out = []
        for predmet in self.predmeti:
            out.append(predmet.ime)
        return out
        
    def dodaj_predmet(self, predmet): #dodamo cel objekt razreda Predmet
        if predmet.ime in self.imena_predmetov():
            return "Dva predmeta ne moreta imeti enakih imen. To ime je že uporabljeno."
        self.predmeti.append(predmet)

    def odstrani_predmet(self, predmet): #sprejme objekt razreda Predmet in ga odstrani
        if predmet.ime in self.imena_predmetov():
            self.predmeti.remove(predmet)
        else:    
            return "Tega predmeta ni v redovalnici."

    def povprecje(self):
        if len(self.predmeti) == 0:
            return "Najprej je potrebno vpisati vsaj en predmet."
        vsota = 0
        stevec = 0
        for predmet in self.predmeti: #imamo list objektov razreda Predmet
            for oc in predmet.seznam_ocen(): #vsak objekt razreda Predmet ima metodo seznam ocen
                vsota += oc
                stevec += 1
        if stevec == 0:
            return "Najprej je potrebno vpisati kakšno oceno."
        return round(vsota / stevec, 2)

    def v_slovar(self):
        return {
            'ime': self.ime,
            'predmeti': [predmet.v_slovar() for predmet in self.predmeti]
        }

    @staticmethod
    def iz_slovarja(slovar):
        leto = SolskoLeto(slovar['ime'])
        leto.predmeti = [Predmet.iz_slovarja(pr) for pr in slovar['predmeti']]
            
    
        return leto

class Stanje:
    def __init__(self):
        self.solska_leta = []
        self.aktualno_solsko_leto = None

    def __repr__(self):
        return f"Stanje({self.solska_leta})"    

    def imena_solskih_let(self):
        out = []
        for s_leto in self.solska_leta:
            out.append(s_leto.ime)

    def dodaj_solsko_leto(self, ime): # mogoče bo treba metodo spremeniti da sprejme direktno objekt razreda solsko leto
        #if ime in self.imena_solskih_let():
        #    return "Dve šolski leti ne smeta imeti enakih imen. To ime je že uporabljeno." 
        leto = SolskoLeto(ime)
        self.solska_leta.append(leto)
        if not self.aktualno_solsko_leto:
            self.aktualno_solsko_leto = leto

    def izbrisi_solsko_leto(self, ime):
        #if ime in self.imena_solskih_let():
            for s_leto in self.solska_leta:
                if s_leto.ime == ime:
                    self.solska_leta.remove(s_leto)
        #else:
            #return "Tega šolskega leta ni v redovalnici"

    def nastavi_aktualno(self, s_leto):
        self.aktualno_solsko_leto = s_leto

    def dodaj_predmet(self, ime, st_kolokvijev=2, st_ocen=2):
        predmet = Predmet(ime, st_kolokvijev, st_ocen)
        self.aktualno_solsko_leto.dodaj_predmet(predmet)

    def odstrani_predmet(self, predmet):
        self.aktualno_solsko_leto.odstrani_predmet(predmet)

    def vpisi_oceno(self, ime_predmeta, opis, kolicina):
        if ime_predmeta in self.aktualno_solsko_leto.imena_predmetov():
            for pr in self.aktualno_solsko_leto.predmeti:
                if pr.ime == ime_predmeta:
                    pr.vpisi_oceno((opis, kolicina))
        else:
            return "Tega predmeta ni v tem šolskem letu."

    def izbrisi_oceno(self, ime_predmeta, opis):
        if ime_predmeta in self.aktualno_solsko_leto.imena_predmetov():
            for pr in self.aktualno_solsko_leto.predmeti:
                if pr.ime == ime_predmeta:
                    pr.izbrisi_oceno(opis) 
        else:
            return "Tega predmeta ni v tem šolskem letu."

    def dodaj_rezultat(self, ime_predmeta, opis, kolicina):
        if ime_predmeta in self.aktualno_solsko_leto.imena_predmetov():
            for pr in self.aktualno_solsko_leto.predmeti:
                if pr.ime == ime_predmeta:
                    pr.dodaj_rezultat((opis, kolicina))
        else:
            return "Tega predmeta ni v tem šolskem letu."

    def odstrani_rezultat(self, ime_predmeta, opis):
        if ime_predmeta in self.aktualno_solsko_leto.imena_predmetov():
            for pr in self.aktualno_solsko_leto.predmeti:
                if pr.ime == ime_predmeta:
                    pr.odstrani_rezultat(opis) 
        else:
            return "Tega predmeta ni v tem šolskem letu."

    def nastavi_st_kolokvijev(self, ime_predmeta, n):
        if ime_predmeta in self.aktualno_solsko_leto.imena_predmetov():
            for pr in self.aktualno_solsko_leto.predmeti:
                if pr.ime == ime_predmeta:
                    pr.nastavi_st_kolokvijev(n) 
        else:
            return "Tega predmeta ni v tem šolskem letu."

    def nastavi_st_ocen(self, ime_predmeta, n):
        if ime_predmeta in self.aktualno_solsko_leto.imena_predmetov():
            for pr in self.aktualno_solsko_leto.predmeti:
                if pr.ime == ime_predmeta:
                    pr.nastavi_st_ocen(n) 
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
            json.dump(slovar, dat, ensure_ascii=False, indent=4)

    @staticmethod
    def preberi_iz_datoteke(datoteka):
        with open(datoteka) as dat:
            slovar = json.load(dat)
            return Stanje.iz_slovarja(slovar)


a = Predmet('analiza', {'ena': 1})
b = Predmet('algebra', 2)
c = Predmet('fizika', )

b.dodaj_rezultat('prvi kolokvij', 100)
a.dodaj_rezultat('prvi kolokvij', 90)
a.nastavi_st_kolokvijev(4)
print(a.ime, a.rezultati, a.opisi_rezultatov(), a.opisi_ocen(), a.stevilo_kolokvijev, a.koliko_potrebujem(6))
print(b.ime, b.rezultati, b.stevilo_kolokvijev)

leto = SolskoLeto('2021/22')
leto.dodaj_predmet(a)
leto.dodaj_predmet(b)
leto.dodaj_predmet(c)
print(leto.imena_predmetov())
leto.odstrani_predmet(b)
print(leto.imena_predmetov())
print(leto.povprecje())
print(leto.predmeti)
aa = Stanje()
aa.dodaj_solsko_leto('2022')
aa.dodaj_predmet('mat', 2, 2)

aa.nastavi_st_kolokvijev('mat', 4)
aa.dodaj_solsko_leto(leto.ime)
aa.aktualno_solsko_leto.predmeti = leto.predmeti
print(aa.solska_leta)


print(aa.v_slovar())
aa.zapisi_v_datoteko('stanje.json')
print(aa.imena_solskih_let())
print(aa.preberi_iz_datoteke('stanje.json'))
