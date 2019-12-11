class Regle:
    def __init__(self, predicat, conditions, conclusion):  # conclusion has the same type as predicat
        # conditions is table of object of type Condition
        self.predicat = predicat
        self.conditions = conditions
        self.conclusion = conclusion
