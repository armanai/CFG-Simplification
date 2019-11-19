from pygments.util import xrange


class EliminateEpsilonProductions:
    grammar = None
    nullable = []
    indirect_nullable = []

    def __init__(self, _grammar):
        self.grammar = _grammar
        self.find_nullable()
        self.eliminate()
        self.clear()
        self.print_result()

    def eliminate(self):
        new_productions = self.grammar.productions
        for null_prod in self.nullable:
            for prod, rules in new_productions.items():
                new_rules = []
                for rule in rules:
                    if not(prod == null_prod and rule == 'ε'):
                        new_rules.append(rule)
                        if null_prod in rule:
                            new_rules += self.replace_nullable(null_prod, rule)
                new_productions[prod] = new_rules
        self.grammar.productions = new_productions

    def replace_nullable(self, nullable, rule):
        occurrences_count = rule.count(nullable)
        return self.prod_combinations(rule, nullable, occurrences_count)

    def prod_combinations(self, prod, nt, count):
        numset = 1 << count
        new_prods = []
        for i in xrange(numset):
            nth_nt = 0
            new_prod = ''
            for s in prod:
                if s == nt:
                    if i & (1 << nth_nt):
                        new_prod += s
                    nth_nt += 1
                else:
                    new_prod += s
            if not new_prod:
                new_prod = "ε"
            if new_prod not in new_prods:
                new_prods.append(new_prod)
        return new_prods

    def eliminate_single_nullable(self):
        new_productions = dict()
        for key, value in self.grammar.productions.items():
            if not (len(value) == 1 and value[0] == "ε"):
                new_productions[key] = value
        self.grammar.productions = new_productions

    def find_nullable(self):
        productions = self.grammar.get_separate_productions()
        for prod in productions:
            if prod[1] == "ε" and prod[0] not in self.nullable:
                self.nullable.append(prod[0])
        self.find_derived_nullable()

    def find_derived_nullable(self):
        productions = self.grammar.get_separate_productions()
        if self.nullable:
            for prod in productions:
                if self.is_nullable_production(prod[1]) and prod[0] not in self.nullable:
                    self.nullable.append(prod[0])
                    self.indirect_nullable.append(prod[0])

    def is_nullable_production(self, prod):
        for null_prod in self.nullable:
            prod = prod.replace(null_prod, '')
        return not prod

    def clear(self):
        for prod, rules in self.grammar.productions.items():
            self.grammar.productions[prod] = list(set(rules))

    def print_result(self):
        print("============================\n")
        print("Eliminating Epsilon productions")
        if self.nullable:
            print("Symbols with epsilon production are: " + ", ".join(
                self.nullable))
            if self.indirect_nullable:
                print("of which the indirect epsilon productions are " + ", ".join(
                    self.indirect_nullable))
            print("\n")
        self.grammar.print_grammar()
        print("\n============================")


