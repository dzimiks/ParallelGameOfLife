# TODO: Task 3
# TODO: =============================================
# TODO: zasebni process za prikaz i crtanje animacije (pre je bio niz matrica)
# TODO: ne javlja da se ciklus zavrsio (samo za analizu stanja)
# TODO: globalni deljeni Queue koji niko nece da cita, vec u njega samo pisemo vrednosti
# TODO: celija pogleda kolika je velicina reda trenutno
# TODO: citamo vrednost u prethodnoj iteraciji za celije da bismo znali nasu trenutnu vrednost
# TODO: deljeni red je blokirajuci, kad imam read na njim, ako je prazan, onda se blokiram dok se ne upise nesto u njega
# TODO: imam svoj red gde ocekujem da mi susedi upisuju vrednosti
# TODO: kad uradim read nad tim redom, ako je neko upisao vrednosti, procitam tu vrednost
# TODO: ako read stavim u for petlju duzine 8, onda citam 8 vrednosti od suseda
# TODO: pre read-a, prvo u prvoj for petlji cu svim svojim susedima da kazem svoju vrednost
# TODO: njima upisem u njihove redove i onda citam
# TODO: redovi treba da budu velicine 8 za broj suseda
# TODO: uradim write, uradim read, onda prelazak u novu iteraciju sa globalnim deljenim redom
# TODO: konsultacije sutra?
# TODO: svaka celija ima queue i ostali upisuju vrednosti
# TODO: susedima upise vrednost
# TODO: globalni brojac ipak na kraju!!!!!
# TODO: =============================================

# TODO: Task 4
# TODO: =============================================
# TODO: recimo imam 5x5 matricu i pravim 5 procesa za svaki red u matrici
# TODO: glavni program spawnuje procese koji rade analizu rada
# TODO: glavni program ima celu matricu i dace procesu sve potrebne vrednosti svih suseda
# TODO: funkcija je zapravo podproces koja ce da vrati nazad glavnom programu
# TODO: Process Pool -> map()
# TODO: damo matricu i on nam vrati nazad
# TODO: funkc koju prosledim poolu da vrati i, j i novu vrednost
# TODO: =============================================
