class Condition:
    def __init__(self, variables, operators_between_var, operator, value):
        self.variables = variables
        self.operators_between_var = operators_between_var
        self.operator = operator
        self.value = value