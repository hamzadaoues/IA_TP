from datetime import date


class log_file:

    def __init__(self, file_name):
        self.file = open(file_name, "w+")
        self.iteration = 0

    def write_detail(self, algorithme, etat_initiale, etat_finale):
        self.file.write("Date : " + date.today().__str__() + "\n")
        self.file.write("Type algorithme : " + algorithme + "\n")
        self.file.write("Etat initiale : " + etat_initiale + "\n")
        self.file.write("Etat finale : " + etat_finale + "\n")
        self.file.write(
            "############################################ Debut de l'algorithme ############################################\n")
        self.file.flush()

    def write_node(self, etat_courant, hauteur, liste_etat_possible):
        self.file.write("L'etat courant est : " + etat_courant.__str__() + "\n")
        self.file.write("Profondeur de l'arbre de recherche est : " + hauteur.__str__() + "\n")
        self.file.write("Les etats possibles déduits : \n")
        for etat_possible in liste_etat_possible:
            self.file.write("        - " + etat_possible.__str__() + "\n")
        self.file.write("\n------------------------------------------\n")
        self.file.flush()

    def write_iteration(self):
        self.file.write(
            "############################################ Iteration " + self.iteration.__str__() +
            "############################################\n")

    def write_result(self, h, finded):
        self.file.write(
            "############################################ Fin de l'algorithme ############################################\n")
        if finded:
            self.file.write("L'etat finale est achevé !!\n")
            self.file.write("Nombre d'itération : " + self.iteration.__str__() + "\n")
            self.file.write("Hauteur du résultats finale dans l'arbre de recherche : " + h.__str__() + "\n")
        else:
            self.file.write("L'etat finale n'est pas achevé !!\n")
        self.file.flush()
        self.file.close()

    def write_heuristique_detail(self, h):
        self.file.write("Le profondeur de la recherche choisis par l'heuristique : " + h.__str__())
        self.file.write("\n \n")
