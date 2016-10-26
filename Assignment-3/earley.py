from pprint import pprint


class EarleyParser(): 
    def __init__(self, rules = 'data/rules'):
        self.grammar = self.__read_grammar(rules)
        self.__get_terminals_nonTerminals()
        self.counter = -1
        self.debug = 0

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

    def __getState(self, chartNum, rule, i, j, dot, bPtr = None ):
        state = {
            "rule": rule,
            "i": i,
            "j": j,
            "dot": dot,
            "bPtr": bPtr
        }
        self.counter[chartNum] += 1
        return self.counter[chartNum], state

    def __addToChart(self, chart, chartNum, rule, i, j, dot, bPtr = None, stepDebug = ""):
        stateId, state = self.__getState(chartNum, rule, i, j, dot, bPtr)
        alreadyExisting = 0
        for existingState in chart[chartNum]:
            if existingState == state:
                alreadyExisting = 1
                self.counter[chartNum] -= 1
                break
        if not alreadyExisting: 
            chart[chartNum].append(state)
            self.__debugger(chart, chartNum, state, stateId, stepDebug)

    def __debugger(self, chart, chartNum, state, stateId, stepDebug):
        if self.debug:
            print "------Add state ", state, "to chart[", chartNum, "] due to ", stepDebug
            for stateId, state in enumerate(chart[chartNum]):
                ruleStr = state["rule"][0] + " ---> "
                placedDot = 0
                for i in range(1, len(state["rule"])): 
                    symbol = state["rule"][i]
                    if state["dot"] + 1 == i:
                        ruleStr += " * " 
                        placedDot = 1
                    ruleStr += symbol + " "
                if not placedDot:
                    ruleStr += " * "
                posStr = str(state["i"]) + ", "+ str(state["j"])
                print stateId, ":: [",  ruleStr, "] [" , posStr, "] [ ", str(state["bPtr"]), " ]"

    def __isIncomplete(self, state):
        return not (state["dot"]+1 == len(state["rule"]))

    def __predictor(self, chart, state):
        assert(state["dot"] + 1 <= len(state["rule"]) - 1)
        nextSymbol = state["rule"][state["dot"]+1]
        assert(nextSymbol in self.nonTerminals)
        for rhs in self.grammar["lr"][nextSymbol]:
            rule = [nextSymbol] + list(rhs)
            self.__addToChart(chart, state["j"], rule , state["j"], state["j"], 0, None, "PREDICT")
        return

    def __get_POS(self, word):
        #TODO
        return [word]

    def __scanner(self, chart, state, sentence):
        if len(sentence) > state["j"]:
            nextWord = sentence[state["j"]]
            nextSymbol = state["rule"][state["dot"]+1]
            if nextSymbol in self.__get_POS(nextWord):
                self.__addToChart(chart, state["j"]+1, [nextSymbol, nextWord], state["j"], state["j"]+1, 1, None, "SCANNER")
        return 

    def __completer(self, chart, chartNum, state, stateId):
        assert(state["dot"]+1 == len(state["rule"]))
        completedSymbol = state["rule"][0]
        for affectedState in chart[state["i"]]:
            if self.__isIncomplete(affectedState) and affectedState["rule"][affectedState["dot"]+1] == completedSymbol:
                bPtr = affectedState["bPtr"]
                if bPtr == None:
                    bPtr = []
                bPtr.append((chartNum, stateId))
                self.__addToChart(chart, state["j"], affectedState["rule"], affectedState["i"], state["j"], affectedState["dot"]+1, bPtr, "COMPLETER")
        return 

    def __to_tree(self, chart, chartNum, stateId):
        state = chart[chartNum][stateId]
        if state["bPtr"] == None:
            return None
        parse = [state["rule"][0]]
        for i in range(1, len(state["rule"])):
            tree = self.__to_tree(chart, state["bPtr"][i-1][0], state["bPtr"][i-1][1])
            if tree is not None:
                parse.append(tree)
        return parse

    def parse(self, sentence):
        '''
        Takes a sentence as list of words,
        returns parse tree 
        '''
        length = len(sentence)+1
        self.counter = [-1 for x in range(length)]
        chart = []
        for i in range(length):
            chart.append([])

        self.__addToChart(chart, 0, ["GAMMA", "S"], 0, 0, 0, None, "Start")

        for i in range(length):
            j = 0
            while j < len(chart[i]):
                state = chart[i][j]
                if self.__isIncomplete(state) and state["rule"][state["dot"]+1] not in self.terminals:
                    self.__predictor(chart, state)
                elif self.__isIncomplete(state) and state["rule"][state["dot"]+1] in self.terminals:
                    self.__scanner(chart, state, sentence)
                else:
                    self.__completer(chart, i, state, j )
                j+=1

        possibleParses = []
        for stateId, state in enumerate(chart[length-1]):
            if not self.__isIncomplete(state) and state["rule"][0] == "S":
                possibleParses.append(self.__to_tree(chart, length-1, stateId))
        return possibleParses

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
    parser = EarleyParser()
    while 1: 
        rawSentence = raw_input("Enter sentence to parse: ")
        trees = parser.parse(rawSentence.split())
        for tree in trees:
            print parser.to_str(tree)
