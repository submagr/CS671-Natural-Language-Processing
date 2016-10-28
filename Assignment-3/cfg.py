from pprint import pprint

class CYKParser(): 
    def __init__(self, rules = 'data/rules'):
        self.grammar = self.__read_grammar(rules)
        self.__get_terminals_nonTerminals()

    def __read_grammar(self, f):
        '''
        Given a file containing rules, return a dictionary of those rules.
        '''

        grammar = { 
            "lr": {}, 
            "rl": {}
        }
        rules = open(f, 'r').readlines()
        for rule in rules:
            tmp = rule.split()
            lhs = tmp[0]
            rhs = tuple(tmp[1:])
            grammar["lr"].setdefault(lhs, []).append(rhs)
            grammar["rl"].setdefault(rhs, []).append(lhs)

        return grammar

    def __producers(self, rhs):
        '''
        Given rhs of a grammer rule, 
        return list of possible lhs's
        '''
        if rhs in self.grammar["rl"]:
            return list(self.grammar["rl"][rhs])
        else: 
            return []

    def __to_tree(self, sentence, table, ptrTable, index):
        '''
        Input: index (i, j, k)
        Output: List containing parse tree
        '''
        i = index[0]
        j = index[1]
        k = index[2]
        tree = [table[i][j][k]]
        if len(ptrTable[i][j]) > k:
            rhs = []
            rhs.append(self.__to_tree(sentence, table, ptrTable, ptrTable[i][j][k][0]))
            rhs.append(self.__to_tree(sentence, table, ptrTable, ptrTable[i][j][k][1]))
        else: 
            rhs = [sentence[i]]
        tree.extend(rhs)
        return tree

    def __get_terminals_nonTerminals(self):
        #get set of symbols 
        symbols = set()
        for lhs, possibleRHSs in self.grammar["lr"].items():
            symbols.add(lhs)
            for rhs in possibleRHSs:
                for i in range(len(rhs)):
                    symbols.add(rhs[i])
        self.terminals = set()
        self.nonTerminals = set()
        for symbol in symbols: 
            if symbol in self.grammar["lr"]:
                self.nonTerminals.add(symbol)
            else:
                self.terminals.add(symbol)
        assert(len(set.intersection(self.terminals, self.nonTerminals)) == 0)

    def __get_POS(self, word):
        pos = []
        if word in ['the']:
            pos.append("Det")
        if word in ['through']:
            pos.append("Preposition")
        if word in ['Houston']:
            pos.append("PP")
        if word in ['book']:
            pos.append("Verb")
        if word in ['book']:
            pos.append("Noun")
        return pos 

       
    def parse(self, sentence):
        '''
        Takes a sentence as list of words,
        returns parse tree 
        '''
        length = len(sentence)+1
        table = [ [[] for x in range(length)] for x in range(length)]
        ptrTable = [ [[] for x in range(length)] for x in range(length)]

        for j in range(1, length):
            table[j-1][j].extend(self.__producers(tuple([sentence[j-1]])))
            pos_tags = self.__get_POS(sentence[j-1])
            # Add symbol if If not already in table[j-1][j]
            [table[j-1][j].append(x) for x in pos_tags if x not in table[j-1][j]]
            for i in range(j-2, -1, -1):
                for k in range(i+1, j):
                    for l, B in enumerate(table[i][k]):
                        for m, C in enumerate(table[k][j]):
                            lhs = self.__producers((B,C)) 
                            if lhs:
                                table[i][j].extend(lhs)
                                ptrTable[i][j].extend([((i, k, l), (k, j, m))]*len(lhs))

        self.table = table
        self.ptrTable = ptrTable
        trees = []
        for k in range(len(table[0][length-1])):
            if table[0][length-1][k] == 'S':
                trees.append(self.__to_tree(sentence, table, ptrTable, (0, length-1, k)))
        return trees

    def to_str(self, tree):
        ''' 
        Return the formatted string of a parse tree.
        '''
        if not tree:
            return None
        # Stringify any lists inside tree
        for i in range(len(tree)):
            if isinstance(tree[i], list):
                tree[i] = self.to_str(tree[i])

        # Turn the list of strings, tree, into a formatted string
        return "({})".format(' '.join(tree)) 

if __name__ == "__main__":
    parser = CYKParser()
    while 1: 
        rawSentence = raw_input("Enter sentence to parse: ")
        trees = parser.parse(rawSentence.split())
        for tree in trees:
            print parser.to_str(tree)
