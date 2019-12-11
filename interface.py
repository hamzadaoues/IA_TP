from tkinter import *
from tkinter import filedialog
from ChargeFromFile import ChargeFromFile
from Resolveur import Resolveur
from log_file import log_file

log_file = log_file("algosRecherche.txt")
master = Tk()
master.title('TP2 IA')
v = StringVar(master, "1")
Label(master, text='Base de connaissance').grid(row=0)
Label(master, text='Etat initiale').grid(row=1)
Label(master, text='Etat Finale').grid(row=2)
Label(master, text='Start').grid(row=4)
Label(master, text='Algorithme de recherche').grid(row=3)
e0 = Entry(master)


def onclickParcourir():
    filepath = filedialog.askopenfilename(initialdir="/", title="Select file",
                                          filetypes=(("text files", "*.txt"), ("all files", "*.*")))
    e0.insert(END, filepath)


radio1 = Radiobutton(master, text="Recherche en profondeur limitée itérative", variable=v, value="1")
radio2 = Radiobutton(master, text="A*", variable=v, value="2")
e1 = Entry(master)
e2 = Entry(master)
Btn1 = Button(master, text="Parcourir ...", command=onclickParcourir)


def onclickStart():
    filepath = e0.get()
    etat_initiale_text = e1.get()
    etat_final_text = e2.get()
    alogorithme_choix = v.get()

    # charger la base de connaisance
    ChargerBase = ChargeFromFile(filepath)
    RegleList = ChargerBase.ReglesFromFile()
    etat_initiale = ChargerBase.predicat_create(etat_initiale_text)
    etat_final = ChargerBase.predicat_create(etat_final_text)
    # Initialiser le résolveur de problème
    Resolve = Resolveur(log_file)
    if alogorithme_choix == '1':
        log_file.write_detail("Recherche limite iterative", etat_initiale_text, etat_final_text)
        Resolve.recherche_A_limite_iterative(etat_initiale, 7, RegleList, etat_final)
    else:
        log_file.write_detail("Recherche avec heurstique A* ", etat_initiale_text, etat_final_text)
        Resolve.recherche_A_heuristique(etat_initiale, RegleList, etat_final)


Btn2 = Button(master, text="Start", command=onclickStart)
Btn1.grid(row=0, column=2)
e0.grid(row=0, column=1)
e1.grid(row=1, column=1)
e2.grid(row=2, column=1)
radio1.grid(row=3, column=1)
radio2.grid(row=3, column=2)
Btn2.grid(row=4, column=2)

mainloop()
