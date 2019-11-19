class EliminateUselessVariables:
    grammar = None
    generating = []
    not_generating = []
    reachable = []
    unreachable = []

    def __init__(self, _grammar):
        self.grammar = _grammar
        self.generating = self.grammar.terminals
        self.generating.append('S')
        self.elimination_p1()
        self.clean_after_p1()
        self.elimination_p2()
        self.clean_after_p2()
        self.print_result()

    def elimination_p1(self):
        productions = self.grammar.get_separate_productions()
        _generating = self.generating
        test = True
        while test:
            for prod in productions:
                if self.is_generating(prod[1]) and prod[0] not in _generating:
                    _generating.append(prod[0])
            if _generating == self.generating:
                test = False
            self.generating = _generating

    def is_generating(self, prod):
        for g in self.generating:
            prod = prod.replace(g, '')
        return not prod or prod.islower()

    def clean_after_p1(self):
        new_productions = dict()
        for key, value in self.grammar.productions.items():
            if key in self.generating:
                new_rules = []
                for rule in value:
                    if self.is_generating(rule):
                        new_rules.append(rule)
                new_productions[key] = new_rules
            else:
                self.not_generating.append(key)
        self.grammar.productions = new_productions

    def elimination_p2(self):
        reachable_productions = ['S']
        next_productions_to_test = ['S']
        test = True
        while test:
            for rp in next_productions_to_test:
                if self.grammar.productions[rp]:
                    for rule in self.grammar.productions[rp]:
                        reachable = [c for c in rule if c.isupper()]
                        reachable_productions += reachable
                        next_productions_to_test = reachable
            if all(elem in reachable_productions for elem in next_productions_to_test):
                test = False
        self.reachable = reachable_productions

    def clean_after_p2(self):
        new_productions = dict()
        for key, value in self.grammar.productions.items():
            if key in self.reachable:
                new_productions[key] = value
            else:
                self.unreachable.append(key)
        self.grammar.productions = new_productions

    def print_result(self):
        print("============================\n")
        print("Eliminating Useless symbols")
        print('\n')
        if self.not_generating:
            print("Symbols which can't produce any string: " + ", ".join(self.not_generating))
        if self.unreachable:
            print("Symbols not reachable from the start: " + ", ".join(self.unreachable))
        print("\n")
        self.grammar.print_grammar()
        print("\n============================")
