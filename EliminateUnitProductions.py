class EliminateUnitProductions:
    grammar = None
    unit_prods = []

    def __init__(self, _grammar):
        self.grammar = _grammar
        self.unit_prods = self.find_unit_prods()
        self.eliminate()
        self.clear()
        self.print_result()

    def eliminate(self):
        unit_prods = self.find_unit_prods()
        while len(unit_prods) > 0:
            new_prods = []
            for up in unit_prods:
                prod = up[0]
                u_rules = up[1]
                new_prods = self.grammar.productions[prod]
                for ur in u_rules:
                    new_prods.remove(ur)
                    if ur in self.grammar.productions:
                        new_prods += self.grammar.productions[ur]
            self.grammar.productions[prod] = new_prods
            unit_prods = self.find_unit_prods()

    def find_unit_prods(self):
        new_unit_productions = []
        for prod, rules in self.grammar.productions.items():
            unit_prods = []
            for rule in rules:
                if self.rule_matches_symbol(rule):
                    unit_prods.append(rule)
            if len(unit_prods) > 0:
                new_unit_productions.append((prod, unit_prods))
        return new_unit_productions

    def rule_matches_symbol(self, rule):
        for symbol in self.grammar.symbols:
            if rule == symbol:
                return True
        return False

    def clear(self):
        for prod, rules in self.grammar.productions.items():
            self.grammar.productions[prod] = list(set(rules))

    def print_result(self):
        print("============================\n")
        print("Eliminating Unit productions")
        print("\n")
        print("Unit productions are: ")
        self.print_unit_prods()
        print("\n")
        self.grammar.print_grammar()
        print("\n============================")

    def print_unit_prods(self):
        if self.unit_prods:
            for up in self.unit_prods:
                print(up[0] + " -> " + " | ".join(up[1]))




