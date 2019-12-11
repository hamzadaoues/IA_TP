from copy import deepcopy


class Resolveur:
    def __init__(self, log_file):
        self.log_file = log_file

    def isVariable(self, E):
        return E.startswith('?')

    def itContains(self, E1, E2):
        if E2.find(E1) == -1:
            return False
        return True

    def unifier_atome(self, E1, E2):
        if E1 == E2:
            return True
        if self.isVariable(E1):
            if self.itContains(E1, E2):
                return False
            return '{' + E1 + '/' + E2 + '}'
        if self.isVariable(E2):
            return '{' + E2 + '/' + E1 + '}'
        return False

    # return taleau a deux element
    def parse_unificateur(self, U):
        U = U[1:]
        U = U[:-1]
        return U.split('/')

    # U c est l unificateur : {?y/?x};{?z/4};{?y/9}
    def substitute(self, E, U):
        table_unif = U.split(';')
        for u in table_unif:
            unificateur = self.parse_unificateur(u)
            for i, _ in enumerate(E):
                E[i] = E[i].replace(unificateur[0], unificateur[1])
        return E

    # E is table of items
    def unifier_terme(self, E1, E2):
        if len(E1) == 1:
            return self.unifier_atome(E1[0], E2[0])
        F1 = E1[0:1]
        F2 = E2[0:1]
        E1.pop(0)
        E2.pop(0)
        Z1 = self.unifier_terme(F1, F2)
        if not Z1:
            return False
        if type(Z1) == type(True):
            G1 = E1
            G2 = E2
        else:
            G1 = self.substitute(E1, Z1)
            G2 = self.substitute(E2, Z1)
        # print(G1)
        # print(G2)
        Z2 = self.unifier_terme(G1, G2)
        if type(Z1) == type(True):
            return Z2
        else:
            return Z1 + ';' + Z2
        # appliquer substitution

    def unifier_predicat(self, p1, p2):
        tab_regle1 = list()
        for parametre in p1.parametres:
            tab_regle1.extend(parametre.items)
        tab_regle2 = list()
        for parametre in p2.parametres:
            tab_regle2.extend(parametre.items)
        s = self.unifier_terme(tab_regle1, tab_regle2)
        return s

    # s c est l unificateur
    def verifier_condition(self, condition, s):
        condition_var = condition.variables
        condition_operators_between_var = condition.operators_between_var
        E = self.substitute(condition_var, s)
        value = int(E[0])
        i = 1
        while i < len(E):
            operateur = condition_operators_between_var[i - 1]
            if operateur == '+':
                value = value + int(E[i])
            if operateur == '-':
                value = value - int(E[i])
            i = i + 1
        operateur = condition.operator
        if operateur == '<':
            return value < int(condition.value)
        if operateur == '>':
            return value > int(condition.value)
        if operateur == '=':
            return value == int(condition.value)
        if operateur == '<=':
            return value <= int(condition.value)
        if operateur == '>=':
            return value >= int(condition.value)

    # cruchesAetB (4, ?y+2) and s={?y/1} => cruchesAetB (4, 3)
    def substitute_conclision(self, conclusion, S):
        for i, _ in enumerate(conclusion.parametres):
            conclusion.parametres[i].items = self.substitute(conclusion.parametres[i].items, S)
            items_tab = conclusion.parametres[i].items
            operators_between_items = conclusion.parametres[i].operators_between_items
            value = int(items_tab[0])
            j = 1
            while j < len(items_tab):
                operateur = operators_between_items[j - 1]
                if operateur == '+':
                    value = value + int(items_tab[j])
                if operateur == '-':
                    value = value - int(items_tab[j])
                j = j + 1
            conclusion.parametres[i].items = [value.__str__()]
        return conclusion

        # etat peut etre : cruchesAetB (0,0)

    # Exemple
    # Regle : si cruchesAetB (?x, ?y) et ?x + ?y + 2<=4 et ?y>=0 alors cruchesAetB (4, ?y+2)
    # Fait : cruchesAetB (0,2)
    # Conclusion : cruchesAetB (4,2)
    def genere_conclusion_regle(self, etat, regle):
        s = self.unifier_predicat(etat, regle.predicat)
        condition_verifié = True
        for condition in regle.conditions:
            if not self.verifier_condition(condition, s):
                condition_verifié = False
        if condition_verifié:
            conclusion = regle.conclusion
            if type(s) != type(True):
                conclusion = self.substitute_conclision(conclusion, s)
            else:
                return False
            return conclusion
        else:
            return False

    def génèreOperateursApplicables(self, etat, liste_regles):
        list_conclusion = list()
        i = 0
        for regle in liste_regles:
            i = i + 1
            conclusion = self.genere_conclusion_regle(etat, regle)
            if conclusion:
                list_conclusion.append(conclusion)
        return list_conclusion

    # Algorithme de recherche A en profondeur maximaum h
    def recherche_A(self, etat, h, hMax, liste_regle, but, visited):
        if etat in visited:
            return False
        else:
            visited.add(etat)
        but_trouve = False
        # verifier si le but est atteint
        s = self.unifier_predicat(etat, but)
        if type(s) == type(True):
            print(etat)
            if s:
                return True
        else:
            return True
        if h == hMax:
            return False
        etat_possible = self.génèreOperateursApplicables(etat, deepcopy(liste_regle))
        # log file
        self.log_file.write_node(etat, h, etat_possible)
        for etat_single in etat_possible:
            but_trouve = self.recherche_A(etat_single, h + 1, hMax, liste_regle, but, visited)
            if but_trouve:
                return True
        return but_trouve

    # Algorithme de recherche en profondeur limitée itérative
    def recherche_A_limite_iterative(self, etat, hauteurMAX, liste_regle, but):
        visited = set()
        h = 1
        while h <= hauteurMAX:
            self.log_file.write_iteration()
            res = self.recherche_A(etat, 0, h, liste_regle, but, visited)
            self.log_file.iteration = self.log_file.iteration + 1
            visited.clear()
            if res:
                self.log_file.write_result(h, True)
                return True
            h = h + 1
        self.log_file.write_result(h, False)
        return False

    def recherche_A_heuristique(self, etat, liste_regle, but):
        visited = set()
        # set h
        h = 10
        x = etat.parametres[0].items[0]
        y = etat.parametres[1].items[0]
        if x == '2':
            h = 0
        else:
            if int(x) + int(y) < 2:
                h = 7
            else:
                if int(y) > 2:
                    h = 3
                else:
                    h = 1
        self.log_file.write_heuristique_detail(h)
        res = self.recherche_A(etat, 0, h, liste_regle, but, visited)
        print(res)
        if res:
            self.log_file.write_result(h-1, True)
            return True
        self.log_file.write_result(h, False)
