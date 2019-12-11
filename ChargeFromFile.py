import shlex
from io import StringIO
import re
from Condition import Condition
from Predicat import Predicat
from Regle import Regle
from predicatParam import predicatParam


class ChargeFromFile:

    def __init__(self, file_location):
        self.file_location = file_location

    # works for cocnclusion too
    # create predicat object from string ## exemple cruchesAetB (?x, ?y)
    def predicat_create(self, predicat_string):
        function_name = predicat_string.split(' (')[0]
        rest = (predicat_string.split(' (')[1])[:-1]
        parametres = rest.split(',')
        parametre_array = list()
        for parametre in parametres:
            parsed = StringIO(parametre)
            l_parsed = list(shlex.shlex(parsed))
            items = list()
            operators_between_items = list()
            for parsed_item in l_parsed:
                if parsed_item == '?':
                    continue
                if parsed_item != '+' and parsed_item != '-':
                    if 'a' <= parsed_item <= 'z':
                        items.append('?' + parsed_item)
                    else:
                        items.append(parsed_item)
                else:
                    operators_between_items.append(parsed_item)
            final_param = predicatParam(items, operators_between_items)
            parametre_array.append(final_param)
        return Predicat(function_name, parametre_array)

    # create Condition object from string ## exemple ?x + ?y>=4
    def condition_create(self, condition_string):
        table = ""
        operator = ""
        operators = ['>=', '<=', '<', '>', '=']
        for op in operators:
            if op in condition_string:
                table = condition_string.split(op)
                operator = op
                break
        val = table[1]
        parsed = StringIO(table[0])
        l_parsed = list(shlex.shlex(parsed))
        # print(l_parsed)
        items = list()
        operators_between_items = list()
        for parsed_item in l_parsed:
            if parsed_item == '?':
                continue
            if parsed_item != '+' and parsed_item != '−':
                if 'a' <= parsed_item <= 'z':
                    items.append('?' + parsed_item)
                else:
                    items.append(parsed_item)
            else:
                operators_between_items.append(parsed_item)
        return Condition(items, operators_between_items, operator, val)

    def regle_create(self, line):
        table = re.split("si | et | alors ", line)
        table.pop(0)
        predicat = self.predicat_create(table[0])
        table.pop(0)
        conditions = list()
        while len(table) > 1:
            conditions.append(self.condition_create(table[0]))
            table.pop(0)
        conclusion = self.predicat_create(table[0])
        return Regle(predicat, conditions, conclusion)

    def ReglesFromFile(self):
        f = open(self.file_location, "r")
        regles = list()
        for line in f:
            line = line.rstrip('\n')
            regles.append(self.regle_create(line))
        f.close()
        return regles
