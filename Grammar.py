from EliminateUselessVariables import EliminateUselessVariables
from EliminateEpsilonProductions import EliminateEpsilonProductions
from EliminateUnitProductions import  EliminateUnitProductions


class Grammar:
    terminals = []
    non_terminals = []
    productions = dict()

    def __init__(self, grammar_string):
        print("============================\n")
        self.parse_grammar(grammar_string)
        print("This is initial grammar")
        print("\n")
        self.print_grammar()
        print("\n============================")
        print("\n\n")
        eliminated_grammar = EliminateEpsilonProductions(self).grammar
        print("\n\n")
        eliminated_grammar = EliminateUnitProductions(self).grammar
        print("\n\n")
        eliminated_grammar = EliminateUselessVariables(eliminated_grammar).grammar

    def parse_grammar(self, grammar_string):
        for line in grammar_string.splitlines():
            line_split = line.replace(" ", "").split('->')
            self.productions[line_split[0]] = line_split[1].split('|')

            for prod in self.productions:
                for rule in self.productions[prod]:
                    if rule.isalpha() and rule != 'ε':
                        if rule.islower() and rule not in self.terminals:
                            self.terminals.append(rule)
                        elif rule.isupper() and rule not in self.non_terminals:
                            self.non_terminals.append(rule)

    def get_separate_productions(self):
        productions = []
        for prod in self.productions:
            for rule in self.productions[prod]:
                productions.append((prod, rule))
        return productions

    def print_grammar(self):
        for symbol, prods in self.productions.items():
            print(symbol + " -> " + " | ".join(prods))





