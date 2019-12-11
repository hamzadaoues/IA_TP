class Predicat:

    def __init__(self, function,
                 parametres):  # parametres est un tableau de parametres : ?x est variable , autrement c une valeur
        self.function = function
        self.parametres = parametres

    def __str__(self):
        return self.function + '(' + self.parametres[0].items[0] + ', ' + self.parametres[1].items[0] + ')'
