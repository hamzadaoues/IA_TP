from ChargeFromFile import ChargeFromFile
from Resolveur import Resolveur
from copy import deepcopy
import array

a = ChargeFromFile("C:\\Users\\User\\Desktop\\education\\TP_IA\\connaissances.txt")
# test predicat_create function
# predicat = a.predicat_create("cruchesAetB (?x+8-?y, ?y)")
# print(predicat.parametres[0].items)

# next to do :create condition
# c = a.condition_create("?y>0")
# print(c.value)

# test for : regle creation
# regles = a.ReglesFromFile()
# for regle in regles:
#    print(regle.predicat.function)


# test for unification
u = Resolveur()
# print(u.unifier_atome('?y', '?x'))
# u.unifier_terme(['?y', '1'], ['?r', '?z'])
# print(u.substitute(['?y', '?z'], '{?y/?x};{?z/4};{?y/9}'))

# test the unification
# s = u.unifier_terme(['?y', '1', '?m'], ['?r', '?y', '?r'])
# print(s)
# substituer
# print(u.substitute(['?r', '?y', '?r'], s))

# creation fait ( c un predicat aussi )
# fait = a.predicat_create("cruchesAetB (0,2)")
# regle = a.regle_create("si cruchesAetB (?x, ?y) et ?x + ?y + 2<=4 et ?y>=0 alors cruchesAetB (4, ?y+2)")
# la conclusion est prete pour etre ajouté a la base des faits
# normalement la fonction retourne une liste des nouveaux fait
# conclusion = u.genere_conclusion_regle(fait, regle)
# print(conclusion.parametres[0].items)

# predicat1 = a.predicat_create("cruchesAetB (4,?y)")
# predicat2 = a.predicat_create("cruchesAetB (4,0)")
# print(u.unifier_predicat(predicat1, predicat2))

regle1 = a.regle_create("si cruchesAetB (?x, ?y) et ?x + ?y + 2<=4 et ?y>=0 alors cruchesAetB (4, ?y+2)")
regle2 = a.regle_create("si cruchesAetB (?x, ?y) et ?y<3 alors cruchesAetB (4, 2)")
liste_regle = list()
liste_regle.append(regle1)
liste_regle.append(regle2)
liste_regle = a.ReglesFromFile()
fait = a.predicat_create("cruchesAetB (0,0)")
but = a.predicat_create("cruchesAetB (2,0)")
# u.recherche_A_limite_iterative(fait, 30, liste_regle, but)
u.recherche_A_heuristique(fait, liste_regle, but)
