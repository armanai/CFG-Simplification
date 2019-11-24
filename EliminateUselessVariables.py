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
        self.reachable.append('S')
        self.elimination_p1()
        self.clean_after_p1()
        self.elimination_p2()
        self.clean_after_p2()
        self.print_result()

    def elimination_p1(self):
        productions = self.grammar.get_separate_productions()
        _generating = [] + self.generating
        test = True
        while test:
            for prod in productions:
                if self.is_generating(prod[1]) and prod[0] not in _generating:
                    _generating.append(prod[0])
            if _generating == self.generating:
                test = False
            self.generating = _generating
        self.set_not_generating()

    def set_not_generating(self):
        for prod in self.grammar.productions:
            if prod[0] not in self.generating and prod[0] not in self.not_generating:
                print(prod[0])
                self.not_generating.append(prod[0])

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
        self.grammar.productions = new_productions

    def elimination_p2(self):
        productions = self.grammar.productions
        _reachable = [] + self.reachable
        prods_to_test = [] + self.reachable
        test = True
        while test:
            new_prods_to_test = []
            for ptt in prods_to_test:
                prods = productions[ptt]
                for prod in prods:
                    for p in prod:
                        if p.isupper():
                            if p not in _reachable:
                                _reachable.append(p)
                            elif p not in new_prods_to_test:
                                new_prods_to_test.append(p)
            if self.reachable == _reachable:
                test = False
            prods_to_test = new_prods_to_test
            self.reachable = _reachable

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
        if self.not_generating:
            print('\n')
            print("Symbols which can't produce any string: " + ", ".join(self.not_generating))
        if self.unreachable:
            print("Symbols not reachable from the start: " + ", ".join(self.unreachable))
        print("\n")
        self.grammar.print_grammar()
        print("\n============================")
